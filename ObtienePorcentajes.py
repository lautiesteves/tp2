"""import http.client

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"
    }

conn.request("GET", "/standings?league=128&season=2022&team=451", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))"""
import requests
"""
lista_equipos_ids = [451, 434, 435, 436, 437, 438, 439, 440, 441, 442, 445, 446, 448, 449, 450, 452, 453, 455, 456, 457, 458, 459, 460, 474, 478, 1064, 4065, 2434]
lista_equipos = ["Boca JRS", "Gimnasia (LP)", "River Plate", "Racing Club", "Rosario Central", "Vélez Sarsfield", "Godoy cruz", "Belgrano (Cba)", "Unión de Santa Fé", "Defensa y Justicia", "Huracán", "Lanús", "Colón de Santa Fé", "Banfield", "Estudiantes (LP)", "Tigre", "Independiente", "Atlético Tucumán", "Talleres (Cba)", "Newells Old Boys", "Argentinos JRS", "Arsenal de Sarandí", "San Lorenzo", "Sarmiento (J)", "Instituto (Cba)", "Platense", "Central Córdoba (SdE)", "Barracas Central"]
print("Equipos de la LPF:")
for i in range(len(lista_equipos)):
    print(f"{i+1}. {lista_equipos[i]}")
print("-"*20)
equipo = int(input("Ingrese de que equipo desea buscar su plantel: "))

while equipo <= 0 or equipo > len(lista_equipos_ids):
    equipo = int(input("Ingreso inválido. Seleccione uno nuevo: "))


id_equipo = lista_equipos_ids[equipo-1]
"""
"""
def MostrarEstadioYEscudo():
    lista_equipos_ids = [451, 434, 435, 436, 437, 438, 439, 440, 441, 442, 445, 446, 448, 449, 450, 452, 453, 455, 456, 457, 458, 459, 460, 474, 478, 1064, 4065, 2434]
    lista_equipos = ["Boca JRS", "Gimnasia (LP)", "River Plate", "Racing Club", "Rosario Central", "Vélez Sarsfield", "Godoy cruz", "Belgrano (Cba)", "Unión de Santa Fé", "Defensa y Justicia", "Huracán", "Lanús", "Colón de Santa Fé", "Banfield", "Estudiantes (LP)", "Tigre", "Independiente", "Atlético Tucumán", "Talleres (Cba)", "Newells Old Boys", "Argentinos JRS", "Arsenal de Sarandí", "San Lorenzo", "Sarmiento (J)", "Instituto (Cba)", "Platense", "Central Córdoba (SdE)", "Barracas Central"]
    print("Equipos de la LPF:")
    for i in range(len(lista_equipos)):
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    equipo_a_buscar = int(input("Ingrese el equipo del que desea obtener información sobre el estadio: "))
    while equipo_a_buscar <= 0 or equipo_a_buscar > len(lista_equipos_ids):
            equipo_a_buscar = int(input("Ingreso inválido. Seleccione uno nuevo: "))
    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]

    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"}

    params ={"league":"128","season": 2022}

    url = "https://v3.football.api-sports.io/teams"

    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #team, venue["name", "address", "city", "capacity", " surface", "image"]
    print("-"*20)
    for i in range(len(respuesta)):
        if respuesta[i]["team"]["id"] == id_equipo_a_buscar:
            print("Escudo:", respuesta[i]["team"]["logo"])   #Ver si se puede imprimir el escudo en lugar de una url
            print(respuesta[i]["team"]["name"].upper() + ":")
            print("Año de fundación:", respuesta[i]["team"]["founded"])
            print("País:", respuesta[i]["team"]["country"])
            print("Ciudad:", respuesta[i]["venue"]["city"])
            print("Estadio:", respuesta[i]["venue"]["name"])
            print("Capacidad:", respuesta[i]["venue"]["capacity"], "espectadores")
            print("Dirección:", respuesta[i]["venue"]["address"])
            if respuesta[i]["venue"]["surface"] == "grass": print("Superficie: Césped")
            print("Imagen:", respuesta[i]["venue"]["image"])  #Ver si se puede imprimir la foto del estadio en lugar de una url
            print("-"*20)"""

