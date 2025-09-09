"""
Material de apoyo: Operadores Aritméticos, Lógicos y Estructuras de Control en Python
Autor: Daniel Rueda Vásquez (monitoría)
Descripción:
- Este archivo contiene ejemplos comentados en el MISMO orden y con el MISMO alcance
  que el documento "Operadores Aritméticos, Lógicos y Estructuras de Control en Python".
- Solo se muestran conceptos tratados en el documento: operadores aritméticos y lógicos,
  idea general de estructuras de control, secuencia, condicional (if / if-else) y ciclos
  (while, do-while -como patrón- y for).
- Las demostraciones posteriores usan únicamente conceptos ya ilustrados previamente
  (por ejemplo, un if que combina operadores lógicos y relacionales se apoya en los
  ejemplos de operadores lógicos anteriores).
"""

print("=== 1) OPERADORES ARITMÉTICOS ===")
a, b = 10, 3

# Suma (+): suma dos operandos
suma = a + b  # 10 + 3 = 13
print("Suma (+):", suma)

# Resta (-): resta; como unario, cambia el signo
resta = a - b  # 10 - 3 = 7
print("Resta (-):", resta)
negativo_de_a = -a  # unario: cambia el signo de 'a' -> -10
print("Unario (-a):", negativo_de_a)

# Multiplicación (*): producto de dos operandos
producto = a * b  # 10 * 3 = 30
print("Multiplicación (*):", producto)

# División (/): siempre produce float
division = a / b  # 10 / 3 = 3.333...
print("División (/):", division)

# Módulo (%): resto de la división entera
modulo = a % b   # 10 % 3 = 1
print("Módulo (%):", modulo)

# División entera (//): cociente entero de la división
cociente_entero = a // b  # 10 // 3 = 3
print("División entera (//):", cociente_entero)

# Potencia (**): exponente
potencia = a ** b  # 10 ** 3 = 1000
print("Potencia (**):", potencia)


print("\n=== 2) OPERADORES LÓGICOS ===")
# AND, OR, NOT se usan sobre operandos booleanos (True/False).

# Relacionales de apoyo (mencionados en el documento como parte de las expresiones de prueba):
x, y = 5, 8
es_mayor = y > x        # True, porque 8 > 5
es_par = (y % 2) == 0   # True, 8 % 2 == 0

print("Relacional (>), (==) con módulo previo:", es_mayor, es_par)

# AND: verdadero si AMBAS condiciones son verdaderas
exp_and = es_mayor and es_par  # True and True -> True
print("AND:", exp_and)

# OR: verdadero si AL MENOS una condición es verdadera
exp_or = es_mayor or (x % 2 == 0)  # True or False -> True
print("OR:", exp_or)

# NOT: invierte el valor lógico
exp_not = not es_par  # not True -> False
print("NOT:", exp_not)

# Precedencia: operadores relacionales se evalúan antes que los lógicos
# Ejemplo: (3 < 7) and (10 % 2 == 0) -> True and True -> True
precedencia = (3 < 7) and (10 % 2 == 0)
print("Precedencia relacionales -> lógicos:", precedencia)


print("\n=== 3) ¿QUÉ SON LAS ESTRUCTURAS DE CONTROL? ===")
# Concepto (comentario):
# Las estructuras de control determinan el orden/flujo en que se ejecutan las instrucciones
# de un algoritmo: secuencia, bifurcación condicional y ciclo.


print("\n=== 4) SECUENCIA ===")
# En secuencia, las instrucciones se ejecutan una tras otra en el orden escrito.
n = 2
n = n + 3    # operación 1: ahora n = 5
m = n * 4    # operación 2: ahora m = 20
print("Secuencia -> n:", n, "| m:", m)


print("\n=== 5) PYTHON Y LAS SENTENCIAS CONDICIONALES (visión general) ===")
# Comentario:
# Las sentencias condicionales ejecutan un bloque si una condición es verdadera (o no).
# Se apoyan en expresiones booleanas como las vistas en la sección de operadores lógicos.


print("\n=== 6) SENTENCIA IF ===")
# IF ejecuta su bloque solo si la condición es verdadera.
edad = 20
tiene_documento = True
if (edad >= 18) and tiene_documento:  # Usa relacional + AND ya ejemplificados
    print("Acceso permitido (mayor de edad y con documento).")


print("\n=== 7) SENTENCIA IF-ELSE ===")
# IF-ELSE permite definir acciones para el caso verdadero y para el falso.
numero = 7
if (numero % 2) == 0:  # condición: paridad (usa módulo y == ya vistos)
    print(numero, "es par")
else:
    print(numero, "es impar")


print("\n=== 8) CONDICIONAL (if – else): bifurcación de dos alternativas ===")
# Elegir entre dos opciones según la condición.
a, b = 12, 15
if a > b:
    mayor = a
else:
    mayor = b
print("El mayor entre", a, "y", b, "es:", mayor)


print("\n=== 9) CICLOS (visión general) ===")
# Comentario:
# Un ciclo permite repetir una operación varias veces mientras se cumpla una condición
# o durante un rango de valores.


print("\n=== 10) CICLO MIENTRAS (while) ===")
# 'while' verifica la condición ANTES de cada iteración.
contador = 0
while contador < 3:  # se repetirá mientras la condición sea verdadera
    print("while -> iteración", contador)
    contador = contador + 1  # incremento unitario


print("\n=== 11) CICLO HACER-MIENTRAS (do-while, patrón en Python) ===")
# Python no tiene 'do-while' nativo. Para reproducir el COMPORTAMIENTO "hacer y luego comprobar",
# usamos un patrón que garantiza al menos una ejecución del cuerpo.
# Evitamos 'break' para mantenernos dentro del alcance mínimo del documento y
# reutilizamos OR lógico para el "al menos una vez".

primera_vez = True
valor = -2
limite = 1

# Se ejecuta al menos una vez; luego continúa mientras 'valor < limite'.
while primera_vez or (valor < limite):
    print("do-while (patrón) -> valor actual:", valor)
    # cuerpo del ciclo: aplicamos una operación simple
    valor = valor + 1  # incremento unitario
    # Tras la primera iteración, desactivamos el "gatillo" de primera vez
    primera_vez = False


print("\n=== 12) CICLO FOR ===")
# 'for' recorre una secuencia de valores. Para un contador con incremento unitario desde
# un valor inicial hasta un valor final INCLUSIVO, usamos range(inicio, fin+1).
inicio, fin = 1, 5
for i in range(inicio, fin + 1):
    print("for -> i =", i)
# Nota: range(inicio, fin) excluye 'fin'; por eso se usa 'fin + 1' para incluirlo.
