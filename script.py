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



def makeScript ():
    municipios = getMunicipioInformation("54")
    diccionario = {}
    for municipio in municipios:
        departamento = municipio["departamento"]["id"]
        print(departamento)
        myList = diccionario.get(departamento, [])
        print(myList)
        myList.append(municipio)
        diccionario[departamento] = myList
        print(diccionario)
    f = open("argentina.json", "w")        
    f.write(json.dumps(diccionario))
    f.close()
    
makeScript()
#Entre Rios, Santa Cruz

