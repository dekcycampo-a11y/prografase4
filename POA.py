# Problema 5: Registro de horas trabajadas

# Crear la matriz de recursos
matriz = []

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

# Registrar los datos de 4 recursos
for i in range(4):
    print("\nRegistro del recurso", i + 1)
    nombre = input("Ingrese el nombre de la persona: ")

    fila = [nombre]

    for dia in dias:
        horas = float(input("Ingrese las horas trabajadas el " + dia + ": "))
        fila.append(horas)

    matriz.append(fila)


# Funcion para calcular y clasificar las horas
def calcular_jornada(matriz):

    print("\n===== REPORTE SEMANAL DE HORAS =====")

    for recurso in matriz:
        nombre = recurso[0]

        # Calcular total de horas semanales
        total = sum(recurso[1:])

        # Clasificar la jornada laboral
        if total > 40:
            clasificacion = "Sobret iempo"
        else:
            clasificacion = "Horario estandar"

        # Mostrar resultados
        print("\nNombre:", nombre)
        print("Total de horas semanales:", total)
        print("Clasificacion:", clasificacion)


# Llamar a la funcion
calcular_jornada(matriz)