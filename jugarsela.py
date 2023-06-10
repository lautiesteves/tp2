def main() -> None:
    print("Jugársela")
    #Login
    usuario: dict = iniciarSesion()
    #Menu
    opcion: str = ingresarOpcion()
    while opcion != 'i':
        if(opcion == 'a'):
            mostrarPlantel()
        if(opcion == 'b'):
            mostrarTabla()
        if(opcion == 'c'):
            mostrarEstadioYEscudo()
        if(opcion == 'd'):
            mostrarGraficoDeGoles()
        if(opcion == 'e'):
            cargarDinero()
        if(opcion == 'f'):
            mostrarUsuarioQueMasAposto()
        if(opcion == 'g'):
            mostrarUsuarioQueMasGano()
        if(opcion == 'h'):
            apostar()

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

main()