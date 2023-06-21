import random
import requests
import csv

def obtener_fixture() -> dict:
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params = {"league":"128","season": 2023}
    url = "https://v3.football.api-sports.io/fixtures"
    return requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]

def obtener_lista_partidos(respuesta, id_equipo_a_buscar) -> list:
    lista_partidos = []
    for i in range(len(respuesta)):
        if id_equipo_a_buscar == respuesta[i]["teams"]["home"]["id"]:
            print(respuesta[i]["league"]["round"])
            ronda = str(respuesta[i]["league"]["round"])
            if len(ronda)==14:
                numero_fecha = int(ronda[0] + ronda[12] + ronda[13])
            else: numero_fecha = int(ronda[0] + "0" + ronda[12])
            lista_partidos.append([numero_fecha, respuesta[i]["teams"]["away"]["name"], "(L)", respuesta[i]["fixture"]["id"]])
        elif id_equipo_a_buscar == respuesta[i]["teams"]["away"]["id"]:
            ronda = str(respuesta[i]["league"]["round"])
            if len(ronda)==14:
                numero_fecha = int(ronda[0] + ronda[12] + ronda[13])
            else:
                numero_fecha = int(ronda[0] + "0" + ronda[12])
            lista_partidos.append([numero_fecha, respuesta[i]["teams"]["home"]["name"], "(V)", respuesta[i]["fixture"]["id"]])
    return sorted(lista_partidos)

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

def elije_partido(dinero_disponible_usuario, dicc_equipos, lista_partidos, id_equipo):
    #Imprimo Fixture
    print(f"El fixture de {dicc_equipos[id_equipo]} en este campeonato es:")
    print("------PRIMERA FASE------")
    centena_fase = 100
    for partido in lista_partidos:
        print(f"{partido[0]-centena_fase}-", partido[1], partido[2])
        if partido[0] == 127: 
            print("------SEGUNDA FASE------")
            centena_fase = 200
    #Pido Partido a apostar
    print("Si desea aostar a un partido de la primera fase escriba ´1´ y si desea apostar para uno de la segunda fase escriba ´2´")
    fase = validador_num(input_num())
    if fase ==1: centena_fase = 100 #No pongo el caso de que sea 2 ya que centena fase ya vale 200 desde el for anterior
    print("Escriba el número del partido en el cual quiere realizar su apuesta: ", end="")
    partido_a_apostar = input_num() + centena_fase
    while not(partido_a_apostar>100 and partido_a_apostar<127) and not(partido_a_apostar>200 and partido_a_apostar<214) and (partido_a_apostar - centena_fase)<27:
        #Chequeo que el partido este en los intervalos de partidos de cada fase (primera fase tiene 27 partidos y segunda fase  14)
        #Tambien chequeo que el ingreso del usuario no sea lo suficientemente mayor como para entrar en el rango de la segunda fase si pone por ejemplo primera fase y partido 110
        print("Ingreso inválido. Ingrese uno de los numeros colocados entre las opciones antes mostradas: ", end="")
        partido_a_apostar = input_num()
        partido_a_apostar += centena_fase #Sumo 100 o 200 para saber a que fase quiere apostar el usuario y poder buscar el partido correcto (De ultima podemos sacar lo de las fases porque puede ser un quilombo)
    #Busca id del partido a apostar
    id_partido = busca_id_partido(lista_partidos, partido_a_apostar)
    #Pido a que equipo desea apostar
    print("En caso de querer apostar por el local ingrese 1, en caso de apostar por un empate ingrese 2, y en caso de apostar por el visitante ingrese 3 \n")
    apuesta = validador_num(input_num(), [1,2,3])
    #VALIDAR EL INGRESO DEL USUARIO
    print("Escriba la cantidad de dinero que desea apostar: ", end="")
    dinero_apostado = input_num()
    #Validar que el usuario cuente con ese dinero
    while dinero_apostado > dinero_disponible_usuario:
        print(f"No cuenta con esa cantidad de dinero en la cuenta. Su plata actual es {dinero_disponible_usuario}.\nIngresé su apuesta: ", end="")
        dinero_apostado = input_num()
    return dinero_apostado, apuesta, id_partido

def busca_id_partido(lista_partidos, partido_apostado):
    if partido_apostado<200: 
        fase = "1st"
        partido_apostado -= 100
    else: 
        fase = "2nd"
        partido_apostado -= 200
    for i in lista_partidos:
        if i[0] == f"{fase} Phase - {partido_apostado}":
            return i[2]

def main_apuestas(): #abierto a cambio de nombre, lo cambie para que no sea parecido a una variable
    dicc_equipos = {451: 'Boca JRS', 434: 'Gimnasia (LP)', 435: 'River Plate', 436: 'Racing Club', 437: 'Rosario Central', 438: 'Vélez Sarsfield', 439: 'Godoy cruz',
    440: 'Belgrano (Cba)', 441: 'Unión de Santa Fé', 442: 'Defensa y Justicia', 445: 'Huracán', 446: 'Lanús', 448: 'Colón de Santa Fé', 449: 'Banfield', 450: 'Estudiantes (LP)', 452: 'Tigre',
    453: 'Independiente', 455: 'Atlético Tucumán', 456: 'Talleres (Cba)', 457: 'Newells Old Boys', 458: 'Argentinos JRS', 459: 'Arsenal de Sarandí', 460: 'San Lorenzo', 474: 'Sarmiento (J)',
    478: 'Instituto (Cba)', 1064: 'Platense', 4065: 'Central Córdoba (SdE)', 2434: 'Barracas Central'}
    usuario = {'prueba@gmail.com': ['Prueba', '$pbkdf2-sha256$29000$ZGxN6Z2zdi5lrPVeS6l1bg$Mq3DdwiQoYcOoZLHF.nYBb5vIMWs8dK3RqCE5zXiajQ', '120', 'DDMMYYYY', '290']}
    dinero_disponible_usuario: float = float([*usuario.values()][0][4])
    lista_partidos, id_equipo = busca_fixture(dicc_equipos)
    print(id_equipo)
    dinero_apostado, apuesta, id_partido = elije_partido(dinero_disponible_usuario, dicc_equipos, lista_partidos, id_equipo)
    win_or_draw:bool = obtener_win_or_draw(id_partido, apuesta)
    #TO-DO Buscar win or draw con el id del partido y ver si la apuesta coincide con el win or draw
    ganancia = resolver_apuesta(dinero_apostado, apuesta, win_or_draw)
    cargar_dinero(usuario, ganancia)
    if(ganancia > 0):
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Gana", str(ganancia))
    else:
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Pierde", str(ganancia))

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