#Definición de lista

nombre_de_la_lista = []

otra_lista = list()

#------------------------------------------------------------------------------------------
#Definir lista con elementos

lista_con_elementos = [1, 2, True, 'Hola', 5.8]
otra_lista_con_elementos = list([4, 9, False, 'texto'])

#------------------------------------------------------------------------------------------
#Mostrar elementos de una lista
print("Mostrar elementos de una lista")
mi_lista = ['Juan', 'Pedro', 'Laura', 'Carmen', 'Susana']
print(mi_lista[0]) # Muestra Juan (la primera posición es la 0)
print(mi_lista[-1]) # Muestra Susana
print(mi_lista[1]) # Muestra Pedro
print(mi_lista[2]) # Muestra Laura
print(mi_lista[-2]) # Muestra Carmen

#------------------------------------------------------------------------------------------
#Formas de recorrer una lista

print("Formas de recorrer una lista")
edades = [20, 41, 6, 18, 23]

# Recorriendo los elementos
for edad in edades:
    print(edad)

# Recorriendo los índices
for i in range(len(edades)):
    print(edades[i])

# Con while y los índices
indice = 0

while indice < len(edades):
    print(edades[indice])
    indice += 1

#------------------------------------------------------------------------------------------
#Agregar elementos a una lista vacia con append

print("Agregar elementos a una lista vacia con append")
números = []
números.append(10)
números.append(5)
números.append(3)
print(números)
# Mostrará [10, 5, 3]

#------------------------------------------------------------------------------------------
#Sumar dos listas
print("Sumar dos listas")
números = []
# Unimos la lista anterior con una nueva
números = números + [10, 5, 3]
print(números)
# Mostrará [10, 5, 3]

#------------------------------------------------------------------------------------------
#Eliminar elementos de una lista con pop

print("Eliminar elementos de una lista con pop")
palabras = ['hola', 'hello', 'ola']
palabras.pop(1)
print(palabras)
# Mostrará ['hola', 'ola']

#------------------------------------------------------------------------------------------
#eliminar un elemento de una lista con remove

print("eliminar un elemento de una lista con remove")
palabras = ['hola', 'hello', 'hello', 'ola']
palabras.remove('hello')
print(palabras)
# Mostrará ['hola', 'hello', 'ola']

#------------------------------------------------------------------------------------------
#ejemplo practico

print("Ejemplo Practico")
# Creamos las listas (vacías al comienzo)
nombres = []
identificaciones = []
# Definimos un tamaño para las listas
# Lo puedes cambiar si quieres
tamaño = 3

# Leemos los datos y los agregamos a la lista
for i in range(tamaño):
    print("Ingrese los datos de la persona", i + 1)
    nombre = input("Nombre: ")
    identificación = input("Identificación: ")

    nombres.append(nombre)
    identificaciones.append(identificación)

# Ahora mostremos las listas
for i in range(tamaño):
    print("Mostrando los datos de la persona", i + 1)

    print("Nombre:", nombres[i])
    print("Identificación:", identificaciones[i])

print(nombres)
print(identificaciones)

#------------------------------------------------------------------------------------------
#ejemplo practico

print("Ejemplo pracico 2")  

numeros = []  # lista vacía

# Pedir 3 números al usuario y guardarlos en la lista
for i in range(3):
    num = int(input(f"Ingrese el número {i+1}: "))
    numeros.append(num)

# Mostrar los números ingresados
print("\nNúmeros ingresados:", numeros)

# Número mayor
print("El número más grande es:", max(numeros))

# Promedio
promedio = sum(numeros) / len(numeros)
print("El promedio es:", promedio)

#---------------------------------------------------------------
#Matrices

matriz = [[1,2,3],
          [4,5,6],
          [7,8,9]]

print(matriz[0][2])

for row in matriz:
    for element in row:
        print(element)

