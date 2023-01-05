import requests
import json


#https://apis.datos.gob.ar/georef/api/municipios?interseccion=provincia:54,departamento:54084

def makeMunicipioInfo(provinceId, departmentId):
    #print(provinceId, departmentId)
    municipiosDelDepartamento = []    
    #Buscar la info de todos los municipio de la provincia
    r = requests.get("https://apis.datos.gob.ar/georef/api/municipios?provincia="+provinceId)
    if r.status_code != 200:
        return []
    municipioDict = json.loads(r.text)
    #Para cada uno, tomar la long&lat
    for municipio in municipioDict["municipios"]:        
        latitud = municipio["centroide"]["lat"]
        longitud= municipio["centroide"]["lon"]
        #Buscar la info de las coordenadas
        r = requests.get("https://apis.datos.gob.ar/georef/api/ubicacion?lat={lat}&lon={lon}".format(lat=latitud, lon=longitud))
        if r.status_code != 200:
            next
        #Extraer el departamento al cual pertenece dicho municipio
        body = json.loads(r.text)        
        print(body)
        if(departmentId == body["ubicacion"]["departamento"]["id"]):
            #print("Agregado")
            #Agregarlo a la lista a devolver
            municipiosDelDepartamento.append(municipio)
    return municipiosDelDepartamento

def filterOwnMunicipios(departmentId, municipios): 
    return []

def getMunicipioInformation(provinceId):
    municipiosDeProvincia = []
    r = requests.get("https://apis.datos.gob.ar/georef/api/municipios?provincia="+provinceId)
    if r.status_code != 200:
        return []
    municipioDict = json.loads(r.text)
    for municipio in municipioDict["municipios"]:        
        latitud = municipio["centroide"]["lat"]
        longitud= municipio["centroide"]["lon"]
        #Buscar la info de las coordenadas
        r = requests.get("https://apis.datos.gob.ar/georef/api/ubicacion?lat={lat}&lon={lon}".format(lat=latitud, lon=longitud))
        if r.status_code != 200:
            next
        #Extraer el departamento al cual pertenece dicho municipio
        body = json.loads(r.text)        
        municipiosDeProvincia.append(body["ubicacion"])
    print(municipiosDeProvincia)        
    return municipiosDeProvincia        


def makeDepartmentInfo(provinceId):
    r =requests.get('https://apis.datos.gob.ar/georef/api/departamentos?provincia='+provinceId)
    if r.status_code != 200:
        return []
    departmentDictionary = json.loads(r.text)
    #print(departmentDictionary)
    for department in departmentDictionary["departamentos"]:        
        #print(department["nombre"])
        department["municipios"] = makeMunicipioInfo(provinceId, department["id"])
    return departmentDictionary        


def makeScript ():
    f = open("argentina.json", "w")    
    r =requests.get('https://apis.datos.gob.ar/georef/api/provincias')
    if r.status_code != 200:
        return
    print("Descargue las provincias")
    provinceDictionary = json.loads(r.text)
#    print(provinceDictionary)
#    print(provinceDictionary["provincias"][0])
    for province in provinceDictionary["provincias"]:
        print(province["nombre"])
        province["departamentos"] = makeDepartmentInfo(province["id"])
        f.write(json.dumps(provinceDictionary))
    print(provinceDictionary["provincias"][0])
    f.close()

#makeScript()    
getMunicipioInformation("70")
#Entre Rios, Santa Cruz