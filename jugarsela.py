import requests
import os
import csv


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

def input_alfa() -> str:
    """
    PRE: -
    POST: Devuelve un valor alfabético, en minúsculas y sin tildes.
    """
    palabra = input("").lower()
    while palabra.isalpha() != True:
        palabra = input("El valor ingresado no es alfabético. Inténtelo nuevamente: ").lower()
    return palabra

def validador_num(valor:int, valores:list) -> int:
    """
    PRE: Ingresa un entero y una lista.
    POST: Devuelve el entero solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"\"{valor}\" es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_num()
    return valor

def validador_str(valor:str, valores:list) -> str:
    """
    PRE: Ingresa un string y una lista.
    POST: Devuelve el string solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"\"{valor}\" es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_alfa()
    return valor

def espacios_menu (nombre:str, dinero:str) -> int:
    cantidad_espacios = 33 - len(nombre) - len(dinero)
    
    if cantidad_espacios > 0:
        espacios = (" "*cantidad_espacios)
    else:
        espacios = ("\n")
    
    return espacios

def menu_principal(usuario) -> None:
    """
    PRE: -
    POST: Imprime el menú principal de la aplicación.
    """
    nombre = "MarianoRuenBladesMaldito"#[*usuario.values()][0][0]
    dinero = "5236"#[*usuario.values()][0][4]
    espacios = espacios_menu(nombre, dinero)
    os.system("cls")
    print("------------ MENU PRINCIPAL ------------")
    print(f"User: {nombre}{espacios}${dinero}")   #TO-DO: Agregar que mida el espacio entre "usuario" y "dinero", segun el "len()" de cada uno
    print("-"*40)
    print("a. Mostrar plantel completo de un equipo (temporada 2023).")
    print("b. Mostrar tabla para una temporada.")
    print("c. Consultar estadio y escudo de un equipo.")
    print("d. Gráficar goles y minutos de un equipo.")
    print("e. Cargar dinero en cuenta.")
    print("f. Mostrar Usuario que más dinero apostó.")
    print("g. Mostrar Usuario que más apuestas ganó.")
    print("h. Apostar.")
    print("i. Salir.")
    print("-"*40)

def posicion_jugador(pos:str) -> str:
    """
    PRE: Ingresa la posicion en la que juega el jugador (en inglés)
    POST: Devuelve la posicion pero en español. En caso de no coincidir con alguna de las 4 posiciones, devuelve la posición en ingles sin cambios.
    """
    if pos == "Attacker":
        pos = "Delantero"
    elif pos == "Defender":
        pos = "Defensor"
    elif pos == "Goalkeeper":
        pos = "Arquero"
    elif pos == "Midfielder":
        pos = "Mediocampista"
    
    return pos

def mostrar_plantel(dicc_equipos:dict) -> None:
    """
    PRE: Ingresan una lista de los equipos de la LPA y otra lista con sus respectivos IDs. 
    POST: Imprime el plantel de jugadores del equipo que indique el usuario.
    """
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]
    lista_opciones = []
    
    print("Equipos de la Liga Profesional Argentina:")
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    print("Ingrese de que equipo desea buscar su plantel: ", end="")
    equipo = validador_num(input_num(), lista_opciones)

    id_equipo = lista_equipos_ids[equipo-1]
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params ={"league":"128", "season": 2023, "team": id_equipo}
    url = "https://v3.football.api-sports.io/players"
    
    respuesta = requests.get(url, params=params, headers=headers).json()["response"]
    os.system("cls")
    
    print(f"Plantel de {lista_equipos[equipo-1]}:")
    for i in range(len(respuesta)):
        apellido = (respuesta[i]["player"]["lastname"]).split()
        nombre = (respuesta[i]["player"]["firstname"]).split()
        puntitos = "." * (32 - (len(apellido[0])+len(nombre[0])))
        posicion = posicion_jugador(respuesta[i]["statistics"][0]["games"]["position"])
        print("{} {}{}{}".format(apellido[0], nombre[0], puntitos, posicion))
    print("-"*40)

