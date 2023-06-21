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
    params = {"league":"128","season": 2023}
    url = "https://v3.football.api-sports.io/fixtures"
    return requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]

def obtener_lista_partidos(respuesta, id_equipo_a_buscar) -> list:
    lista_partidos = []
    for i in range(len(respuesta)):
        localias = ["home", "away"]
        for localia in localias:
            if id_equipo_a_buscar == respuesta[i]["teams"][localia]["id"]:
                ronda = str(respuesta[i]["league"]["round"])
                if len(ronda)==14:
                    numero_fecha = int(ronda[0] + ronda[12] + ronda[13])
                else: numero_fecha = int(ronda[0] + "0" + ronda[12])
                lista_partidos.append([numero_fecha, respuesta[i]["teams"], respuesta[i]["fixture"]["id"]])
    return sorted(lista_partidos) # Ordenado por fase y fecha. Ej "203" , teams , IDpartido
#                                                                   ↑ fase 2, fecha 3


def imprimir_fixture(dicc_equipos, lista_partidos, id_equipo):
    os.system("cls")
    print("FIXTURE DE {}".format(dicc_equipos[id_equipo].upper()))
    print(" "*9,"<LOCAL>"," "*58,"<VISITANTE>")
    print("                          ---------------- PRIMERA FASE ----------------")
    iterador = 0
    for partido in lista_partidos:
        iterador += 1
        if iterador == 28:
            print("                          ---------------- SEGUNDA FASE ----------------")
        if partido[0] > 200:
            partido[0] -= 200
        else:
            partido[0] -= 100
        if partido[0] < 10:
            partido[0] = "0"+str(partido[0])
        partido[0] = str(partido[0])
        local = partido[1]["home"]["name"]
        visitante = partido[1]["away"]["name"]
        puntitos1= "."*(32 - (len(local)))
        puntitos2= "."*(32 - (len(visitante)))
        print("Fecha {}. {}(WorD){}vs{}{}(WorD)".format(partido[0], local, puntitos1, puntitos2, visitante))


