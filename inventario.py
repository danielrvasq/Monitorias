import tkinter as tk
from tkinter import ttk, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Inventario (Login simulado)")
        self.geometry("820x520")
        self.minsize(820, 520)

        # Sesión simulada y almacenamiento en memoria
        self.session = {"user": None}
        self.inventory = []  # lista de dicts: {"id": int, "nombre": str, "cantidad": int, "precio": float}
        self._next_id = 1

        # Frames
        self.login_frame = LoginFrame(self)
        self.inventory_frame = InventoryFrame(self)

        self.show_login()

        # Datos de ejemplo
        self._seed_data()

    def _seed_data(self):
        ejemplos = [
            {"nombre": "Teclado", "cantidad": 15, "precio": 19.99},
            {"nombre": "Mouse", "cantidad": 30, "precio": 12.50},
            {"nombre": "Monitor 24\"", "cantidad": 7, "precio": 129.90},
        ]
        for e in ejemplos:
            self.add_item(e["nombre"], e["cantidad"], e["precio"])

    # Navegación
    def show_login(self):
        self.inventory_frame.pack_forget()
        self.login_frame.reset()
        self.login_frame.pack(fill="both", expand=True)

    def show_inventory(self):
        self.login_frame.pack_forget()
        self.inventory_frame.refresh_table()
        self.inventory_frame.update_status()
        self.inventory_frame.pack(fill="both", expand=True)

    # Sesión
    def login(self, username, password):
        # Credenciales quemadas: admin/admin
        if username == "admin" and password == "admin":
            self.session["user"] = "admin"
            self.show_inventory()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def logout(self):
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.session["user"] = None
            self.show_login()

    # Inventario (CRUD en memoria)
    def add_item(self, nombre, cantidad, precio):
        item = {
            "id": self._next_id,
            "nombre": nombre,
            "cantidad": int(cantidad),
            "precio": float(precio),
        }
        self.inventory.append(item)
        self._next_id += 1
        return item

    def get_item(self, item_id):
        for it in self.inventory:
            if it["id"] == item_id:
                return it
        return None

    def update_item(self, item_id, nombre, cantidad, precio):
        it = self.get_item(item_id)
        if not it:
            return False
        it["nombre"] = nombre
        it["cantidad"] = int(cantidad)
        it["precio"] = float(precio)
        return True

    def delete_item(self, item_id):
        before = len(self.inventory)
        self.inventory = [it for it in self.inventory if it["id"] != item_id]
        return len(self.inventory) < before


class LoginFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self, padding=24)
        container.grid(row=0, column=0, sticky="nsew")
        for i in range(2):
            container.columnconfigure(i, weight=1)

        title = ttk.Label(container, text="Iniciar sesión", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 16))

        ttk.Label(container, text="Usuario:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(container, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)

        self.username_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")

        user_entry = ttk.Entry(container, textvariable=self.username_var)
        pass_entry = ttk.Entry(container, textvariable=self.password_var, show="*")

        user_entry.grid(row=1, column=1, sticky="ew", pady=6)
        pass_entry.grid(row=2, column=1, sticky="ew", pady=6)

        hint = ttk.Label(
            container,
            text="Credenciales simuladas → usuario: admin, contraseña: admin",
            foreground="#666"
        )
        hint.grid(row=3, column=0, columnspan=2, pady=(2, 16))

        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, pady=8)

        login_btn = ttk.Button(btns, text="Entrar", command=self._on_login)
        login_btn.grid(row=0, column=0, padx=6)

        quit_btn = ttk.Button(btns, text="Salir", command=self.master.destroy)
        quit_btn.grid(row=0, column=1, padx=6)

        self.bind_all("<Return>", lambda e: self._on_login())

    def reset(self):
        self.username_var.set("")
        self.password_var.set("")

    def _on_login(self):
        self.master.login(self.username_var.get().strip(), self.password_var.get().strip())


class InventoryFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        self._selected_id = None

        # Layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        header = ttk.Frame(self, padding=(12, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(header, text="Inventario", font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, sticky="w")

        logout_btn = ttk.Button(header, text="Cerrar sesión", command=self.master.logout)
        logout_btn.grid(row=0, column=1, sticky="e", padx=6)

        content = ttk.Frame(self, padding=(12, 8))
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        # Formulario
        form = ttk.LabelFrame(content, text="Formulario", padding=12)
        form.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for i in range(6):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Cantidad").grid(row=0, column=2, sticky="w")
        ttk.Label(form, text="Precio").grid(row=0, column=4, sticky="w")

        self.nombre_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        nombre_entry = ttk.Entry(form, textvariable=self.nombre_var)
        cantidad_entry = ttk.Entry(form, textvariable=self.cantidad_var)
        precio_entry = ttk.Entry(form, textvariable=self.precio_var)

        nombre_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=4)
        cantidad_entry.grid(row=1, column=2, sticky="ew", padx=(0, 8), pady=4)
        precio_entry.grid(row=1, column=4, sticky="ew", pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=6, sticky="w", pady=(8, 0))
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar seleccionado", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar seleccionado", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar formulario", command=self._clear_form).grid(row=0, column=3, padx=4)

        # Tabla
        table_frame = ttk.Frame(content)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("id", "nombre", "cantidad", "precio", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("total", text="Total")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=260, anchor="w")
        self.tree.column("cantidad", width=100, anchor="center")
        self.tree.column("precio", width=120, anchor="e")
        self.tree.column("total", width=120, anchor="e")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Barra de estado
        self.status_var = tk.StringVar(value="")
        status = ttk.Label(self, textvariable=self.status_var, anchor="w", padding=(12, 6))
        status.grid(row=2, column=0, sticky="ew")

    # Utilidades de UI
    def update_status(self):
        user = self.master.session.get("user") or "—"
        self.status_var.set(f"Usuario: {user}  |  Items: {len(self.master.inventory)}")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for it in self.master.inventory:
            total = it["cantidad"] * it["precio"]
            self.tree.insert("", "end", iid=str(it["id"]), values=(
                it["id"],
                it["nombre"],
                it["cantidad"],
                f"{it['precio']:.2f}",
                f"{total:.2f}",
            ))
        self.update_status()

    def _clear_form(self):
        self._selected_id = None
        self.nombre_var.set("")
        self.cantidad_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        item = self.master.get_item(int(iid))
        if item:
            self._selected_id = item["id"]
            self.nombre_var.set(item["nombre"])
            self.cantidad_var.set(str(item["cantidad"]))
            self.precio_var.set(f"{item['precio']:.2f}")

    # Validación y acciones CRUD
    def _validate_inputs(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre no puede estar vacío.")
            return None

        try:
            cantidad = int(self.cantidad_var.get().strip())
            if cantidad < 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Cantidad debe ser un entero ≥ 0.")
            return None

        try:
            precio = float(self.precio_var.get().strip())
            if precio < 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Precio debe ser un número ≥ 0.")
            return None

        return nombre, cantidad, precio

    def _on_add(self):
        vals = self._validate_inputs()
        if not vals:
            return
        nombre, cantidad, precio = vals
        self.master.add_item(nombre, cantidad, precio)
        self.refresh_table()
        self._clear_form()

    def _on_update(self):
        if self._selected_id is None:
            messagebox.showinfo("Actualizar", "Seleccione un elemento de la tabla para actualizar.")
            return
        vals = self._validate_inputs()
        if not vals:
            return
        nombre, cantidad, precio = vals
        ok = self.master.update_item(self._selected_id, nombre, cantidad, precio)
        if not ok:
            messagebox.showerror("Actualizar", "No se encontró el elemento a actualizar.")
            return
        self.refresh_table()
        self._clear_form()

    def _on_delete(self):
        if self._selected_id is None:
            messagebox.showinfo("Eliminar", "Seleccione un elemento de la tabla para eliminar.")
            return
        if not messagebox.askyesno("Eliminar", "¿Confirma eliminar el elemento seleccionado?"):
            return
        self.master.delete_item(self._selected_id)
        self.refresh_table()
        self._clear_form()


if __name__ == "__main__":
    app = App()
    app.mainloop()