def mostrar_tabla() -> None:
    """
    PRE: -
    POST: Imprime la tabla de posiciones de la LPA del año que indique el usuario.
    """
    años_ligas = [2015,2016,2017,2018,2019,2020,2021,2022,2023]
    print("Temporadas de la Liga Profesional Argentina.")
    for año in años_ligas:
        print(f" - {año}")
    print("-"*20)
    print("Ingrese el año de la temporada que desea conocer: ", end="")
    año_liga = int(validador_num(input_num(), años_ligas))

    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params = {"league":"128", "season": año_liga}
    url = "https://v3.football.api-sports.io/standings"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"][0]["league"]["standings"][0]
    #STANDINGS[season][team]←indices de listas : ['rank', 'team', 'points', 'goalsDiff', 'group', 'form', 'status', 'description', 'all', 'home', 'away', 'update']
    os.system("cls")
    print(f"---- Liga Profesional Argentina {año_liga} ----")
    iterador = 0
    for equipo in respuesta:
        iterador += 1
        if iterador <= 9:
            puntitos = "." * (32 - len(equipo["team"]["name"]))
        else:
            puntitos = "." * (31 - len(equipo["team"]["name"]))
        
        print("{}. {}{}{}pts".format(equipo["rank"], equipo["team"]["name"], puntitos, equipo["points"]))
    print("-"*40)

def mostrar_estadio_y_escudo(dicc_equipos:dict):
    """
    PRE: Ingresan una lista de los equipos de la LPA y otra lista con sus respectivos IDs. 
    POST: Imprime información sobre el club que indique el usuario.
    """
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]    
    lista_opciones = []
    
    print("Equipos de la Liga Profesional Argentina:")
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    print("Ingrese el equipo del que desea obtener información sobre el estadio: ", end="")
    equipo_a_buscar = validador_num(input_num(), lista_opciones)

    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params ={"league":"128","season": 2023}
    url = "https://v3.football.api-sports.io/teams"

    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #team, venue["name", "address", "city", "capacity", " surface", "image"]
    os.system("cls")
    for i in range(len(respuesta)):
        if respuesta[i]["team"]["id"] == id_equipo_a_buscar:
            print(respuesta[i]["team"]["logo"])   #Ver si se puede imprimir el escudo en lugar de una url
            print("----" + respuesta[i]["team"]["name"].upper() + "----")
            print("Año de fundación:", respuesta[i]["team"]["founded"])
            print("País:", respuesta[i]["team"]["country"])
            print("Ciudad:", respuesta[i]["venue"]["city"])
            print("Dirección:", respuesta[i]["venue"]["address"])
            if respuesta[i]["venue"]["surface"] == "grass": print("Superficie: Césped")
            print("Estadio:", respuesta[i]["venue"]["name"])
            print("Capacidad:", respuesta[i]["venue"]["capacity"], "espectadores")
            #urlimagen = respuesta[i]["venue"]["image"]  #Ver si se puede imprimir la foto del estadio en lugar de una url
            #estadio = Image.open(requests.get(urlimagen, stream=True).raw)
            
            print("-"*40)

def MostrarFixture():
    numero_temporada = int(input("Ingrese numero de temporada para ver el fixture: "))
    numero_fecha = int(input("Ingrese numero de fecha para ver el fixture: "))
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params ={"league":"128","season": numero_temporada, "round": f"1st Phase - {numero_fecha}"}
    url = "https://v3.football.api-sports.io/fixtures"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]
    print(f"Fixture de la fecha {numero_fecha}:")
    print("-"*20)
    for i in range(14):
        print(respuesta[i]["teams"]["home"]["name"], "VS", respuesta[i]["teams"]["away"]["name"])
        print(respuesta[i]["goals"]["home"], "\t\t", respuesta[i]["goals"]["away"])
    print("-"*20)

def mostrar_grafico_goles(dicc_equipos:dict):
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]   
    lista_opciones = []
    años_ligas = [2015,2016,2017,2018,2019,2020,2021,2022,2023]
    print("Temporadas de la Liga Profesional Argentina:")
    for año in años_ligas:
        print(f" - {año}")
    print("-"*20)
    print("Ingrese el año de la temporada que desea conocer: ", end="")
    año_liga = (validador_num(input_num(), años_ligas))
    print("Equipos de la Liga Profesional Argentina:")
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    print("Ingrese de que equipo desea buscar sus estadísticas de goles: ", end="")
    equipo = (validador_num(input_num(), lista_opciones))

    id_equipo = (lista_equipos_ids[equipo-1])

    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
    params ={"league":128,"season":año_liga,"team":id_equipo}
    url = "https://v3.football.api-sports.io/teams/statistics"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"]["goals"]["for"]
    numeros_porcentajes= []
    porcentajes =[] #["0-15"],["16-30"],["31-45"],["46-60"],["61-75"],["76-90"],["91-105"],["106-120"] ej: ['31.58%', '10.53%', '10.53%', '15.79%', '10.53%', '15.79%', '5.26%', None]
    porcentajes_str = ""
    print("Goles a favor:", respuesta["total"]["total"])
    input("Presione enter para abrir el gráfico")
    for minutos in respuesta["minute"]:
        porcentajes.append(respuesta["minute"][minutos]["percentage"])
    for i in range(len(porcentajes)):
        if type(porcentajes[i]) is not str:
            porcentajes[i] = "0.00%"
    porcentajes_str = " ".join(porcentajes)
    porcentajes_str = porcentajes_str.replace("%", "")
    numeros_porcentajes = porcentajes_str.split()
    for i in range(len(numeros_porcentajes)):
        numeros_porcentajes[i] = float(numeros_porcentajes[i])

    plt.figure(figsize=(12, 8))
    x = ["Min 0 al 15", "Min 16 al 30", "Min 31 al 45", "Min 46 al 60", "Min 61 al 75", "Min 76 al 90", "Min 90 al 105", "Min 105 al 120"]
    y = numeros_porcentajes
    plt.xlabel("Minutos")
    plt.ylabel("Porcentaje de goles")
    plt.yticks(sorted(numeros_porcentajes))
    plt.title("PORCENTAJE GOLES A FAVOR\n TOTAL DE GOLES EN LA TEMPORADA {}: {}".format(año_liga, respuesta["total"]["total"]))
    plt.bar(x,y, linewidth=2, edgecolor="black")
    plt.show()

