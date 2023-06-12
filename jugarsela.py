import requests

def main() -> None:
    print("Jugársela")
    #Login
    #usuario: dict = iniciarSesion()
    #Menu
    opcion: str = ingresarOpcion()
    while opcion != 'i':
        if(opcion == 'a'):
            MostrarPlantel()
            input("Enter para continuar")
        elif(opcion == 'b'):
            mostrarTabla()
        elif(opcion == 'c'):
            mostrarEstadioYEscudo()
        elif(opcion == 'd'):
            mostrarGraficoDeGoles()
        elif(opcion == 'e'):
            cargarDinero()
        elif(opcion == 'f'):
            mostrarUsuarioQueMasAposto()
        elif(opcion == 'g'):
            mostrarUsuarioQueMasGano()
        elif(opcion == 'h'):
            apostar()
        opcion: str = ingresarOpcion()

def imprimirOpciones() -> None:
    print("-"*15)
    print("Opciones:")
    print("a. Mostrar plantel completo de un equipo (temporada 2023).")
    print("b. Mostrar tabla para una temporada.")
    print("c. Consultar estadio y escudo de un equipo.")
    print("d. Gráficar goles y minutos de un equipo.")
    print("e. Cargar dinero en cuenta.")
    print("f. Mostrar Usuario que más dinero apostó.")
    print("g. Mostrar Usuario que más apuestas ganó.")
    print("h. Apostar.")
    print("i. Salir")
    print("-"*15)

def validarOpcion(opcion: str) -> bool:
    return opcion in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] 

def ingresarOpcion() -> str:
    imprimirOpciones()
    opcion: str = input("Ingrese una opción: ")
    while not validarOpcion(opcion):
        opcion = input(f"'{opcion}' no es una opción válida. Por favor seleccione una opción válida: ")
    return opcion

def MostrarPlantel():
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
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "06a1ef31a4553ae29d102396d964a20f"}
    params ={"league":"128", "season": 2022, "team": id_equipo}
    url = "https://v3.football.api-sports.io/players"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"]

    for i in range(len(respuesta)):
        print(respuesta[i]["player"]["name"])


main()