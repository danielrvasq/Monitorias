def suma_filas(matrix):
    """Devuelve la suma de cada fila en matrix (lista de listas)."""
    return [sum(row) for row in matrix]

def suma_columnas(matrix):
    """Devuelve la suma de cada columna en matrix (lista de listas)."""
    if not matrix:
        return []
    # Validar que la matriz sea rectangular (todas las filas misma longitud)
    cols = len(matrix[0])
    for r in matrix:
        if len(r) != cols:
            raise ValueError("La matriz no es rectangular: filas con longitudes diferentes")
    col_sums = [0] * cols
    for row in matrix:
        for j, val in enumerate(row):
            col_sums[j] += val
    return col_sums

def max_con_pos(matrix):
    """Devuelve el valor máximo en matrix y su posición (fila, columna)."""
    if not matrix or not matrix[0]:
        raise ValueError("Matriz vacía")
    max_val = matrix[0][0]
    pos = (0,0)
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val > max_val:
                max_val = val
                pos = (i,j)
    return max_val, pos

def transponer(matrix):
    """Devuelve la transpuesta de la matriz dada."""
    if not matrix:
        return []
    # Validar rectangularidad
    cols = len(matrix[0])
    for r in matrix:
        if len(r) != cols:
            raise ValueError("La matriz no es rectangular: no se puede transponer de forma segura")
    # usar zip para claridad
    return [list(row) for row in zip(*matrix)]

def rotar_90(matrix):
    # rotación = transponer y luego invertir cada fila
    t = transponer(matrix)
    return [list(reversed(row)) for row in t]

def matriz_mul(A, B):
    # A: m x p, B: p x n
    if not A or not B:
        raise ValueError("A y B deben ser matrices no vacías")
    m = len(A)
    p = len(A[0])
    # validar rectangularidad de A y B
    for r in A:
        if len(r) != p:
            raise ValueError("La matriz A no es rectangular")
    if any(len(r) != len(B[0]) for r in B):
        # B puede tener filas uniformes pero comprobamos la longitud de la primera fila
        pass
    if len(B) != p:
        raise ValueError("Dimensiones inválidas para multiplicar: columnas de A != filas de B")
    n = len(B[0])
    for r in B:
        if len(r) != n:
            raise ValueError("La matriz B no es rectangular")
    # Inicializar resultado m x n
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for k in range(p):
            a = A[i][k]
            for j in range(n):
                C[i][j] += a * B[k][j]
    return C

def max_path_sum(matrix):
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    # validar rectangularidad
    for r in matrix:
        if len(r) != n:
            raise ValueError("La matriz no es rectangular")
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = matrix[0][0]
    # primera fila
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + matrix[0][j]
    # primera columna
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + matrix[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + matrix[i][j]
    return dp[m-1][n-1]

def max_subarray_1d(arr):
    if not arr:
        raise ValueError("Arreglo vacío")
    max_ending = max_so_far = arr[0]
    for x in arr[1:]:
        max_ending = max(x, max_ending + x)
        max_so_far = max(max_so_far, max_ending)
    return max_so_far

def max_submatrix_sum(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    best = float('-inf')
    # fijar columnas izquierda y derecha
    for left in range(cols):
        tmp = [0]*rows
        for right in range(left, cols):

            for r in range(rows):
                tmp[r] += matrix[r][right]
            current_max = max_subarray_1d(tmp)
            best = max(best, current_max)
    return best

