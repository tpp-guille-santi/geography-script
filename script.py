import requests
import json


#https://apis.datos.gob.ar/georef/api/municipios?interseccion=provincia:54,departamento:54084

def getMunicipioInformation(provinceId):
    municipiosDeProvincia = []
    r = requests.get("https://apis.datos.gob.ar/georef/api/municipios?provincia="+provinceId+"&max=5000")
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
    #print(municipiosDeProvincia)        
    return municipiosDeProvincia        

def makeProvincesMunicipiosDict (provinceId):
    municipios = getMunicipioInformation(provinceId)
    diccionario = {}
    for municipio in municipios:
        departamento = municipio["departamento"]["id"]
        myList = diccionario.get(departamento, [])
        myList.append(municipio["municipio"])
        diccionario[departamento] = myList
    #print(diccionario)
    return diccionario
    

def makeDepartmentInfo(provinceId):
    r =requests.get('https://apis.datos.gob.ar/georef/api/departamentos?provincia='+provinceId)
    if r.status_code != 200:
        return []
    departmentDictionary = json.loads(r.text)
    print("Consigo municipios de la provincia")
    municipios = makeProvincesMunicipiosDict(provinceId)
    for department in departmentDictionary["departamentos"]:        
        department["municipios"] =municipios[department["id"]]
    return departmentDictionary["departamentos"]        


def makeProvinceInformation():
    r =requests.get('https://apis.datos.gob.ar/georef/api/provincias')    
    if r.status_code != 200:
        return
    print("Descargue las provincias")
    provinceDictionary = json.loads(r.text)
    for province in provinceDictionary["provincias"]:
        print(province["nombre"])
        province["departamentos"] = makeDepartmentInfo(province["id"])
        f = open("argentina_2.json", "w")            
        f.write(json.dumps(provinceDictionary))    
        f.close()    
    return

makeProvinceInformation()
#Entre Rios, Santa Cruz

