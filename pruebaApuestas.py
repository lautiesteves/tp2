import random
import requests
import csv
import os


def busca_fixture(dicc_equipos):
    lista_equipos = [*dicc_equipos.values()]
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_opciones = []
    #Imprimo equipos
    print("Equipos de la Liga Profesional Argentina:")
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    print("Ingrese el equipo del que desea obtener información sobre el fixture: ", end="")
    #Pido a usuario el Equipo
    equipo_a_buscar = validador_num(input_num(), lista_opciones)
    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]
    #Get Fixture
    respuesta = obtener_fixture()
    #Armo Lista de Partidos
    lista_partidos = obtener_lista_partidos(respuesta, id_equipo_a_buscar)
    
    return lista_partidos, id_equipo_a_buscar

def obtener_fixture() -> dict:
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params = {"league":"128","season": 2023, "from":"2023-01-15", "to":"2023-08-10"}
    url = "https://v3.football.api-sports.io/fixtures"
    return requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]


def busca_partidos_no_jugados(lista_partidos):
    estado = lista_partidos[2]["status"]["short"]
    lista_partidos.append(estado)


def obtener_wod(id:str)->bool: #SIEMPRE VA A DAR EL WIN_OR_DRAW DEL LOCAL
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params = {"fixture":id}
    url = "https://v3.football.api-sports.io/predictions"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"][0]
    if respuesta["predictions"]["winner"]["name"] == respuesta["teams"]["home"]["name"]:
        wod = respuesta["predictions"]["win_or_draw"]
    else:
        wod = not respuesta["predictions"]["win_or_draw"]
    return wod

def obtener_lista_partidos(fixture, id_equipo_a_buscar) -> list:
    lista_partidos = []
    for i in range(len(fixture)):
        localias = ["home", "away"]
        for localia in localias:
            if id_equipo_a_buscar == fixture[i]["teams"][localia]["id"]:
                fecha = str(fixture[i]["league"]["round"])
                numero_fecha = int(fecha[12:])
                estado = fixture[i]["fixture"]["status"]["short"]
                wod:bool = False #es para rellenar, no se va a acceder al wod de una fecha con "estado" == FT.
                if estado != "FT":
                    wod:bool = obtener_wod(fixture[i]["fixture"]["id"])
                lista_partidos.append([numero_fecha, fixture[i]["teams"], estado, wod])

    return sorted(lista_partidos) # Ordenado por fase y fecha. Ej "15" , teams , estado (FT y otros), wod(bool)



def imprimir_fixture(dicc_equipos:dict, lista_partidos:list, id_equipo:str):
    os.system("cls")
    print("FIXTURE DE {}".format(dicc_equipos[id_equipo].upper()))
    print(" "*8,"<LOCAL>"," "*67,"<VISITANTE>")
    print(" "*31,"---------------- PRIMERA FASE ----------------")
    
    for partido in lista_partidos:
        if partido[0] < 10:
            partido[0] = "0"+str(partido[0])
        partido[0] = str(partido[0])
        local = partido[1]["home"]["name"]
        visitante = partido[1]["away"]["name"]
        puntitos1= "."*(45 - (len(local)))
        puntitos2= "."*(40 - (len(visitante)))

        if partido[2] == "FT":
            print("Fecha {}.{}{}vs{}{} - TERMINADO".format(partido[0], local, puntitos1, puntitos2, visitante))
        else:
            if partido[3]:
                paga_local = "+MULT(10%)"
                paga_visitante = "+ MULT(100%)"
                puntitos1 = "."*(34 - (len(local)))
            else: 
                paga_local = "+MULT(100%)"
                paga_visitante = "+ MULT(10%)"
                puntitos1 = "."*(33 - (len(local)))
            print("Fecha {}.{} {}{}vs{}{} {}".format(partido[0], local, paga_local, puntitos1, puntitos2, visitante, paga_visitante))



