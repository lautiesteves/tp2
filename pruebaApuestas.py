import random
import requests


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
    lista_partidos = sorted(lista_partidos)
    
    print(f"El fixture de {dicc_equipos[id_equipo_a_buscar]} en este campeonato es:")
    print("------PRIMERA FASE------")
    centena_fase = 100
    for partido in lista_partidos:
        print(f"{partido[0]-centena_fase}-", partido[1], partido[2])
        if partido[0] == 127: 
            print("------SEGUNDA FASE------")
            centena_fase = 200
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
    FuncionPagaOQuita(billetera, dinero_apostado, local, win_or_draw)


MostrarFixture()


def FuncionPagaOQuita(billetera:float, plata_apostada:float, local:bool, win_or_draw:bool):   #No incluyo el partido porque entiendo que no nos interesa para saber cuanto gana, lo unico que nos interesa es saber si el win or draw es true y si se apuesta por el local
    dado = random.randint(1,3)
    ganancia = 3
    if win_or_draw: ganancia = 0,3
    if dado == 2:
        print(f"Ha habido un empate! Por lo que se añaden {plata_apostada*1.5}$ equivalentes a su apuesta mas su ganancia del 0.5 de lo que apostó")
        billetera += plata_apostada*1.5                    #Falta ver si se quita primero lo apostado y despues lo recupera o si se quita solo en caso de perder
    elif dado == 1:
        if local:
            print(f"Felicitacioness!! La apuesta ha sido un exito, ya puede encontrar su ganancia de {plata_apostada*ganancia} además de recuperar los {plata_apostada}$ apostados previamente.")
            billetera += plata_apostada*ganancia
        else:
            print("Lo sentimos. El ganador ha sido el local por lo que lamentablemente no se recupera lo apostado")
    elif dado == 3:
        if not local:
            print(f"Felicitacioness!! La apuesta ha sido un exito, ya puede encontrar su ganancia de {plata_apostada*ganancia} además de recuperar los {plata_apostada}$ apostados previamente.")
            billetera += plata_apostada*ganancia
        else:
            print("Lo sentimos. El ganador ha sido el visitante por lo que lamentablemente no se recupera lo apostado")


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