def validador_num(valor:int, valores:list) -> int:
    """
    PRE: Ingresa un entero y una lista.
    POST: Devuelve el entero solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"{valor} es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_num()
    return valor

def input_num() -> int:
    """
    PRE: -
    POST: Devuelve un valor numérico.
    """
    numero = input("")
    while numero.isnumeric() != True:
        numero = input("El valor ingresado debe ser un número. Inténtelo nuevamente: ")
    numero = int(numero)
    return numero

def MostrarFixture():
    numero_temporada = int(input("Ingrese numero de temporada para ver el fixture: "))
    numero_fecha = int(input("Ingrese numero de fecha para ver el fixture: "))
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"}
    params ={"league":"128","season": numero_temporada, "round": f"1st Phase - {numero_fecha}"}
    url = "https://v3.football.api-sports.io/fixtures"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]
    print(f"Fixture de la fecha {numero_fecha}:")
    print("-"*20)
    for i in range(14):
        print(respuesta[i]["teams"]["home"]["name"], "VS", respuesta[i]["teams"]["away"]["name"])
        print(respuesta[i]["fixture"]["status"])
        print(respuesta[i]["goals"]["home"], "\t\t", respuesta[i]["goals"]["away"])
    print("-"*20)

lista_equipos_ids = [451, 434, 435, 436, 437, 438, 439, 440, 441, 442, 445, 446, 448, 449, 450, 452, 453, 455, 456, 457, 458, 459, 460, 474, 478, 1064, 4065, 2434]
lista_equipos = ["Boca JRS", "Gimnasia (LP)", "River Plate", "Racing Club", "Rosario Central", "Vélez Sarsfield", "Godoy cruz", "Belgrano (Cba)", "Unión de Santa Fé", "Defensa y Justicia",
"Huracán", "Lanús", "Colón de Santa Fé", "Banfield", "Estudiantes (LP)", "Tigre", "Independiente", "Atlético Tucumán", "Talleres (Cba)", "Newells Old Boys", "Argentinos JRS",
"Arsenal de Sarandí", "San Lorenzo", "Sarmiento (J)", "Instituto (Cba)", "Platense", "Central Córdoba (SdE)", "Barracas Central"]
numero_temporada = int(input("Ingrese numero de temporada para ver el fixture: "))

lista_opciones = []
    
print("Equipos de la Liga Profesional Argentina:")
for i in range(len(lista_equipos)):
    lista_opciones.append(i+1)
    print(f"{i+1}. {lista_equipos[i]}")
print("-"*20)
print("Ingrese de que equipo desea buscar sus estadísticas de goles: ", end="")
equipo = validador_num(input_num(), lista_opciones)

id_equipo = lista_equipos_ids[equipo-1]

headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"}
params ={"league":128,"season":numero_temporada,"team":id_equipo}
url = "https://v3.football.api-sports.io/teams/statistics"
respuesta = requests.get(url, params=params, headers=headers).json()["response"]["goals"]["for"]
numeros_porcentajes= []
porcentajes =[] #["0-15"],["16-30"],["31-45"],["46-60"],["61-75"],["76-90"],["91-105"],["106-120"] ej: ['31.58%', '10.53%', '10.53%', '15.79%', '10.53%', '15.79%', '5.26%', None]
porcentajes_str = ""
print("Goles a favor:", respuesta["total"]["total"])
for minutos in respuesta["minute"]:
    porcentajes.append(respuesta["minute"][minutos]["percentage"])
for i in porcentajes:
    porcentajes_str += str(i)
numeros_porcentajes = porcentajes_str.split("%")
for i in range(len(numeros_porcentajes)):
    if numeros_porcentajes[i] == "None":
        numeros_porcentajes[i] = "0"
    numeros_porcentajes[i] = float(numeros_porcentajes[i])

print(numeros_porcentajes)


"""min0_al15 = respuesta["minute"]["0-15"]["percentage"]
min16_al30 = respuesta["minute"]["16-30"]["percentage"]
min31_al45 = respuesta["minute"]["31-45"]["percentage"]
min46_al60 = respuesta["minute"]["46-60"]["percentage"]
min61_al75 = respuesta["minute"]["61-75"]["percentage"]
min76_al90 = respuesta["minute"]["76-90"]["percentage"]
min91_al105 = respuesta["minute"]["91-105"]["percentage"]
min106_al120 = respuesta["minute"]["106-120"]["percentage"]"""


"""for i in range(len(respuesta)):
    print(respuesta[i]["league"]["round"])"""


"""headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"}

params ={"league":"128","season": 2022}

url = "https://v3.football.api-sports.io/stadistics"

respuesta = requests.get(url, params=params, headers=headers).json()["response"]
print(respuesta)"""