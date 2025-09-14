'''
Escribir un programa que almacene las asignaturas de un curso 
(por ejemplo Matemáticas, Física, Química, Historia y Lengua) en una lista, 
pregunte al usuario la nota que ha sacado en cada asignatura, y después las muestre por 
pantalla con el mensaje En<asignatura> has sacado <nota> donde <asignatura> es cada una des las asignaturas 
de la lista y <nota> cada una de las correspondientes notas introducidas por el usuario.

'''
def pedirMaterias():
    materias = []
    cantidad = int(input("¿Cuántas materias viste este semestre?: "))

    for i in range(cantidad):
        materia = input(f"Ingrese el nombre de la materia {i+1}: ")
        materias.append(materia)

    return materias

def pedirNotas(materias):
    notas = []
    for materia in materias:
        nota = input(f"Ingrese la nota para {materia}: ")
        notas.append(nota)
    return notas

def mostrarResultados(materias, notas):
    for materia, nota in zip(materias, notas):
        print(f"En {materia} has sacado {nota}")

def main():
    materias = pedirMaterias()
    notas = pedirNotas(materias)
    mostrarResultados(materias, notas)

main()