def mail_validado() -> str:
    os.system("cls")
    print("El mail debe cumplir las siguientes condiciones:\n - Formato: nombre_usuario@nombre_servicio_correo.com\n - \"nombre_usuario\" y \"nombre_servicio_correo\" no deben contener espacios ni\
 caracteres especiales.\n - Ejemplo: Leonel@gmail.com")
    print("-"*25)
    mail = input("Ingrese un mail: ")
    while len(mail) == 0:
        mail = input("Ingrese un mail: ")

    cantidad_puntos = mail.count(".")
    mail_spliteado:list = mail.split("@")

    if len(mail_spliteado) != 2:
        print("El mail debe contener una única \"arroba\"(@) para separar usuario del servicio de correo electrónico")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()
    if cantidad_puntos != 1:
        print("El mail debe contener un único \"punto\"(.) para poder finalizar con \".com\"")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()
    if mail_spliteado[1].count(".") == 0:
        print("El \"punto\"(.) del mail debe estar después de la \"arroba\"(@)")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()

    usuario, correo, com  = mail_spliteado[0], mail_spliteado[1].split(".")[0], mail_spliteado[1].split(".")[1]
    #condiciones (booleanos)
    cond1 = usuario.isalnum()
    cond2 = correo.isalnum()
    cond3 = com == "com"

    if cond1 != True or cond2 != True or cond3 != True:
        print(f"{mail} es un mail inválido.")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()

    return mail

def obtener_usuarios_existentes() -> dict:
    usuarios_existentes: dict = {}
    with open('usuarios.csv', newline='') as usuariosCsv:
        csvReader = csv.reader(usuariosCsv, delimiter = ",")
        next(csvReader)
        for row in csvReader:
            usuariosExistentes[row[0]] = [row[1],row[2],row[3],row[4], row[5]]
    return usuariosExistentes

def pedirDataInicioSesion() -> list:
    #Pido e-mail y contraseña.
    email: str = mail_validado()
    contrasena: str = input("Ingrese su contraseña: ")
    while contrasena == '':
        contrasena = input("Ingrese su contraseña: ")
    return [email, contrasena]

#Asume que existe un Usuario con el email
def obtener_usuario(email: str) -> dict:
    usuarios: dict = obtener_usuarios_existentes()
    for id in usuarios:
        if email == id:
            return {email: usuarios[id]}