def elije_partido(dinero_disponible_usuario, lista_partidos):
    #Pido Partido a apostar
    print("-"*25)
    print("En que fase desea apostar:")
    print("1. Primera Fase\n2. Segunda Fase")
    fase = validador_num(input_num(), [1,2])
    print("-"*25)
    print("Escriba el numero de la fecha del partido donde quiere realizar su apuesta: ", end="")
    if fase == 1:
        partido_a_apostar = str(validador_num(input_num(), [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]))
    else:
        partido_a_apostar = str(validador_num(input_num(), [1,2,3,4,5,6,7,8,9,10,11,12,13,14]))
    
    id_partido, eq_local, eq_visitante = busca_id_partido(lista_partidos, partido_a_apostar, fase)
    #Pido a que equipo desea apostar
    os.system("cls")
    print(f"Elegiste apostar al partido: {eq_local}(L) vs {eq_visitante}(V)")
    print("-"*25)
    print("A que resultado quiere apostar:")
    print(f"1. Ganador {eq_local}(L)\n2. Empate\n3. Ganador {eq_visitante}(V)")
    apuesta = validador_num(input_num(), [1,2,3])
    
    os.system("cls")
    if apuesta == 1:
        impresion = f"Elegiste apostar por el equipo {eq_local}(L)"
    elif apuesta == 2:
        impresion = f"Elegiste apostar por un empate entre {eq_local}(L) y {eq_visitante}(V)"
    else:
        impresion = f"Elegiste apostar por el equipo {eq_visitante}(V)"
    print(impresion)
    print("-"*25)
    print("Escriba la cantidad de dinero que desea apostar: ", end="")
    dinero_apostado = input_num()
    #Validar que el usuario cuente con ese dinero
    while dinero_apostado > dinero_disponible_usuario or dinero_apostado == 0:
        print("-"*25)
        if dinero_apostado > dinero_disponible_usuario:
            print(f"No cuenta con esa cantidad de dinero. Actualmente dispone de ${dinero_disponible_usuario}.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        else:
            print(f"Debe ingresar una cantidad de dinero mayor a 0.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        dinero_apostado = input_num()
    os.system("cls")
    print("Apuesta realizada exitosamente!")
    print(f"Apostaste ${dinero_apostado} {impresion[17:]}")
    print("-"*25)
    input("Presione enter para continuar.")

    return dinero_apostado, apuesta, id_partido

def busca_id_partido(lista_partidos, partido_apostado, fase):
    if len(partido_apostado) == 1:
        partido_apostado = "0"+partido_apostado
    
    inicio = 0
    if fase == 2:
        inicio = 27
    for i in range(inicio, len(lista_partidos)):
        if lista_partidos[i][0] == partido_apostado:
            id_partido = lista_partidos[i][2]
            nombre_local = lista_partidos[i][1]["home"]["name"]
            nombre_visitante = lista_partidos[i][1]["away"]["name"]

    return id_partido, nombre_local, nombre_visitante


def obtener_win_or_draw():
    pass

#No incluyo el partido porque entiendo que no nos interesa para saber cuanto gana, lo unico que nos
#interesa es saber es si el win or draw es true y si se apuesta por el local/empate/visitante
def resolver_apuesta(dinero_apostado:float, apuesta:int, win_or_draw:bool):
    #Dado simula resultado:
    #1 -> Gana Local
    #2 -> Empate
    #3 -> Gana Visitante
    dado = random.randint(1,3)
    #TO-DO Resolver cantidad ganancia con win_or_draw
    multiplicador = 3
    if win_or_draw: multiplicador = 0.3
    #Dado == 2 da Empate
    #Falta ver si se quita primero lo apostado y despues lo recupera o si se quita solo en caso de perder
    if dado == 2:
        #Dado da Empate y se Aposto Empate
        if apuesta == 2:
            print(f"Felicitacioness!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}.")
            ganancia = dinero_apostado*0.5
        #Dado da Empate y se Aposto otra cosa
        else:
            print("Lo sentimos. El partido terminó empatado por lo que lamentablemente no se recupera lo apostado")
            ganancia = -dinero_apostado
    #Dado == 1 da que Gana Local
    elif dado == 1:
        #Dado da Gana Local y se Aposto Gana Local
        if apuesta == 1:
            print(f"Felicitaciones!! Ganó (L)!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}.")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana Local y se Aposto otra cosa
        else:
            print("Lo sentimos. El ganador ha sido el local por lo que lamentablemente no se recupera lo apostado")
            ganancia = -dinero_apostado
    #Dado == 3 da que Gana Visitante
    elif dado == 3:
        #Dado da gana V y se Aposto Gana V
        if apuesta == 3:
            print(f"Felicitacioness!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}.")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana V y se Aposto otra cosa
        else:
            print("Lo sentimos. El ganador ha sido el visitante por lo que lamentablemente no se recupera lo apostado")
            ganancia = -dinero_apostado
    return ganancia


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
    dinero_apostado, apuesta, id_partido = elije_partido(dinero_disponible_usuario, lista_partidos)
    win_or_draw:bool = obtener_win_or_draw(id_partido, apuesta)
    #TO-DO Buscar win or draw con el id del partido y ver si la apuesta coincide con el win or draw
    ganancia = resolver_apuesta(dinero_apostado, apuesta, win_or_draw)
    cargar_dinero(usuario, ganancia)



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

"""def MostrarFixtureViejo():
    dicc_equipos = {451: 'Boca JRS', 434: 'Gimnasia (LP)', 435: 'River Plate', 436: 'Racing Club', 437: 'Rosario Central', 438: 'Vélez Sarsfield', 439: 'Godoy cruz',
    440: 'Belgrano (Cba)', 441: 'Unión de Santa Fé', 442: 'Defensa y Justicia', 445: 'Huracán', 446: 'Lanús', 448: 'Colón de Santa Fé', 449: 'Banfield', 450: 'Estudiantes (LP)', 452: 'Tigre',
    453: 'Independiente', 455: 'Atlético Tucumán', 456: 'Talleres (Cba)', 457: 'Newells Old Boys', 458: 'Argentinos JRS', 459: 'Arsenal de Sarandí', 460: 'San Lorenzo', 474: 'Sarmiento (J)',
    478: 'Instituto (Cba)', 1064: 'Platense', 4065: 'Central Córdoba (SdE)', 2434: 'Barracas Central'}
    lista_equipos = [*dicc_equipos.values()]    
    lista_opciones = []
    lista_equipos_ids = [*dicc_equipos.keys()]
    print("Equipos de la Liga Profesional Argentina:")
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    print("Ingrese el equipo del que desea obtener información sobre el fixture: ", end="")
    equipo_a_buscar = validador_num(input_num(), lista_opciones)
    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params ={"league":"128","season": 2023}
    url = "https://v3.football.api-sports.io/fixtures"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]
    print(respuesta[0])
    lista_partidos = []
    lista_orden = [0, 11, 20, 21, 22, 23, 24, 25, 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 27, 33, 34, 35, 36, 37, 38, 39, 40, 28, 29, 30, 31, 32]
    for i in range(len(respuesta)):
        if id_equipo_a_buscar == respuesta[i]["teams"]["home"]["id"]:
            lista_partidos.append([respuesta[i]["league"]["round"], respuesta[i]["teams"]["away"]["name"], "(L)", respuesta[i]["fixture"]["id"]])
        elif id_equipo_a_buscar == respuesta[i]["teams"]["away"]["id"]:
            lista_partidos.append([respuesta[i]["league"]["round"], respuesta[i]["teams"]["home"]["name"], "(V)", respuesta[i]["fixture"]["id"]])
    lista_partidos = sorted(lista_partidos)
    lista_opciones_partidos = []
    print(f"El fixture de {dicc_equipos[id_equipo_a_buscar]} en este campeonato es:")
    print("------PRIMERA FASE------")
    for i in range(27):
        print(f"{i+1}-", lista_partidos[lista_orden[i]][1], lista_partidos[lista_orden[i]][2], lista_partidos[lista_orden[i]][0])
        lista_opciones_partidos.append(lista_partidos[lista_orden[i]][3])
    print("------SEGUNDA FASE------")
    for i in range(27,41):
        print(f"{i+1}-", lista_partidos[lista_orden[i]][1], lista_partidos[lista_orden[i]][2], lista_partidos[lista_orden[i]][0])
        lista_opciones_partidos.append(lista_partidos[lista_orden[i]][3])
    print("Escriba el número del partido en el cual quiere realizar su apuesta: ", end="")
    opt = validador_num(input_num())
    while opt>40 or opt<1:
        print("Ingreso inválido. Ingrese uno de los numeros colocados entre las opciones antes mostradas: ", end="")
        opt = validador_num(input_num())
    apuesta = input("En caso de querer apostar por el local ingrese 1, en caso de apostar por un empate ingrese 2, y en caso de apostar por el visitante ingrese 3 \n")
    #VALIDAR EL INGRESO DEL USUARIO
    print("Escriba la cantidad de dinero que desea apostar: ", end="")
    dinero_apostado = validador_num(input_num())
    #VALIDAR CON LA BILLETERA QUE EL USUARIO CUENTE CON ESE DINERO
    if apuesta == 1: local = True
    #Buscar win or draw con el id del partido 
    FuncionPagaOQuita(billetera, dinero_apostado, local, win_or_draw)"""