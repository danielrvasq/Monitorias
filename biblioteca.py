class Libro:
    def __init__(self, titulo, autor, anio, isbn, cantidad):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.isbn = isbn
        self.cantidad = cantidad
        self.prestados = 0

    def __str__(self):
        return f"{self.titulo} ({self.autor}, {self.anio}) - Disp: {self.cantidad - self.prestados}"

class Usuario:
    def __init__(self, nombre, codigo, tipo):
        self.nombre = nombre
        self.codigo = codigo
        self.tipo = tipo
        self.prestamos = []

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - Préstamos activos: {len(self.prestamos)}"

class Prestamo:
    def __init__(self, usuario, libro):
        self.usuario = usuario
        self.libro = libro

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.prestamos = []

    # ---------- LIBROS ----------
    def agregar_libro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        anio = input("Año: ")
        isbn = input("ISBN: ")
        cantidad = int(input("Cantidad disponible: "))
        self.libros.append(Libro(titulo, autor, anio, isbn, cantidad))
        print("✅ Libro registrado con éxito.\n")

    def listar_libros(self):
        if not self.libros:
            print("No hay libros registrados.\n")
            return
        print("\n📚 Lista de libros:")
        for i, libro in enumerate(self.libros, 1):
            print(f"{i}. {libro}")
        print()

    def buscar_libro(self):
        termino = input("Buscar por título o autor: ").lower()
        encontrados = [l for l in self.libros if termino in l.titulo.lower() or termino in l.autor.lower()]
        if encontrados:
            for l in encontrados:
                print(l)
        else:
            print("No se encontraron coincidencias.\n")

    # ---------- USUARIOS ----------
    def registrar_usuario(self):
        nombre = input("Nombre: ")
        codigo = input("Código: ")
        tipo = input("Tipo (estudiante/profesor): ").lower()
        self.usuarios.append(Usuario(nombre, codigo, tipo))
        print("✅ Usuario registrado con éxito.\n")

    def listar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios registrados.\n")
            return
        print("\n👥 Lista de usuarios:")
        for u in self.usuarios:
            print(u)
        print()

    # ---------- PRÉSTAMOS ----------
    def prestar_libro(self):
        codigo = input("Código del usuario: ")
        usuario = next((u for u in self.usuarios if u.codigo == codigo), None)
        if not usuario:
            print("Usuario no encontrado.\n")
            return

        if len(usuario.prestamos) >= 3:
            print("❌ Este usuario ya tiene 3 préstamos activos.\n")
            return

        self.listar_libros()
        isbn = input("Ingrese ISBN del libro a prestar: ")
        libro = next((l for l in self.libros if l.isbn == isbn), None)
        if not libro:
            print("Libro no encontrado.\n")
            return

        if libro.prestados >= libro.cantidad:
            print("❌ No hay ejemplares disponibles.\n")
            return

        libro.prestados += 1
        prestamo = Prestamo(usuario, libro)
        usuario.prestamos.append(prestamo)
        self.prestamos.append(prestamo)
        print("✅ Préstamo realizado con éxito.\n")

    def devolver_libro(self):
        codigo = input("Código del usuario: ")
        usuario = next((u for u in self.usuarios if u.codigo == codigo), None)
        if not usuario:
            print("Usuario no encontrado.\n")
            return

        if not usuario.prestamos:
            print("Este usuario no tiene préstamos activos.\n")
            return

        print("\n📚 Libros prestados:")
        for i, p in enumerate(usuario.prestamos, 1):
            print(f"{i}. {p.libro.titulo}")

        indice = int(input("Seleccione el número del libro a devolver: ")) - 1
        prestamo = usuario.prestamos.pop(indice)
        prestamo.libro.prestados -= 1
        self.prestamos.remove(prestamo)
        print("✅ Libro devuelto con éxito.\n")

    # ---------- REPORTES ----------
    def reporte_libros_prestados(self):
        if not self.prestamos:
            print("No hay libros prestados actualmente.\n")
            return
        print("\n📖 Libros actualmente prestados:")
        for p in self.prestamos:
            print(f"- {p.libro.titulo} → {p.usuario.nombre}")
        print()

    def reporte_top_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios registrados.\n")
            return
        top = sorted(self.usuarios, key=lambda u: len(u.prestamos), reverse=True)
        print("\n🏅 Usuarios con más préstamos:")
        for u in top:
            print(f"{u.nombre}: {len(u.prestamos)} préstamos")
        print()

    # ---------- MENÚ ----------
    def menu(self):
        while True:
            print("=== SISTEMA DE BIBLIOTECA ===")
            print("1. Registrar libro")
            print("2. Listar libros")
            print("3. Buscar libro")
            print("4. Registrar usuario")
            print("5. Listar usuarios")
            print("6. Prestar libro")
            print("7. Devolver libro")
            print("8. Reporte de libros prestados")
            print("9. Reporte top de usuarios")
            print("0. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.agregar_libro()
            elif opcion == "2":
                self.listar_libros()
            elif opcion == "3":
                self.buscar_libro()
            elif opcion == "4":
                self.registrar_usuario()
            elif opcion == "5":
                self.listar_usuarios()
            elif opcion == "6":
                self.prestar_libro()
            elif opcion == "7":
                self.devolver_libro()
            elif opcion == "8":
                self.reporte_libros_prestados()
            elif opcion == "9":
                self.reporte_top_usuarios()
            elif opcion == "0":
                print("👋 Saliendo del sistema...")
                break
            else:
                print("Opción inválida.\n")


# ---------- EJECUCIÓN ----------
if __name__ == "__main__":
    biblioteca = Biblioteca()
    biblioteca.menu()
 