import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clínica Veterinaria")
        self.geometry("1100x720")
        self.minsize(1000, 680)

        # Estado de sesión
        self.session = {"user": None}

        # Modelos en memoria
        self.owners = []  # {id, nombre, telefono, direccion, email}
        self.pets = []  # {id, nombre, especie, raza, edad, color, owner_id}
        self.appointments = []  # {id, pet_id, fecha, hora, motivo, estado, diagnostico, tratamiento, costo}
        self.medicines = []  # {id, nombre, tipo, stock, stock_minimo, precio}

        # Configuración
        self.base_price = 25.0
        self.appointment_duration = 30  # minutos
        self.start_hour = 8  # 8:00 AM
        self.end_hour = 18  # 6:00 PM

        # Secuencias de IDs
        self._owner_next_id = 1
        self._pet_next_id = 1
        self._appointment_next_id = 1
        self._medicine_next_id = 1

        # UI Frames
        self.login_frame = LoginFrame(self)
        self.main_frame = MainFrame(self)

        self._seed_data()
        self.show_login()

    # ===================== Datos iniciales =====================
    def _seed_data(self):
        # Dueños
        o1 = self._create_owner("Carlos Mendez", "555-1234", "Av. Principal 123", "carlos@mail.com")
        o2 = self._create_owner("Ana López", "555-5678", "Calle 2 #45", "ana@mail.com")
        o3 = self._create_owner("Luis Torres", "555-9012", "Barrio Centro", "luis@mail.com")
        
        # Mascotas
        self._create_pet("Max", "Perro", "Labrador", 3, "Dorado", o1["id"])
        self._create_pet("Luna", "Gato", "Siamés", 2, "Blanco", o1["id"])
        self._create_pet("Rocky", "Perro", "Pastor Alemán", 5, "Negro", o2["id"])
        self._create_pet("Mishi", "Gato", "Persa", 1, "Gris", o2["id"])
        self._create_pet("Bella", "Perro", "Beagle", 4, "Tricolor", o3["id"])
        self._create_pet("Coco", "Ave", "Loro", 2, "Verde", o3["id"])

        # Medicamentos
        self._create_medicine("Amoxicilina", "Antibiótico", 50, 10, 8.50)
        self._create_medicine("Vacuna Rabia", "Vacuna", 30, 15, 12.00)
        self._create_medicine("Desparasitante", "Antiparasitario", 40, 10, 5.00)
        self._create_medicine("Antiinflamatorio", "Analgésico", 25, 10, 6.50)
        self._create_medicine("Vitaminas", "Suplemento", 8, 10, 15.00)  # Bajo stock

        # Citas de ejemplo
        today = datetime.now()
        p1 = self.pets[0]["id"]
        p2 = self.pets[2]["id"]
        self._create_appointment(p1, today, "10:00", "Vacunación anual", "Pendiente")
        self._create_appointment(p2, today, "14:30", "Control general", "Pendiente")

    # ===================== Navegación =====================
    def show_login(self):
        self.main_frame.pack_forget()
        self.login_frame.reset()
        self.login_frame.pack(fill="both", expand=True)

    def show_main(self):
        self.login_frame.pack_forget()
        self.main_frame.refresh_all()
        self.main_frame.pack(fill="both", expand=True)

    # ===================== Sesión =====================
    def login(self, username, password):
        if username == "veterinario" and password == "1234":
            self.session["user"] = {"username": "veterinario", "nombre": "Dr. Veterinario"}
            self.show_main()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def logout(self):
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.session["user"] = None
            self.show_login()

    # ===================== CRUD Dueños =====================
    def _create_owner(self, nombre, telefono, direccion, email):
        o = {
            "id": self._owner_next_id,
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "email": email,
        }
        self.owners.append(o)
        self._owner_next_id += 1
        return o

    def update_owner(self, owner_id, nombre, telefono, direccion, email):
        for o in self.owners:
            if o["id"] == owner_id:
                o["nombre"] = nombre
                o["telefono"] = telefono
                o["direccion"] = direccion
                o["email"] = email
                return True
        return False

    def delete_owner(self, owner_id):
        # No permitir si tiene mascotas
        if any(p["owner_id"] == owner_id for p in self.pets):
            return False
        self.owners = [o for o in self.owners if o["id"] != owner_id]
        return True

    def get_owner(self, owner_id):
        for o in self.owners:
            if o["id"] == owner_id:
                return o
        return None

    # ===================== CRUD Mascotas =====================
    def _create_pet(self, nombre, especie, raza, edad, color, owner_id):
        p = {
            "id": self._pet_next_id,
            "nombre": nombre,
            "especie": especie,
            "raza": raza,
            "edad": edad,
            "color": color,
            "owner_id": owner_id,
        }
        self.pets.append(p)
        self._pet_next_id += 1
        return p

    def update_pet(self, pet_id, nombre, especie, raza, edad, color, owner_id):
        for p in self.pets:
            if p["id"] == pet_id:
                p["nombre"] = nombre
                p["especie"] = especie
                p["raza"] = raza
                p["edad"] = edad
                p["color"] = color
                p["owner_id"] = owner_id
                return True
        return False

    def delete_pet(self, pet_id):
        # No permitir si tiene citas
        if any(a["pet_id"] == pet_id for a in self.appointments):
            return False
        self.pets = [p for p in self.pets if p["id"] != pet_id]
        return True

    def get_pet(self, pet_id):
        for p in self.pets:
            if p["id"] == pet_id:
                return p
        return None

    # ===================== CRUD Medicamentos =====================
    def _create_medicine(self, nombre, tipo, stock, stock_minimo, precio):
        m = {
            "id": self._medicine_next_id,
            "nombre": nombre,
            "tipo": tipo,
            "stock": stock,
            "stock_minimo": stock_minimo,
            "precio": precio,
        }
        self.medicines.append(m)
        self._medicine_next_id += 1
        return m

    def update_medicine(self, med_id, nombre, tipo, stock, stock_minimo, precio):
        for m in self.medicines:
            if m["id"] == med_id:
                m["nombre"] = nombre
                m["tipo"] = tipo
                m["stock"] = stock
                m["stock_minimo"] = stock_minimo
                m["precio"] = precio
                return True
        return False

    def delete_medicine(self, med_id):
        self.medicines = [m for m in self.medicines if m["id"] != med_id]
        return True

    def get_medicine(self, med_id):
        for m in self.medicines:
            if m["id"] == med_id:
                return m
        return None

    def low_stock_medicines(self):
        return [m for m in self.medicines if m["stock"] <= m["stock_minimo"]]

    # ===================== Citas =====================
    def _create_appointment(self, pet_id, fecha, hora, motivo, estado):
        a = {
            "id": self._appointment_next_id,
            "pet_id": pet_id,
            "fecha": fecha if isinstance(fecha, datetime) else datetime.strptime(fecha, "%Y-%m-%d"),
            "hora": hora,
            "motivo": motivo,
            "estado": estado,  # Pendiente, En atención, Completada
            "diagnostico": "",
            "tratamiento": "",
            "costo": 0.0,
        }
        self.appointments.append(a)
        self._appointment_next_id += 1
        return a

    def update_appointment(self, apt_id, pet_id, fecha, hora, motivo):
        for a in self.appointments:
            if a["id"] == apt_id:
                a["pet_id"] = pet_id
                a["fecha"] = fecha if isinstance(fecha, datetime) else datetime.strptime(fecha, "%Y-%m-%d")
                a["hora"] = hora
                a["motivo"] = motivo
                return True
        return False

    def delete_appointment(self, apt_id):
        self.appointments = [a for a in self.appointments if a["id"] != apt_id]
        return True

    def complete_appointment(self, apt_id, diagnostico, tratamiento, costo):
        for a in self.appointments:
            if a["id"] == apt_id:
                a["estado"] = "Completada"
                a["diagnostico"] = diagnostico
                a["tratamiento"] = tratamiento
                a["costo"] = float(costo)
                return True
        return False

    def set_appointment_status(self, apt_id, estado):
        for a in self.appointments:
            if a["id"] == apt_id:
                a["estado"] = estado
                return True
        return False

    def get_appointment(self, apt_id):
        for a in self.appointments:
            if a["id"] == apt_id:
                return a
        return None

    def get_pet_history(self, pet_id):
        return [a for a in self.appointments if a["pet_id"] == pet_id and a["estado"] == "Completada"]