def elije_partido(dinero_disponible_usuario, lista_partidos) -> tuple:
    #Pido Partido a apostar
    partidos_restantes:list = []
    for partido in lista_partidos:
        if partido[2] != "FT": partidos_restantes.append(int(partido[0]))
    print("-"*25)
    print("Escriba el numero de la fecha del partido (sin definir) donde quiere realizar su apuesta: ", end="")
    partido_a_apostar = str(validador_num(input_num(), partidos_restantes))
    for i in range(len(lista_partidos)):
        if lista_partidos[i][0] == partido_a_apostar:
            nombre_local = lista_partidos[i][1]["home"]["name"]
            nombre_visitante = lista_partidos[i][1]["away"]["name"]
    print("-"*45)
    print(f"Elegiste apostar al partido: {nombre_local}(L) vs {nombre_visitante}(V)")
    print("-"*25)
    print("A que resultado quiere apostar:")
    print(f"1. Ganador {nombre_local}(L)\n2. Empate\n3. Ganador {nombre_visitante}(V)")
    apuesta = validador_num(input_num(), [1,2,3])   # 1: APUESTA POR EL LOCAL - 2: EMPATE - 3: APUESTA POR EL VISITANTE
    
    os.system("cls")
    if apuesta == 1:
        impresion = f"Elegiste apostar por el equipo {nombre_local}(L)"
    elif apuesta == 2:
        impresion = f"Elegiste apostar por un empate entre {nombre_local}(L) y {nombre_visitante}(V)"
    else:
        impresion = f"Elegiste apostar por el equipo {nombre_visitante}(V)"
    print(impresion)
    print("-"*25)
    print("Escriba la cantidad de dinero que desea apostar: ", end="")
    dinero_apostado = input_float()
    #Validar que el usuario cuente con ese dinero
    while dinero_apostado > dinero_disponible_usuario or dinero_apostado == 0:
        print("-"*25)
        if dinero_apostado > dinero_disponible_usuario:
            print(f"No cuenta con esa cantidad de dinero. Actualmente dispone de ${dinero_disponible_usuario}.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        else:
            print(f"Debe ingresar una cantidad de dinero mayor a 0.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        dinero_apostado = input_float()
    os.system("cls")
    print("Apuesta realizada exitosamente!")
    print(f"Apostaste ${dinero_apostado} {impresion[17:]}")
    print("-"*25)
    input("Presione enter para conocer los resultados del partido.")
    print("-"*25)
    return dinero_apostado, apuesta, partido_a_apostar


#No incluyo el partido porque entiendo que no nos interesa para saber cuanto gana, lo unico que nos
#interesa es saber es si el win or draw es true y si se apuesta por el local/empate/visitante
def resolver_apuesta(dinero_apostado:float, apuesta:int, win_or_draw:bool, nombres:tuple) -> float: #EL WIN OR DRAW ES DEL EQUIPO LOCAL
    #Dado simula resultado:
    #1 -> Gana Local
    #2 -> Empate
    #3 -> Gana Visitante
    dado = 3 #random.randint(1,3)
    #TO-DO Resolver cantidad ganancia con win_or_draw
    multiplicador = random.randint(2,4)
    if (apuesta == 1 and win_or_draw==True) or (apuesta == 3 and win_or_draw==False):
        multiplicador = multiplicador*0.1
    #Dado == 2 da Empate
    #Falta ver si se quita primero lo apostado y despues lo recupera o si se quita solo en caso de perder
    
    if dado == 2:
        #Dado da Empate y se Aposto Empate
        if apuesta == 2:
            print(f"Felicitacioness!! El partido entre {nombres[0]} y {nombres[1]} fue un empate!! ya puede encontrar su ganancia de ${dinero_apostado*0.5}")
            ganancia = dinero_apostado*0.5
        #Dado da Empate y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El partido entre {nombres[0]} y {nombres[1]} terminó empatado, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    #Dado == 1 da que Gana Local
    elif dado == 1:
        #Dado da Gana Local y se Aposto Gana Local
        if apuesta == 1:
            print(f"Felicitaciones!! Ganó {nombres[0]}!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana Local y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El ganador ha sido {nombres[0]}, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    #Dado == 3 da que Gana Visitante
    elif dado == 3:
        #Dado da gana V y se Aposto Gana V
        if apuesta == 3:
            print(f"Felicitacioness!! Ganó {nombres[1]}!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana V y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El ganador ha sido {nombres[1]}, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    return ganancia


def wod_partido(lista_partidos:list, partido_a_apostar:str) -> tuple:
    for partido in lista_partidos:
        if int(partido[0]) == int(partido_a_apostar):
            local = partido[1]["home"]["name"]
            visitante = partido[1]["away"]["name"]
            equipos = local, visitante
            return partido[3], equipos


def main_apuestas(): #abierto a cambio de nombre, lo cambie para que no sea parecido a una variable
    print("TO-DO: EXPLICACION DE APUESTAS")
    input("Presione enter para comenzar.")
    dicc_equipos = {451: 'Boca JRS', 434: 'Gimnasia (LP)', 435: 'River Plate', 436: 'Racing Club', 437: 'Rosario Central', 438: 'Vélez Sarsfield', 439: 'Godoy cruz',
    440: 'Belgrano (Cba)', 441: 'Unión de Santa Fé', 442: 'Defensa y Justicia', 445: 'Huracán', 446: 'Lanús', 448: 'Colón de Santa Fé', 449: 'Banfield', 450: 'Estudiantes (LP)', 452: 'Tigre',
    453: 'Independiente', 455: 'Atlético Tucumán', 456: 'Talleres (Cba)', 457: 'Newells Old Boys', 458: 'Argentinos JRS', 459: 'Arsenal de Sarandí', 460: 'San Lorenzo', 474: 'Sarmiento (J)',
    478: 'Instituto (Cba)', 1064: 'Platense', 4065: 'Central Córdoba (SdE)', 2434: 'Barracas Central'}
    usuario = {'prueba@gmail.com': ['Prueba', '$pbkdf2-sha256$29000$ZGxN6Z2zdi5lrPVeS6l1bg$Mq3DdwiQoYcOoZLHF.nYBb5vIMWs8dK3RqCE5zXiajQ', '120', 'DDMMYYYY', '290']}
    dinero_disponible_usuario: float = float([*usuario.values()][0][4])
    lista_partidos, id_equipo = busca_fixture(dicc_equipos)
    imprimir_fixture(dicc_equipos, lista_partidos, id_equipo)
    dinero_apostado, apuesta, partido_a_apostar = elije_partido(dinero_disponible_usuario, lista_partidos)
    win_or_draw, equipos = wod_partido(lista_partidos, partido_a_apostar)
    ganancia = resolver_apuesta(dinero_apostado, apuesta, win_or_draw, equipos)
    print("-"*30)
    print(f"{ganancia}\nGANAMOS EL MUNDIAL")
    cargar_dinero(usuario, ganancia)
    if(ganancia > 0):
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Gana", str(ganancia))
    else:
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Pierde", str(ganancia))

    

"""--------------------------------------------------------------------------------------------------------------------------------------------------------------"""

#FUNCIONES QUE YA ESTAN EN JUGARSELA:PY

def cargar_dinero(usuario: dict, cantidad_a_cargar: int) -> None:
    usuarios_existentes: dict = obtener_usuarios_existentes()
    email: str = list(usuario.keys())[0]
    dinero_disponible = int(usuarios_existentes[email][4])
    usuarios_existentes[email][4] = str(dinero_disponible + cantidad_a_cargar)
    print(f"Carga exitosa! Ahora dispones de ${usuarios_existentes[email][4]}!")
    modificar_usuario(usuarios_existentes)

def modificar_usuario(usuarios_actualizados: dict) -> None:
    with open('usuarios.csv', 'w', newline='') as usuariosCsv:
        csvWriter = csv.writer(usuariosCsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(("ID Usuario", "Nombre Usuario", "Contraseña", "Dinero Apostado", "Fecha Última Apuesta", "Dinero Disponible"))
        for id in usuarios_actualizados:
            csvWriter.writerow((id, usuarios_actualizados[id][0], usuarios_actualizados[id][1], usuarios_actualizados[id][2], usuarios_actualizados[id][3], usuarios_actualizados[id][4]))

def obtener_usuarios_existentes() -> dict:
    usuarios_existentes: dict = {}
    with open('usuarios.csv', newline='') as usuariosCsv:
        csvReader = csv.reader(usuariosCsv, delimiter = ",")
        next(csvReader)
        for row in csvReader:
            usuarios_existentes[row[0]] = [row[1],row[2],row[3],row[4], row[5]]
    return usuarios_existentes

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

def es_float(num) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False

def input_float() -> float:
    numero = input("")
    while not es_float(numero):
        numero = input("El valor ingresado debe ser un número. Inténtelo nuevamente: ")
    numero = float(numero)
    return numero

def input_alfa() -> str:
    """
    PRE: -
    POST: Devuelve un valor alfabético, en minúsculas y sin tildes.
    """
    palabra = input("").lower()
    while palabra.isalpha() != True:
        palabra = input("El valor ingresado no es alfabético. Inténtelo nuevamente: ").lower()
    return palabra

def validador_str(valor:str, valores:list) -> str:
    """
    PRE: Ingresa un string y una lista.
    POST: Devuelve el string solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"\"{valor}\" es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_alfa()
    return valor

main_apuestas()
