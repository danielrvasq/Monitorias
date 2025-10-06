'''
Desarrolla un programa en Python que permita gestionar las calificaciones de los estudiantes de una clase. El sistema debe permitir:

Registrar estudiantes y sus calificaciones en varias materias.
Mostrar la lista completa de estudiantes y sus calificaciones en formato de tabla.
Buscar estudiantes por nombre.
Calcular el promedio de cada estudiante y el promedio general de la clase.
Identificar y mostrar los estudiantes con mejor y peor desempeño.
Actualizar las calificaciones de un estudiante.
Eliminar estudiantes que hayan abandonado el curso.
Salir del sistema.
Utiliza listas y matrices para almacenar los datos, estructuras de control para la lógica y variables para la gestión de información.
El programa debe ser interactivo y mostrar mensajes claros al usuario.
'''

def mostrar_menu():
    print("\n--- Sistema de Gestión de Calificaciones ---")
    print("1. Registrar estudiante")
    print("2. Mostrar todos los estudiantes")
    print("3. Buscar estudiante por nombre")
    print("4. Calcular promedios")
    print("5. Mejor y peor desempeño")
    print("6. Actualizar calificaciones")
    print("7. Eliminar estudiante")
    print("8. Salir")

def registrar_estudiante(estudiantes, materias):
    nombre = input("Nombre del estudiante: ").strip()
    notas = []
    for materia in materias:
        while True:
            try:
                nota = float(input(f"Nota en {materia}: "))
                if 0 <= nota <= 10:
                    notas.append(nota)
                    break
                else:
                    print("La nota debe estar entre 0 y 10.")
            except ValueError:
                print("Introduce un número válido.")
    estudiantes.append([nombre, notas])
    print("Estudiante registrado correctamente.")

def mostrar_estudiantes(estudiantes, materias):
    print("\n{:<15}".format("Nombre"), end="")
    for materia in materias:
        print("{:<12}".format(materia), end="")
    print("{:<10}".format("Promedio"))
    print("-" * (15 + 12 * len(materias) + 10))
    for est in estudiantes:
        print("{:<15}".format(est[0]), end="")
        for nota in est[1]:
            print("{:<12}".format(nota), end="")
        promedio = sum(est[1]) / len(est[1])
        print("{:<10.2f}".format(promedio))

def buscar_estudiante(estudiantes):
    nombre = input("Nombre a buscar: ").strip().lower()
    encontrados = [est for est in estudiantes if nombre in est[0].lower()]
    if encontrados:
        print("\nEstudiantes encontrados:")
        for est in encontrados:
            print(f"{est[0]} - Notas: {est[1]}")
    else:
        print("No se encontró ningún estudiante con ese nombre.")

def calcular_promedios(estudiantes):
    print("\nPromedios individuales:")
    for est in estudiantes:
        promedio = sum(est[1]) / len(est[1])
        print(f"{est[0]}: {promedio:.2f}")
    if estudiantes:
        promedio_general = sum([sum(est[1]) / len(est[1]) for est in estudiantes]) / len(estudiantes)
        print(f"\nPromedio general de la clase: {promedio_general:.2f}")
    else:
        print("No hay estudiantes registrados.")

def mejor_peor_desempeno(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    promedios = [(est[0], sum(est[1]) / len(est[1])) for est in estudiantes]
    mejor = max(promedios, key=lambda x: x[1])
    peor = min(promedios, key=lambda x: x[1])
    print(f"\nMejor desempeño: {mejor[0]} con promedio {mejor[1]:.2f}")
    print(f"Peor desempeño: {peor[0]} con promedio {peor[1]:.2f}")

def actualizar_calificaciones(estudiantes, materias):
    nombre = input("Nombre del estudiante a actualizar: ").strip().lower()
    for est in estudiantes:
        if nombre == est[0].lower():
            print(f"Notas actuales de {est[0]}: {est[1]}")
            for i, materia in enumerate(materias):
                while True:
                    try:
                        nota = float(input(f"Nueva nota en {materia} (actual: {est[1][i]}): "))
                        if 0 <= nota <= 10:
                            est[1][i] = nota
                            break
                        else:
                            print("La nota debe estar entre 0 y 10.")
                    except ValueError:
                        print("Introduce un número válido.")
            print("Calificaciones actualizadas.")
            return
    print("Estudiante no encontrado.")

def eliminar_estudiante(estudiantes):
    nombre = input("Nombre del estudiante a eliminar: ").strip().lower()
    for i, est in enumerate(estudiantes):
        if nombre == est[0].lower():
            estudiantes.pop(i)
            print("Estudiante eliminado.")
            return
    print("Estudiante no encontrado.")

def main():
    materias = ["Matemáticas", "Lengua", "Ciencias"]
    estudiantes = []
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_estudiante(estudiantes, materias)
        elif opcion == "2":
            mostrar_estudiantes(estudiantes, materias)
        elif opcion == "3":
            buscar_estudiante(estudiantes)
        elif opcion == "4":
            calcular_promedios(estudiantes)
        elif opcion == "5":
            mejor_peor_desempeno(estudiantes)
        elif opcion == "6":
            actualizar_calificaciones(estudiantes, materias)
        elif opcion == "7":
            eliminar_estudiante(estudiantes)
        elif opcion == "8":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()