#Asume que no existe un Usuario con el email
def crearNuevoUsuario(dataInicioSesion: list) -> None:
    usuariosExistentes: dict = obtenerUsuariosExistentes()
    print(usuariosExistentes)
    with open('usuarios.csv', 'w', newline='') as usuariosCsv:
        csvWriter = csv.writer(usuariosCsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(("ID Usuario", "Nombre Usuario", "Contraseña", "Dinero Apostado", "Fecha Última Apuesta", "Dinero Disponible"))
        for id in usuariosExistentes:
            csvWriter.writerow((id, usuariosExistentes[id][0], usuariosExistentes[id][1], usuariosExistentes[id][2], usuariosExistentes[id][3], usuariosExistentes[id][4]))
        csvWriter.writerow((dataInicioSesion[0], dataInicioSesion[2], dataInicioSesion[1], "0", "DDMMYYYY", "0"))

def crear_usuario() -> dict:                 #TO-DO: Agregar pregunta al usuario, si el mail existe... desea loguearse con el mismo?.
    #Busco Usuarios existentes
    usuariosExistentes: dict = obtenerUsuariosExistentes()
    #Pido usuario y contraseña
    dataInicioSesion: list = pedirDataInicioSesion()
    #Ver que no exista
    while dataInicioSesion[0] in usuariosExistentes.keys():
        print("El usuario ya existe. Intente con otro e-mail.")
        dataInicioSesion = pedirDataInicioSesion()
    #Pido nombre de usuario
    nombreDeUsuario: str = input("Ingrese su nombre de usuario: ")
    while nombreDeUsuario == "":
        nombreDeUsuario = input("Ingrese su nombre de usuario: ")
    dataInicioSesion.append(nombreDeUsuario)
    #Guardar Usuario en usuarios.csv
    crearNuevoUsuario(dataInicioSesion)
    return obtenerUsuario(dataInicioSesion[0])

def verificar_contrasena(contrasena_encriptada: str, contrasena_ingresada:str) -> bool:
    if(pbkdf2_sha256.verify(contrasena_ingresada, contrasena_encriptada)):
        return True
    return False

def ingresar_usuario() -> dict:                 #TO-DO: Agregar opcion de dejar al usuario volver para atras para registrar un mail.
    usuarios_existentes: dict = obtener_usuarios_existentes()
    #Pido usuario y contraseña
    data_inicio_sesion: list = pedir_data_inicio_sesion()
    #Ver que exista
    while data_inicio_sesion[0] not in usuarios_existentes.keys():
        print("El usuario no existe. Intente con otro e-mail.")
        data_inicio_sesion = pedir_data_inicio_sesion()
    #Chequeo contraseña
    while not verificar_contrasena(usuarios_existentes[data_inicio_sesion[0]][1], data_inicio_sesion[1]):
        print("La contraseña ingresada es incorrecta.")
        data_inicio_sesion[1] = input("Intente nuevamente: ")
    usuario: dict = usuarios_existentes[data_inicio_sesion[0]]
    
    os.system("cls")
    print(f"Bienvenido {usuario[0]}!")
    print(f"Tienes ${usuario[4]} disponible.")
    print("-"*20)
    input("Pulsa enter para ingresar al menú.")
    return obtener_usuario(data_inicio_sesion[0])

def iniciar_sesion() -> dict:
    print("-"*38)
    print("a. Iniciar sesión.\nb. Crear nuevo usuario.")
    print("-"*38)
    print("Indique que desea hacer: ", end = "")
    opcion: str = validador_str(input_alfa(), ["a","b"])
    
    os.system("cls")
    if(opcion == 'a'):
        usuario: dict = ingresar_usuario()
    if(opcion == 'b'):
        usuario: dict = crear_usuario()
    return usuario
>>>>>>> Stashed changes

def main() -> None:
    diccionario_equipos = {451: 'Boca JRS', 434: 'Gimnasia (LP)', 435: 'River Plate', 436: 'Racing Club', 437: 'Rosario Central', 438: 'Vélez Sarsfield', 439: 'Godoy cruz',
    440: 'Belgrano (Cba)', 441: 'Unión de Santa Fé', 442: 'Defensa y Justicia', 445: 'Huracán', 446: 'Lanús', 448: 'Colón de Santa Fé', 449: 'Banfield', 450: 'Estudiantes (LP)', 452: 'Tigre',
    453: 'Independiente', 455: 'Atlético Tucumán', 456: 'Talleres (Cba)', 457: 'Newells Old Boys', 458: 'Argentinos JRS', 459: 'Arsenal de Sarandí', 460: 'San Lorenzo', 474: 'Sarmiento (J)',
    478: 'Instituto (Cba)', 1064: 'Platense', 4065: 'Central Córdoba (SdE)', 2434: 'Barracas Central'}
    
    print("--------Bienvenido a Jugársela--------")
    input("Pulse Enter para iniciar la aplicación")
    #Login
    """usuario: dict = iniciarSesion()"""
    
    menu_principal(usuario)
    print("Ingrese una opción del menú: ", end="")
    opcion = validador_str(input_alfa(), ["a","b","c","d","e","f","g","h","i"])
    while opcion != 'i':
        os.system("cls")
        if(opcion == 'a'):
            mostrar_plantel(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'b'):
            mostrar_tabla()
            input("Pulse enter para continuar.")
        elif(opcion == 'c'):
            mostrar_estadio_y_escudo(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'd'):
            mostrar_grafico_goles(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'e'):
            cargarDinero()
        elif(opcion == 'f'):
            mostrarUsuarioQueMasAposto()
        elif(opcion == 'g'):
            mostrarUsuarioQueMasGano()
        elif(opcion == 'h'):
            apostar()
        
        menu_principal(usuario)
        opcion = validador_str(input_alfa(), ["a","b","c","d","e","f","g","h","i"])
    
    print("Saliste de la Aplicación")

main()

#Prueba