# ======================= Frames de UI =======================
class LoginFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        container = ttk.Frame(self, padding=24)
        container.pack(expand=True)

        ttk.Label(container, text="Clínica Veterinaria", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8))
        ttk.Label(container, text="Iniciar sesión", font=("Segoe UI", 14)).grid(row=1, column=0, columnspan=2, pady=(0, 16))

        ttk.Label(container, text="Usuario:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(container, text="Contraseña:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=6)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Entry(container, textvariable=self.username_var).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Entry(container, textvariable=self.password_var, show="*").grid(row=3, column=1, sticky="ew", pady=6)

        hint = ttk.Label(container, text="Credenciales → veterinario / 1234", foreground="#666")
        hint.grid(row=4, column=0, columnspan=2, pady=(2, 14))

        btns = ttk.Frame(container)
        btns.grid(row=5, column=0, columnspan=2)
        ttk.Button(btns, text="Entrar", command=self._on_login).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Salir", command=self.master.destroy).grid(row=0, column=1, padx=6)

        self.bind_all("<Return>", lambda e: self._on_login())

    def reset(self):
        self.username_var.set("")
        self.password_var.set("")

    def _on_login(self):
        self.master.login(self.username_var.get().strip(), self.password_var.get().strip())


class MainFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        # Header
        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill="x")
        ttk.Label(header, text="🏥 Clínica Veterinaria", font=("Segoe UI", 14, "bold")).pack(side="left")
        
        # Alertas de stock bajo
        self.alert_label = ttk.Label(header, text="", foreground="red", font=("Segoe UI", 10, "bold"))
        self.alert_label.pack(side="left", padx=20)
        
        ttk.Button(header, text="Cerrar sesión", command=self.master.logout).pack(side="right")

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=4, pady=4)

        self.appointments_tab = AppointmentsTab(self)
        self.pets_tab = PetsTab(self)
        self.owners_tab = OwnersTab(self)
        self.medicines_tab = MedicinesTab(self)
        self.config_tab = ConfigTab(self)
        self.reports_tab = ReportsTab(self)

        self.nb.add(self.appointments_tab, text="📅 Agenda")
        self.nb.add(self.pets_tab, text="🐾 Mascotas")
        self.nb.add(self.owners_tab, text="👤 Dueños")
        self.nb.add(self.medicines_tab, text="💊 Medicamentos")
        self.nb.add(self.config_tab, text="⚙️ Configuración")
        self.nb.add(self.reports_tab, text="📊 Reportes")

        # Status bar
        self.status_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status_var, anchor="w", padding=(12, 6)).pack(fill="x")

    def refresh_all(self):
        self._update_status()
        self._check_alerts()
        self.appointments_tab.refresh_everything()
        self.pets_tab.refresh_everything()
        self.owners_tab.refresh_everything()
        self.medicines_tab.refresh_everything()
        self.config_tab.refresh_everything()
        self.reports_tab.refresh_everything()

    def _update_status(self):
        user = self.master.session.get("user", {}).get("nombre", "")
        today_apts = [a for a in self.master.appointments if a["fecha"].date() == datetime.now().date()]
        pending = [a for a in today_apts if a["estado"] == "Pendiente"]
        txt = f"Usuario: {user} | Mascotas registradas: {len(self.master.pets)} | Citas hoy: {len(today_apts)} (Pendientes: {len(pending)})"
        self.status_var.set(txt)

    def _check_alerts(self):
        low = self.master.low_stock_medicines()
        if low:
            names = ", ".join([m["nombre"] for m in low[:3]])
            if len(low) > 3:
                names += f" y {len(low)-3} más"
            self.alert_label.config(text=f"⚠️ Stock bajo: {names}")
        else:
            self.alert_label.config(text="")


class OwnersTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Dueño", padding=10)
        form.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(form, text="Teléfono").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(form, text="Dirección").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Label(form, text="Email").grid(row=0, column=3, sticky="w", padx=4)

        self.nombre_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.email_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.nombre_var, width=20).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.telefono_var, width=15).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.direccion_var, width=25).grid(row=1, column=2, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.email_var, width=20).grid(row=1, column=3, sticky="ew", padx=4, pady=4)

        for i in range(4):
            form.columnconfigure(i, weight=1)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=4, sticky="w", pady=8)
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "nombre", "telefono", "direccion", "email")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w in [("id", 50), ("nombre", 180), ("telefono", 120), ("direccion", 220), ("email", 180)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w" if c != "id" else "center")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

    def refresh_everything(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for o in self.app.owners:
            self.tree.insert("", "end", iid=str(o["id"]), values=(o["id"], o["nombre"], o["telefono"], o["direccion"], o["email"]))

    def _clear_form(self):
        self._selected_id = None
        self.nombre_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.email_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        oid = int(sel[0])
        o = self.app.get_owner(oid)
        if o:
            self._selected_id = o["id"]
            self.nombre_var.set(o["nombre"])
            self.telefono_var.set(o["telefono"])
            self.direccion_var.set(o["direccion"])
            self.email_var.set(o["email"])

    def _on_add(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        self.app._create_owner(nombre, self.telefono_var.get().strip(), self.direccion_var.get().strip(), self.email_var.get().strip())
        self.refresh_everything()
        self._clear_form()

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione un dueño.")
            return
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        self.app.update_owner(self._selected_id, nombre, self.telefono_var.get().strip(), self.direccion_var.get().strip(), self.email_var.get().strip())
        self.refresh_everything()
        self._clear_form()

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione un dueño.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el dueño seleccionado?"):
            return
        ok = self.app.delete_owner(self._selected_id)
        if not ok:
            messagebox.showerror("Error", "No se puede eliminar: tiene mascotas asociadas.")
            return
        self.refresh_everything()
        self._clear_form()


class PetsTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Mascota", padding=10)
        form.grid(row=0, column=0, sticky="ew")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(form, text="Especie").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(form, text="Raza").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Label(form, text="Edad").grid(row=0, column=3, sticky="w", padx=4)
        ttk.Label(form, text="Color").grid(row=0, column=4, sticky="w", padx=4)
        ttk.Label(form, text="Dueño").grid(row=0, column=5, sticky="w", padx=4)

        self.nombre_var = tk.StringVar()
        self.especie_var = tk.StringVar()
        self.raza_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.owner_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.nombre_var, width=15).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.especie_var, width=12).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.raza_var, width=15).grid(row=1, column=2, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.edad_var, width=8).grid(row=1, column=3, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.color_var, width=12).grid(row=1, column=4, sticky="ew", padx=4, pady=4)
        
        self.owner_cb = ttk.Combobox(form, textvariable=self.owner_var, state="readonly", width=20)
        self.owner_cb.grid(row=1, column=5, sticky="ew", padx=4, pady=4)

        for i in range(6):
            form.columnconfigure(i, weight=1)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=6, sticky="w", pady=8)
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)
        ttk.Button(btns, text="Ver Historial", command=self._on_history).grid(row=0, column=4, padx=4)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "nombre", "especie", "raza", "edad", "color", "dueno")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w in [("id", 50), ("nombre", 120), ("especie", 100), ("raza", 120), ("edad", 60), ("color", 100), ("dueno", 180)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w" if c not in ["id", "edad"] else "center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

    def refresh_everything(self):
        owners = [f"{o['id']} - {o['nombre']}" for o in self.app.owners]
        self.owner_cb["values"] = owners
        if owners and not self.owner_var.get():
            self.owner_var.set(owners[0])

        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.app.pets:
            owner = self.app.get_owner(p["owner_id"])
            owner_name = owner["nombre"] if owner else "?"
            self.tree.insert("", "end", iid=str(p["id"]), 
                           values=(p["id"], p["nombre"], p["especie"], p["raza"], p["edad"], p["color"], owner_name))

    def _clear_form(self):
        self._selected_id = None
        self.nombre_var.set("")
        self.especie_var.set("")
        self.raza_var.set("")
        self.edad_var.set("")
        self.color_var.set("")
        if self.owner_cb["values"]:
            self.owner_var.set(self.owner_cb["values"][0])
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        pid = int(sel[0])
        p = self.app.get_pet(pid)
        if p:
            self._selected_id = p["id"]
            self.nombre_var.set(p["nombre"])
            self.especie_var.set(p["especie"])
            self.raza_var.set(p["raza"])
            self.edad_var.set(str(p["edad"]))
            self.color_var.set(p["color"])
            owner = self.app.get_owner(p["owner_id"])
            if owner:
                self.owner_var.set(f"{owner['id']} - {owner['nombre']}")

    def _on_add(self):
        nombre = self.nombre_var.get().strip()
        especie = self.especie_var.get().strip()
        if not nombre or not especie:
            messagebox.showwarning("Validación", "Nombre y especie son obligatorios.")
            return
        try:
            edad = int(self.edad_var.get().strip()) if self.edad_var.get().strip() else 0
        except:
            messagebox.showwarning("Validación", "Edad debe ser un número.")
            return
        if not self.owner_var.get():
            messagebox.showwarning("Validación", "Seleccione un dueño.")
            return
        owner_id = int(self.owner_var.get().split(" - ")[0])
        self.app._create_pet(nombre, especie, self.raza_var.get().strip(), edad, self.color_var.get().strip(), owner_id)
        self.refresh_everything()
        self.parent._update_status()
        self._clear_form()

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione una mascota.")
            return
        nombre = self.nombre_var.get().strip()
        especie = self.especie_var.get().strip()
        if not nombre or not especie:
            messagebox.showwarning("Validación", "Nombre y especie son obligatorios.")
            return
        try:
            edad = int(self.edad_var.get().strip()) if self.edad_var.get().strip() else 0
        except:
            messagebox.showwarning("Validación", "Edad debe ser un número.")
            return
        owner_id = int(self.owner_var.get().split(" - ")[0])
        self.app.update_pet(self._selected_id, nombre, especie, self.raza_var.get().strip(), edad, self.color_var.get().strip(), owner_id)
        self.refresh_everything()
        self._clear_form()

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione una mascota.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar la mascota seleccionada?"):
            return
        ok = self.app.delete_pet(self._selected_id)
        if not ok:
            messagebox.showerror("Error", "No se puede eliminar: tiene citas asociadas.")
            return
        self.refresh_everything()
        self.parent._update_status()
        self._clear_form()

    def _on_history(self):
        if not self._selected_id:
            messagebox.showinfo("Historial", "Seleccione una mascota.")
            return
        pet = self.app.get_pet(self._selected_id)
        if not pet:
            return
        history = self.app.get_pet_history(self._selected_id)
        
        win = tk.Toplevel(self)
        win.title(f"Historial Médico - {pet['nombre']}")
        win.geometry("800x400")
        
        ttk.Label(win, text=f"Historial de {pet['nombre']} ({pet['especie']} - {pet['raza']})", 
                 font=("Segoe UI", 12, "bold"), padding=10).pack()
        
        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ("fecha", "motivo", "diagnostico", "tratamiento", "costo")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c, w in [("fecha", 120), ("motivo", 150), ("diagnostico", 180), ("tratamiento", 180), ("costo", 80)]:
            tree.heading(c, text=c.upper())
            tree.column(c, width=w, anchor="w" if c != "costo" else "e")
        
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        for h in history:
            fecha = h["fecha"].strftime("%Y-%m-%d")
            tree.insert("", "end", values=(fecha, h["motivo"], h["diagnostico"], h["tratamiento"], f"${h['costo']:.2f}"))
        
        if not history:
            ttk.Label(win, text="No hay historial médico registrado.", foreground="#999").pack(pady=20)


class MedicinesTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Medicamento", padding=10)
        form.grid(row=0, column=0, sticky="ew")

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(form, text="Tipo").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(form, text="Stock").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Label(form, text="Stock Mínimo").grid(row=0, column=3, sticky="w", padx=4)
        ttk.Label(form, text="Precio").grid(row=0, column=4, sticky="w", padx=4)

        self.nombre_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.stock_min_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.nombre_var, width=18).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.tipo_var, width=15).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.stock_var, width=10).grid(row=1, column=2, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.stock_min_var, width=10).grid(row=1, column=3, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.precio_var, width=10).grid(row=1, column=4, sticky="ew", padx=4, pady=4)

        for i in range(5):
            form.columnconfigure(i, weight=1)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=5, sticky="w", pady=8)
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "nombre", "tipo", "stock", "stock_min", "precio", "alerta")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w in [("id", 50), ("nombre", 180), ("tipo", 150), ("stock", 80), ("stock_min", 100), ("precio", 80), ("alerta", 100)]:
            self.tree.heading(c, text=c.upper().replace("_", " "))
            self.tree.column(c, width=w, anchor="w" if c not in ["id", "stock", "stock_min", "precio", "alerta"] else "center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

    def refresh_everything(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in self.app.medicines:
            alerta = "⚠️ BAJO" if m["stock"] <= m["stock_minimo"] else "✓ OK"
            self.tree.insert("", "end", iid=str(m["id"]),
                           values=(m["id"], m["nombre"], m["tipo"], m["stock"], m["stock_minimo"], f"${m['precio']:.2f}", alerta))
            # Colorear filas con stock bajo
            if m["stock"] <= m["stock_minimo"]:
                self.tree.tag_configure(str(m["id"]), background="#ffe6e6")

    def _clear_form(self):
        self._selected_id = None
        self.nombre_var.set("")
        self.tipo_var.set("")
        self.stock_var.set("")
        self.stock_min_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        mid = int(sel[0])
        m = self.app.get_medicine(mid)
        if m:
            self._selected_id = m["id"]
            self.nombre_var.set(m["nombre"])
            self.tipo_var.set(m["tipo"])
            self.stock_var.set(str(m["stock"]))
            self.stock_min_var.set(str(m["stock_minimo"]))
            self.precio_var.set(f"{m['precio']:.2f}")

    def _on_add(self):
        nombre = self.nombre_var.get().strip()
        tipo = self.tipo_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        try:
            stock = int(self.stock_var.get().strip()) if self.stock_var.get().strip() else 0
            stock_min = int(self.stock_min_var.get().strip()) if self.stock_min_var.get().strip() else 10
            precio = float(self.precio_var.get().strip().replace("$", "")) if self.precio_var.get().strip() else 0.0
        except:
            messagebox.showwarning("Validación", "Stock, stock mínimo y precio deben ser números válidos.")
            return
        self.app._create_medicine(nombre, tipo, stock, stock_min, precio)
        self.refresh_everything()
        self.parent._check_alerts()
        self._clear_form()

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione un medicamento.")
            return
        nombre = self.nombre_var.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        try:
            stock = int(self.stock_var.get().strip()) if self.stock_var.get().strip() else 0
            stock_min = int(self.stock_min_var.get().strip()) if self.stock_min_var.get().strip() else 10
            precio = float(self.precio_var.get().strip().replace("$", "")) if self.precio_var.get().strip() else 0.0
        except:
            messagebox.showwarning("Validación", "Stock, stock mínimo y precio deben ser números válidos.")
            return
        self.app.update_medicine(self._selected_id, nombre, self.tipo_var.get().strip(), stock, stock_min, precio)
        self.refresh_everything()
        self.parent._check_alerts()
        self._clear_form()

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione un medicamento.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el medicamento seleccionado?"):
            return
        self.app.delete_medicine(self._selected_id)
        self.refresh_everything()
        self.parent._check_alerts()
        self._clear_form()


class AppointmentsTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Formulario agendar cita
        form = ttk.LabelFrame(self, text="Agendar Cita", padding=10)
        form.grid(row=0, column=0, sticky="ew")

        ttk.Label(form, text="Mascota").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(form, text="Fecha (AAAA-MM-DD)").grid(row=0, column=1, sticky="w", padx=4)
        ttk.Label(form, text="Hora (HH:MM)").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Label(form, text="Motivo").grid(row=0, column=3, sticky="w", padx=4)

        self.pet_var = tk.StringVar()
        self.fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.hora_var = tk.StringVar(value="10:00")
        self.motivo_var = tk.StringVar()

        self.pet_cb = ttk.Combobox(form, textvariable=self.pet_var, state="readonly", width=25)
        self.pet_cb.grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.fecha_var, width=15).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.hora_var, width=10).grid(row=1, column=2, sticky="ew", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.motivo_var, width=30).grid(row=1, column=3, sticky="ew", padx=4, pady=4)

        for i in range(4):
            form.columnconfigure(i, weight=1)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=4, sticky="w", pady=8)
        ttk.Button(btns, text="Agendar", command=self._on_schedule).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar cita", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar cita", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)

        # Tabla de agenda
        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "mascota", "dueno", "fecha", "hora", "motivo", "estado")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w in [("id", 50), ("mascota", 120), ("dueno", 150), ("fecha", 100), ("hora", 80), ("motivo", 180), ("estado", 100)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w" if c not in ["id", "hora", "estado"] else "center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

        # Botones de acción
        action_frame = ttk.Frame(self)
        action_frame.grid(row=2, column=0, sticky="ew", pady=8)
        ttk.Button(action_frame, text="➜ En Atención", command=lambda: self._change_status("En atención")).pack(side="left", padx=4)
        ttk.Button(action_frame, text="✓ Completar Cita", command=self._on_complete).pack(side="left", padx=4)
        ttk.Button(action_frame, text="🔄 Refrescar", command=self.refresh_everything).pack(side="left", padx=4)

    def refresh_everything(self):
        pets = [f"{p['id']} - {p['nombre']} ({p['especie']})" for p in self.app.pets]
        self.pet_cb["values"] = pets
        if pets and not self.pet_var.get():
            self.pet_var.set(pets[0])

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for a in self.app.appointments:
            pet = self.app.get_pet(a["pet_id"])
            owner = self.app.get_owner(pet["owner_id"]) if pet else None
            pet_name = pet["nombre"] if pet else "?"
            owner_name = owner["nombre"] if owner else "?"
            fecha = a["fecha"].strftime("%Y-%m-%d")
            
            self.tree.insert("", "end", iid=str(a["id"]),
                           values=(a["id"], pet_name, owner_name, fecha, a["hora"], a["motivo"], a["estado"]))
            
            # Colorear según estado
            if a["estado"] == "Pendiente":
                self.tree.tag_configure(str(a["id"]), background="#e6ffe6")
            elif a["estado"] == "En atención":
                self.tree.tag_configure(str(a["id"]), background="#fff4e6")
            elif a["estado"] == "Completada":
                self.tree.tag_configure(str(a["id"]), background="#e6f2ff")

    def _clear_form(self):
        self._selected_id = None
        if self.pet_cb["values"]:
            self.pet_var.set(self.pet_cb["values"][0])
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.hora_var.set("10:00")
        self.motivo_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        aid = int(sel[0])
        a = self.app.get_appointment(aid)
        if a:
            self._selected_id = a["id"]
            pet = self.app.get_pet(a["pet_id"])
            if pet:
                self.pet_var.set(f"{pet['id']} - {pet['nombre']} ({pet['especie']})")
            self.fecha_var.set(a["fecha"].strftime("%Y-%m-%d"))
            self.hora_var.set(a["hora"])
            self.motivo_var.set(a["motivo"])

    def _on_schedule(self):
        if not self.pet_var.get():
            messagebox.showwarning("Validación", "Seleccione una mascota.")
            return
        try:
            pet_id = int(self.pet_var.get().split(" - ")[0])
            fecha = datetime.strptime(self.fecha_var.get().strip(), "%Y-%m-%d")
            hora = self.hora_var.get().strip()
            motivo = self.motivo_var.get().strip()
            if not motivo:
                messagebox.showwarning("Validación", "El motivo es obligatorio.")
                return
            self.app._create_appointment(pet_id, fecha, hora, motivo, "Pendiente")
            messagebox.showinfo("Cita agendada", "La cita se ha agendado correctamente.")
            self.refresh_everything()
            self.parent._update_status()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agendar: {str(e)}")

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione una cita.")
            return
        try:
            pet_id = int(self.pet_var.get().split(" - ")[0])
            fecha = datetime.strptime(self.fecha_var.get().strip(), "%Y-%m-%d")
            hora = self.hora_var.get().strip()
            motivo = self.motivo_var.get().strip()
            self.app.update_appointment(self._selected_id, pet_id, fecha, hora, motivo)
            messagebox.showinfo("Actualizar", "Cita actualizada.")
            self.refresh_everything()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione una cita.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar la cita seleccionada?"):
            return
        self.app.delete_appointment(self._selected_id)
        self.refresh_everything()
        self.parent._update_status()
        self._clear_form()

    def _change_status(self, status):
        if not self._selected_id:
            messagebox.showinfo("Cambiar estado", "Seleccione una cita.")
            return
        self.app.set_appointment_status(self._selected_id, status)
        self.refresh_everything()

    def _on_complete(self):
        if not self._selected_id:
            messagebox.showinfo("Completar", "Seleccione una cita.")
            return
        
        apt = self.app.get_appointment(self._selected_id)
        if not apt:
            return
        
        # Ventana para completar cita
        win = tk.Toplevel(self)
        win.title("Completar Cita")
        win.geometry("500x350")
        win.transient(self)
        win.grab_set()

        ttk.Label(win, text="Completar Cita", font=("Segoe UI", 12, "bold"), padding=10).pack()

        form = ttk.Frame(win, padding=10)
        form.pack(fill="both", expand=True)

        ttk.Label(form, text="Diagnóstico:").grid(row=0, column=0, sticky="nw", pady=4)
        diag_text = tk.Text(form, height=4, width=50)
        diag_text.grid(row=0, column=1, pady=4, padx=4)

        ttk.Label(form, text="Tratamiento:").grid(row=1, column=0, sticky="nw", pady=4)
        trat_text = tk.Text(form, height=4, width=50)
        trat_text.grid(row=1, column=1, pady=4, padx=4)

        ttk.Label(form, text="Costo:").grid(row=2, column=0, sticky="w", pady=4)
        costo_var = tk.StringVar(value=str(self.app.base_price))
        ttk.Entry(form, textvariable=costo_var, width=15).grid(row=2, column=1, sticky="w", pady=4, padx=4)

        def save_complete():
            try:
                diagnostico = diag_text.get("1.0", "end-1c").strip()
                tratamiento = trat_text.get("1.0", "end-1c").strip()
                costo = float(costo_var.get().replace("$", ""))
                
                if not diagnostico or not tratamiento:
                    messagebox.showwarning("Validación", "Diagnóstico y tratamiento son obligatorios.")
                    return
                
                self.app.complete_appointment(self._selected_id, diagnostico, tratamiento, costo)
                messagebox.showinfo("Completada", "Cita completada correctamente.")
                win.destroy()
                self.refresh_everything()
                self.parent._update_status()
                self._clear_form()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        ttk.Button(form, text="Guardar y Completar", command=save_complete).grid(row=3, column=1, sticky="w", pady=10, padx=4)


class ConfigTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        frm = ttk.LabelFrame(self, text="Configuración de la Clínica", padding=12)
        frm.pack(fill="x")

        ttk.Label(frm, text="Precio base consulta ($)").grid(row=0, column=0, sticky="w", padx=4, pady=6)
        ttk.Label(frm, text="Duración cita (minutos)").grid(row=1, column=0, sticky="w", padx=4, pady=6)
        ttk.Label(frm, text="Hora inicio (0-23)").grid(row=2, column=0, sticky="w", padx=4, pady=6)
        ttk.Label(frm, text="Hora fin (0-23)").grid(row=3, column=0, sticky="w", padx=4, pady=6)

        self.base_price_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        ttk.Entry(frm, textvariable=self.base_price_var, width=12).grid(row=0, column=1, sticky="w", padx=4, pady=6)
        ttk.Entry(frm, textvariable=self.duration_var, width=12).grid(row=1, column=1, sticky="w", padx=4, pady=6)
        ttk.Entry(frm, textvariable=self.start_var, width=12).grid(row=2, column=1, sticky="w", padx=4, pady=6)
        ttk.Entry(frm, textvariable=self.end_var, width=12).grid(row=3, column=1, sticky="w", padx=4, pady=6)

        ttk.Button(frm, text="Guardar Configuración", command=self._on_save).grid(row=4, column=0, columnspan=2, pady=12)

    def refresh_everything(self):
        self.base_price_var.set(f"{self.app.base_price:.2f}")
        self.duration_var.set(str(self.app.appointment_duration))
        self.start_var.set(str(self.app.start_hour))
        self.end_var.set(str(self.app.end_hour))

    def _on_save(self):
        try:
            price = float(self.base_price_var.get().replace("$", ""))
            duration = int(self.duration_var.get())
            start = int(self.start_var.get())
            end = int(self.end_var.get())
            
            if price < 0 or duration <= 0 or start < 0 or start > 23 or end < 0 or end > 23 or start >= end:
                raise ValueError("Valores inválidos")
            
            self.app.base_price = price
            self.app.appointment_duration = duration
            self.app.start_hour = start
            self.app.end_hour = end
            
            messagebox.showinfo("Configuración", "Configuración guardada correctamente.")
            self.parent._update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Error en validación: {str(e)}")


class ReportsTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        # Resumen
        summary_frame = ttk.LabelFrame(self, text="Resumen General", padding=12)
        summary_frame.pack(fill="x", pady=(0, 10))

        self.summary_text = tk.Text(summary_frame, height=8, width=80, state="disabled", font=("Consolas", 10))
        self.summary_text.pack(fill="x")

        # Historial completo
        ttk.Label(self, text="Historial de Citas Completadas", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 4))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "fecha", "mascota", "especie", "dueno", "motivo", "diagnostico", "costo")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w in [("id", 40), ("fecha", 90), ("mascota", 100), ("especie", 80), ("dueno", 130), ("motivo", 140), ("diagnostico", 180), ("costo", 70)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w" if c not in ["id", "costo"] else "center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        ttk.Button(self, text="🔄 Actualizar Reportes", command=self.refresh_everything).pack(pady=10)

    def refresh_everything(self):
        # Calcular estadísticas
        completed = [a for a in self.app.appointments if a["estado"] == "Completada"]
        total_ingresos = sum(a.get("costo", 0) for a in completed)
        
        # Especies más atendidas
        especies = {}
        for a in completed:
            pet = self.app.get_pet(a["pet_id"])
            if pet:
                esp = pet["especie"]
                especies[esp] = especies.get(esp, 0) + 1
        
        top_especies = sorted(especies.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Stock bajo
        low_stock = self.app.low_stock_medicines()
        
        # Actualizar resumen
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", "end")
        
        report = f"""
═══════════════════════════════════════════════════════════════════════
  REPORTE GENERAL - CLÍNICA VETERINARIA
═══════════════════════════════════════════════════════════════════════

  📊 ESTADÍSTICAS:
    • Total citas completadas: {len(completed)}
    • Total ingresos generados: ${total_ingresos:.2f}
    • Promedio por consulta: ${total_ingresos/len(completed) if completed else 0:.2f}

  🐾 ESPECIES MÁS ATENDIDAS:
"""
        for esp, count in top_especies:
            report += f"    • {esp}: {count} consulta(s)\n"
        
        if not top_especies:
            report += "    (Sin datos)\n"
        
        report += f"\n  💊 ALERTAS DE STOCK:\n"
        if low_stock:
            for med in low_stock:
                report += f"    ⚠️ {med['nombre']}: {med['stock']} unidades (mín: {med['stock_minimo']})\n"
        else:
            report += "    ✓ Todos los medicamentos tienen stock suficiente\n"
        
        report += "\n═══════════════════════════════════════════════════════════════════════\n"
        
        self.summary_text.insert("1.0", report)
        self.summary_text.config(state="disabled")

        # Tabla de historial
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for a in completed:
            pet = self.app.get_pet(a["pet_id"])
            owner = self.app.get_owner(pet["owner_id"]) if pet else None
            fecha = a["fecha"].strftime("%Y-%m-%d")
            self.tree.insert("", "end", values=(
                a["id"],
                fecha,
                pet["nombre"] if pet else "?",
                pet["especie"] if pet else "?",
                owner["nombre"] if owner else "?",
                a["motivo"],
                a.get("diagnostico", "")[:50] + "..." if len(a.get("diagnostico", "")) > 50 else a.get("diagnostico", ""),
                f"${a.get('costo', 0):.2f}"
            ))


if __name__ == "__main__":
    app = App()
    app.mainloop()
