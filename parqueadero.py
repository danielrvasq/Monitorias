import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import math


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Parqueadero (Login simulado)")
        self.geometry("1060x680")
        self.minsize(980, 640)

        # Estado de sesión y almacenamiento en memoria
        self.session = {"user": None}  # dict con usuario autenticado

        # Modelos en memoria
        self.users = []  # {id, username, password, nombre}
        self.vehicles = []  # {id, placa, user_id, marca, modelo, color}
        self.spots = []  # {id, codigo, ocupado(bool)}
        self.active_tickets = []  # {id, vehicle_id, spot_id, checkin, user_in}
        self.closed_tickets = []  # {id, vehicle_id, spot_id, checkin, checkout, user_in, user_out, total}

        # Configuración de negocio
        self.rate_per_hour = 5.0  # tarifa por hora (USD/moneda local)
        self.capacity = 12  # número de puestos

        # Secuencias de IDs
        self._user_next_id = 1
        self._vehicle_next_id = 1
        self._spot_next_id = 1
        self._ticket_next_id = 1

        # UI Frames
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterUserFrame(self)
        self.main_frame = MainFrame(self)

        self._seed_data()
        self.show_login()

    # ===================== Datos iniciales =====================
    def _seed_data(self):
        # Usuarios: admin por defecto
        self._create_user("admin", "admin", nombre="Administrador")
        # Crear puestos por capacidad
        self._ensure_spots(self.capacity)
        # Usuarios de ejemplo
        u1 = self._create_user("maria", "1234", nombre="María Pérez")
        u2 = self._create_user("juan", "1234", nombre="Juan Ruiz")
        # Vehículos de ejemplo
        self._create_vehicle("ABC123", u1["id"], marca="Toyota", modelo="Yaris", color="Rojo")
        self._create_vehicle("XYZ789", u2["id"], marca="Chevrolet", modelo="Onix", color="Negro")

    # ===================== Navegación =====================
    def show_login(self):
        self.register_frame.pack_forget()
        self.main_frame.pack_forget()
        self.login_frame.reset()
        self.login_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.register_frame.reset()
        self.register_frame.pack(fill="both", expand=True)

    def show_main(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.main_frame.refresh_all()
        self.main_frame.pack(fill="both", expand=True)

    # ===================== Sesión =====================
    def login(self, username, password):
        user = self._find_user_by_username(username)
        if user and user["password"] == password:
            self.session["user"] = user
            self.show_main()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def logout(self):
        if messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.session["user"] = None
            self.show_login()

    # ===================== Utilidades de modelo =====================
    # Usuarios
    def _find_user_by_username(self, username):
        for u in self.users:
            if u["username"].lower() == username.lower():
                return u
        return None

    def _create_user(self, username, password, nombre=""):
        if self._find_user_by_username(username):
            return None
        u = {
            "id": self._user_next_id,
            "username": username,
            "password": password,
            "nombre": nombre or username,
        }
        self.users.append(u)
        self._user_next_id += 1
        return u

    def update_user(self, user_id, username, password, nombre):
        # evitar duplicados de username
        for u in self.users:
            if u["id"] != user_id and u["username"].lower() == username.lower():
                return False
        for u in self.users:
            if u["id"] == user_id:
                u["username"] = username
                u["password"] = password
                u["nombre"] = nombre or username
                return True
        return False

    def delete_user(self, user_id):
        # no permitir eliminar admin
        for u in self.users:
            if u["id"] == user_id and u["username"] == "admin":
                return False
        # no permitir borrar usuario con vehículos o tickets activos
        if any(v["user_id"] == user_id for v in self.vehicles):
            return False
        self.users = [u for u in self.users if u["id"] != user_id]
        return True

    # Vehículos
    def _find_vehicle_by_plate(self, placa):
        for v in self.vehicles:
            if v["placa"].upper() == placa.upper():
                return v
        return None

    def _create_vehicle(self, placa, user_id, marca="", modelo="", color=""):
        if self._find_vehicle_by_plate(placa):
            return None
        v = {
            "id": self._vehicle_next_id,
            "placa": placa.upper().strip(),
            "user_id": user_id,
            "marca": marca,
            "modelo": modelo,
            "color": color,
        }
        self.vehicles.append(v)
        self._vehicle_next_id += 1
        return v

    def update_vehicle(self, vehicle_id, placa, user_id, marca, modelo, color):
        # placa única
        for v in self.vehicles:
            if v["id"] != vehicle_id and v["placa"].upper() == placa.upper():
                return False
        for v in self.vehicles:
            if v["id"] == vehicle_id:
                v["placa"] = placa.upper().strip()
                v["user_id"] = user_id
                v["marca"] = marca
                v["modelo"] = modelo
                v["color"] = color
                return True
        return False

    def delete_vehicle(self, vehicle_id):
        # no permitir si tiene ticket activo
        if any(t["vehicle_id"] == vehicle_id for t in self.active_tickets):
            return False
        self.vehicles = [v for v in self.vehicles if v["id"] != vehicle_id]
        return True

    # Puestos
    def _ensure_spots(self, new_capacity):
        # Crear o ajustar cantidad de puestos (códigos P1..Pn)
        current = len(self.spots)
        if new_capacity > current:
            for i in range(current + 1, new_capacity + 1):
                codigo = f"P{i}"
                self.spots.append({
                    "id": self._spot_next_id,
                    "codigo": codigo,
                    "ocupado": False,
                })
                self._spot_next_id += 1
        elif new_capacity < current:
            # solo podemos reducir si hay suficientes libres
            libres = [s for s in self.spots if not s["ocupado"]]
            exceso = current - new_capacity
            if len(libres) < exceso:
                raise ValueError("No hay suficientes puestos libres para reducir capacidad.")
            # quitar últimos libres
            to_remove = set(s["id"] for s in libres[-exceso:])
            self.spots = [s for s in self.spots if s["id"] not in to_remove]
        self.capacity = new_capacity

    def available_spots(self):
        return [s for s in self.spots if not s["ocupado"]]

    def get_spot_by_id(self, spot_id):
        for s in self.spots:
            if s["id"] == spot_id:
                return s
        return None

    # Tickets y lógica de parqueo
    def checkin(self, placa, maybe_user_id=None, marca="", modelo="", color="", spot_id=None):
        # Reglas: si vehículo existe, usarlo; si no existe, crear con propietario requerido
        veh = self._find_vehicle_by_plate(placa)
        if veh is None:
            if not maybe_user_id:
                raise ValueError("Debe seleccionar usuario propietario para una placa nueva.")
            veh = self._create_vehicle(placa, maybe_user_id, marca, modelo, color)
            if veh is None:
                raise ValueError("La placa ya existe.")
        # verificar que no esté ya activo
        if any(t["vehicle_id"] == veh["id"] for t in self.active_tickets):
            raise ValueError("Este vehículo ya tiene una entrada activa.")
        # verificar puesto
        spot = self.get_spot_by_id(spot_id) if spot_id else None
        if not spot or spot["ocupado"]:
            raise ValueError("Debe seleccionar un puesto disponible.")
        # crear ticket
        t = {
            "id": self._ticket_next_id,
            "vehicle_id": veh["id"],
            "spot_id": spot["id"],
            "checkin": datetime.now(),
            "user_in": self.session["user"]["id"] if self.session.get("user") else None,
        }
        self.active_tickets.append(t)
        self._ticket_next_id += 1
        # ocupar puesto
        spot["ocupado"] = True
        return t

    def _compute_amount(self, checkin_dt, checkout_dt):
        elapsed = checkout_dt - checkin_dt
        minutes = max(1, int(elapsed.total_seconds() // 60))
        hours = math.ceil(minutes / 60)
        return hours * float(self.rate_per_hour), elapsed

    def checkout(self, ticket_id):
        ticket = None
        for t in self.active_tickets:
            if t["id"] == ticket_id:
                ticket = t
                break
        if ticket is None:
            return None
        now = datetime.now()
        total, elapsed = self._compute_amount(ticket["checkin"], now)
        closed = {
            "id": ticket["id"],
            "vehicle_id": ticket["vehicle_id"],
            "spot_id": ticket["spot_id"],
            "checkin": ticket["checkin"],
            "checkout": now,
            "user_in": ticket["user_in"],
            "user_out": self.session["user"]["id"] if self.session.get("user") else None,
            "total": total,
        }
        self.closed_tickets.append(closed)
        # liberar puesto
        spot = self.get_spot_by_id(ticket["spot_id"])
        if spot:
            spot["ocupado"] = False
        # quitar de activos
        self.active_tickets = [t for t in self.active_tickets if t["id"] != ticket_id]
        return closed


# ======================= Frames de UI =======================
class LoginFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        container = ttk.Frame(self, padding=24)
        container.pack(expand=True)

        ttk.Label(container, text="Iniciar sesión", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 16))

        ttk.Label(container, text="Usuario:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(container, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        user_entry = ttk.Entry(container, textvariable=self.username_var)
        pass_entry = ttk.Entry(container, textvariable=self.password_var, show="*")
        user_entry.grid(row=1, column=1, sticky="ew", pady=6)
        pass_entry.grid(row=2, column=1, sticky="ew", pady=6)

        hint = ttk.Label(container, text="Credenciales por defecto → admin / admin", foreground="#666")
        hint.grid(row=3, column=0, columnspan=2, pady=(2, 14))

        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2)
        ttk.Button(btns, text="Entrar", command=self._on_login).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Registrar usuario", command=self.master.show_register).grid(row=0, column=1, padx=6)
        ttk.Button(btns, text="Salir", command=self.master.destroy).grid(row=0, column=2, padx=6)

        self.bind_all("<Return>", lambda e: self._on_login())

    def reset(self):
        self.username_var.set("")
        self.password_var.set("")

    def _on_login(self):
        self.master.login(self.username_var.get().strip(), self.password_var.get().strip())


class RegisterUserFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master
        container = ttk.Frame(self, padding=24)
        container.pack(expand=True)

        ttk.Label(container, text="Registrar nuevo usuario", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 16))
        ttk.Label(container, text="Usuario:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(container, text="Nombre:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(container, text="Contraseña:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=6)

        self.username_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Entry(container, textvariable=self.username_var).grid(row=1, column=1, sticky="ew", pady=6)
        ttk.Entry(container, textvariable=self.nombre_var).grid(row=2, column=1, sticky="ew", pady=6)
        ttk.Entry(container, textvariable=self.password_var, show="*").grid(row=3, column=1, sticky="ew", pady=6)

        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Guardar", command=self._on_save).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Volver", command=self.master.show_login).grid(row=0, column=1, padx=6)

    def reset(self):
        self.username_var.set("")
        self.nombre_var.set("")
        self.password_var.set("")

    def _on_save(self):
        username = self.username_var.get().strip()
        nombre = self.nombre_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Validación", "Usuario y contraseña son obligatorios.")
            return
        if self.master._find_user_by_username(username):
            messagebox.showwarning("Validación", "El usuario ya existe.")
            return
        self.master._create_user(username, password, nombre=nombre)
        messagebox.showinfo("Registro", "Usuario creado. Inicie sesión.")
        self.master.show_login()


class MainFrame(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master

        # Header
        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill="x")
        ttk.Label(header, text="Gestor de Parqueadero", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Cerrar sesión", command=self.master.logout).pack(side="right")

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.parking_tab = ParkingTab(self)
        self.vehicles_tab = VehiclesTab(self)
        self.users_tab = UsersTab(self)
        self.config_tab = ConfigTab(self)
        self.reports_tab = ReportsTab(self)

        self.nb.add(self.parking_tab, text="Parqueo")
        self.nb.add(self.vehicles_tab, text="Vehículos")
        self.nb.add(self.users_tab, text="Usuarios")
        self.nb.add(self.config_tab, text="Configuración")
        self.nb.add(self.reports_tab, text="Reportes")

        # Status bar
        self.status_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status_var, anchor="w", padding=(12, 6)).pack(fill="x")

        # refresco periódico de tiempos
        self.after(1000, self._tick)

    def _tick(self):
        # refrescar solo pestaña parqueo para tiempos
        try:
            self.parking_tab.refresh_active_table(update_elapsed_only=True)
        finally:
            self.after(1000, self._tick)

    def refresh_all(self):
        self._update_status()
        self.parking_tab.refresh_everything()
        self.vehicles_tab.refresh_everything()
        self.users_tab.refresh_everything()
        self.config_tab.refresh_everything()
        self.reports_tab.refresh_everything()

    def _update_status(self):
        user = self.master.session.get("user")
        txt = f"Usuario: {user['username']} | Tarifa: {self.master.rate_per_hour:.2f} /h | Puestos: {len(self.master.spots)} (Libres: {len(self.master.available_spots())}) | Activos: {len(self.master.active_tickets)}"
        self.status_var.set(txt)


class ParkingTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Check-in form
        form = ttk.LabelFrame(self, text="Registrar entrada", padding=10)
        form.grid(row=0, column=0, sticky="ew")
        for i in range(8):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="Placa").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Propietario").grid(row=0, column=2, sticky="w")
        ttk.Label(form, text="Marca").grid(row=0, column=4, sticky="w")
        ttk.Label(form, text="Modelo").grid(row=0, column=6, sticky="w")

        self.placa_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.modelo_var = tk.StringVar()
        self.color_var = tk.StringVar()

        self.owner_var = tk.StringVar()
        self.owner_cb = ttk.Combobox(form, textvariable=self.owner_var, state="readonly")

        ttk.Entry(form, textvariable=self.placa_var).grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=4)
        self.owner_cb.grid(row=1, column=2, columnspan=2, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.marca_var).grid(row=1, column=4, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.modelo_var).grid(row=1, column=6, sticky="ew", pady=4)

        ttk.Label(form, text="Color").grid(row=2, column=0, sticky="w")
        ttk.Label(form, text="Puesto").grid(row=2, column=2, sticky="w")
        self.color_entry = ttk.Entry(form, textvariable=self.color_var)
        self.color_entry.grid(row=3, column=0, sticky="ew", padx=(0, 8), pady=4)

        self.spot_var = tk.StringVar()
        self.spot_cb = ttk.Combobox(form, textvariable=self.spot_var, state="readonly")
        self.spot_cb.grid(row=3, column=2, sticky="ew", padx=(0, 8), pady=4)

        ttk.Button(form, text="Registrar Entrada", command=self._on_checkin).grid(row=3, column=6, sticky="e", pady=4)

        # Active table
        table_frame = ttk.LabelFrame(self, text="Vehículos en parqueo", padding=10)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "placa", "puesto", "entrada", "transcurrido")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w, a in [("id", 60, "center"), ("placa", 120, "w"), ("puesto", 80, "center"), ("entrada", 180, "center"), ("transcurrido", 140, "e")]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Checkout buttons
        btns = ttk.Frame(self)
        btns.grid(row=2, column=0, sticky="ew", pady=8)
        ttk.Button(btns, text="Registrar Salida", command=self._on_checkout).pack(side="left")
        ttk.Button(btns, text="Actualizar", command=self.refresh_everything).pack(side="left", padx=6)

    def refresh_everything(self):
        # owners
        owners = [f"{u['id']} - {u['nombre']} ({u['username']})" for u in self.app.users]
        self.owner_cb["values"] = owners
        if owners and not self.owner_var.get():
            self.owner_var.set(owners[0])
        # spots
        free_spots = self.app.available_spots()
        self.spot_cb["values"] = [f"{s['id']} - {s['codigo']}" for s in free_spots]
        if free_spots and not self.spot_var.get():
            self.spot_var.set(f"{free_spots[0]['id']} - {free_spots[0]['codigo']}")
        # table
        self.refresh_active_table()
        self.parent._update_status()

    def refresh_active_table(self, update_elapsed_only=False):
        if not update_elapsed_only:
            for item in self.tree.get_children():
                self.tree.delete(item)
        for t in self.app.active_tickets:
            veh = next((v for v in self.app.vehicles if v["id"] == t["vehicle_id"]), None)
            spot = self.app.get_spot_by_id(t["spot_id"]) if t else None
            placa = veh["placa"] if veh else "?"
            puesto = spot["codigo"] if spot else "?"
            entrada = t["checkin"].strftime("%Y-%m-%d %H:%M:%S")
            elapsed = datetime.now() - t["checkin"]
            h, rem = divmod(int(elapsed.total_seconds()), 3600)
            m, _ = divmod(rem, 60)
            trans = f"{h:02d}h {m:02d}m"
            if update_elapsed_only:
                if self.tree.exists(str(t["id"])):
                    self.tree.set(str(t["id"]), "transcurrido", trans)
            else:
                self.tree.insert("", "end", iid=str(t["id"]), values=(t["id"], placa, puesto, entrada, trans))
        self.parent._update_status()

    def _on_checkin(self):
        try:
            placa = self.placa_var.get().strip().upper()
            if not placa:
                messagebox.showwarning("Validación", "La placa es obligatoria.")
                return
            owner_id = None
            if not self.app._find_vehicle_by_plate(placa):
                # si no existe el vehículo, necesitamos propietario
                if not self.owner_var.get():
                    messagebox.showwarning("Validación", "Seleccione propietario para una placa nueva.")
                    return
                owner_id = int(self.owner_var.get().split(" - ")[0])
            if not self.spot_var.get():
                messagebox.showwarning("Validación", "Seleccione un puesto disponible.")
                return
            spot_id = int(self.spot_var.get().split(" - ")[0])
            t = self.app.checkin(
                placa,
                maybe_user_id=owner_id,
                marca=self.marca_var.get().strip(),
                modelo=self.modelo_var.get().strip(),
                color=self.color_var.get().strip(),
                spot_id=spot_id,
            )
            messagebox.showinfo("Entrada registrada", f"Ticket #{t['id']} creado para {placa} en puesto {self.app.get_spot_by_id(spot_id)['codigo']}.")
            # limpiar form parcial
            self.placa_var.set("")
            self.marca_var.set("")
            self.modelo_var.set("")
            self.color_var.set("")
            self.spot_var.set("")
            self.refresh_everything()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_checkout(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Salida", "Seleccione un ticket activo en la tabla.")
            return
        ticket_id = int(sel[0])
        # Previsualizar total
        ticket = next((t for t in self.app.active_tickets if t["id"] == ticket_id), None)
        if not ticket:
            messagebox.showerror("Error", "No se encontró el ticket.")
            return
        total, elapsed = self.app._compute_amount(ticket["checkin"], datetime.now())
        h, rem = divmod(int(elapsed.total_seconds()), 3600)
        m, _ = divmod(rem, 60)
        if not messagebox.askyesno("Confirmar salida", f"Tiempo: {h}h {m}m\nTotal: {total:.2f}\n\n¿Confirmar salida?"):
            return
        closed = self.app.checkout(ticket_id)
        if closed:
            messagebox.showinfo("Salida registrada", f"Ticket #{closed['id']} cerrado. Total: {closed['total']:.2f}")
            self.refresh_everything()


class VehiclesTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Vehículo", padding=10)
        form.grid(row=0, column=0, sticky="ew")
        for i in range(8):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="Placa").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Propietario").grid(row=0, column=2, sticky="w")
        ttk.Label(form, text="Marca").grid(row=0, column=4, sticky="w")
        ttk.Label(form, text="Modelo").grid(row=0, column=6, sticky="w")

        self.placa_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.modelo_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.owner_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.placa_var).grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=4)
        self.owner_cb = ttk.Combobox(form, textvariable=self.owner_var, state="readonly")
        self.owner_cb.grid(row=1, column=2, columnspan=2, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.marca_var).grid(row=1, column=4, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.modelo_var).grid(row=1, column=6, sticky="ew", pady=4)

        ttk.Label(form, text="Color").grid(row=2, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.color_var).grid(row=3, column=0, sticky="ew", padx=(0, 8), pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=3, column=6, sticky="e")
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "placa", "propietario", "marca", "modelo", "color")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        headers = [
            ("id", 60, "center"),
            ("placa", 120, "w"),
            ("propietario", 220, "w"),
            ("marca", 120, "w"),
            ("modelo", 120, "w"),
            ("color", 100, "w"),
        ]
        for c, w, a in headers:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

    def refresh_everything(self):
        owners = [f"{u['id']} - {u['nombre']} ({u['username']})" for u in self.app.users]
        self.owner_cb["values"] = owners
        if owners and not self.owner_var.get():
            self.owner_var.set(owners[0])
        # table
        for item in self.tree.get_children():
            self.tree.delete(item)
        for v in self.app.vehicles:
            owner = next((u for u in self.app.users if u["id"] == v["user_id"]), None)
            owner_txt = f"{owner['nombre']} ({owner['username']})" if owner else "?"
            self.tree.insert("", "end", iid=str(v["id"]), values=(v["id"], v["placa"], owner_txt, v["marca"], v["modelo"], v["color"]))

    def _clear_form(self):
        self._selected_id = None
        self.placa_var.set("")
        self.marca_var.set("")
        self.modelo_var.set("")
        self.color_var.set("")
        if self.owner_cb["values"]:
            self.owner_var.set(self.owner_cb["values"][0])
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        vid = int(sel[0])
        v = next((x for x in self.app.vehicles if x["id"] == vid), None)
        if not v:
            return
        self._selected_id = v["id"]
        self.placa_var.set(v["placa"])
        self.marca_var.set(v["marca"])
        self.modelo_var.set(v["modelo"])
        self.color_var.set(v["color"])
        owner = next((u for u in self.app.users if u["id"] == v["user_id"]), None)
        if owner:
            display = f"{owner['id']} - {owner['nombre']} ({owner['username']})"
            self.owner_var.set(display)

    def _on_add(self):
        placa = self.placa_var.get().strip().upper()
        if not placa:
            messagebox.showwarning("Validación", "Placa obligatoria.")
            return
        if not self.owner_var.get():
            messagebox.showwarning("Validación", "Seleccione propietario.")
            return
        user_id = int(self.owner_var.get().split(" - ")[0])
        v = self.app._create_vehicle(placa, user_id, self.marca_var.get().strip(), self.modelo_var.get().strip(), self.color_var.get().strip())
        if not v:
            messagebox.showerror("Error", "La placa ya existe.")
            return
        self.refresh_everything()
        self._clear_form()

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione un vehículo de la tabla.")
            return
        placa = self.placa_var.get().strip().upper()
        if not placa:
            messagebox.showwarning("Validación", "Placa obligatoria.")
            return
        user_id = int(self.owner_var.get().split(" - ")[0])
        ok = self.app.update_vehicle(self._selected_id, placa, user_id, self.marca_var.get().strip(), self.modelo_var.get().strip(), self.color_var.get().strip())
        if not ok:
            messagebox.showerror("Error", "No se pudo actualizar (placa duplicada).")
            return
        self.refresh_everything()
        self._clear_form()

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione un vehículo de la tabla.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el vehículo seleccionado?"):
            return
        ok = self.app.delete_vehicle(self._selected_id)
        if not ok:
            messagebox.showerror("Error", "No se puede eliminar: ticket activo.")
            return
        self.refresh_everything()
        self._clear_form()


class UsersTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self, text="Usuario", padding=10)
        form.grid(row=0, column=0, sticky="ew")
        for i in range(6):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="Usuario").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Nombre").grid(row=0, column=2, sticky="w")
        ttk.Label(form, text="Contraseña").grid(row=0, column=4, sticky="w")

        self.username_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.username_var).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.nombre_var).grid(row=1, column=2, sticky="ew", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.password_var).grid(row=1, column=4, sticky="ew", pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=1, column=5, sticky="e")
        ttk.Button(btns, text="Agregar", command=self._on_add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Actualizar", command=self._on_update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Limpiar", command=self._clear_form).grid(row=0, column=3, padx=4)

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("id", "usuario", "nombre")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c, w, a in [("id", 60, "center"), ("usuario", 160, "w"), ("nombre", 240, "w")]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self._selected_id = None

    def refresh_everything(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for u in self.app.users:
            self.tree.insert("", "end", iid=str(u["id"]), values=(u["id"], u["username"], u["nombre"]))

    def _clear_form(self):
        self._selected_id = None
        self.username_var.set("")
        self.nombre_var.set("")
        self.password_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        uid = int(sel[0])
        u = next((x for x in self.app.users if x["id"] == uid), None)
        if not u:
            return
        self._selected_id = u["id"]
        self.username_var.set(u["username"])
        self.nombre_var.set(u["nombre"])
        self.password_var.set(u["password"])

    def _on_add(self):
        username = self.username_var.get().strip()
        nombre = self.nombre_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Validación", "Usuario y contraseña obligatorios.")
            return
        if self.app._find_user_by_username(username):
            messagebox.showerror("Error", "El usuario ya existe.")
            return
        self.app._create_user(username, password, nombre or username)
        self.refresh_everything()
        self._clear_form()

    def _on_update(self):
        if not self._selected_id:
            messagebox.showinfo("Actualizar", "Seleccione un usuario.")
            return
        if self.username_var.get().strip() == "admin" and self._selected_id != 1:
            messagebox.showwarning("Validación", "No se puede reasignar el nombre 'admin'.")
            return
        ok = self.app.update_user(self._selected_id, self.username_var.get().strip(), self.password_var.get().strip(), self.nombre_var.get().strip())
        if not ok:
            messagebox.showerror("Error", "No se pudo actualizar (usuario duplicado).")
            return
        self.refresh_everything()
        self._clear_form()

    def _on_delete(self):
        if not self._selected_id:
            messagebox.showinfo("Eliminar", "Seleccione un usuario.")
            return
        if any(u["username"] == "admin" and u["id"] == self._selected_id for u in self.app.users):
            messagebox.showwarning("Validación", "No se puede eliminar el usuario admin.")
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el usuario seleccionado?"):
            return
        ok = self.app.delete_user(self._selected_id)
        if not ok:
            messagebox.showerror("Error", "No se puede eliminar (quizá tiene vehículos).")
            return
        self.refresh_everything()
        self._clear_form()


class ConfigTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        frm = ttk.LabelFrame(self, text="Configuración", padding=12)
        frm.pack(fill="x")

        ttk.Label(frm, text="Tarifa por hora").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Label(frm, text="Capacidad (puestos)").grid(row=0, column=2, sticky="w", padx=(24, 8), pady=4)

        self.rate_var = tk.StringVar()
        self.cap_var = tk.StringVar()

        ttk.Entry(frm, textvariable=self.rate_var, width=12).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frm, textvariable=self.cap_var, width=12).grid(row=1, column=2, sticky="w", padx=(24, 8), pady=4)

        ttk.Button(frm, text="Guardar", command=self._on_save).grid(row=1, column=3, sticky="w", padx=(12, 0), pady=4)

    def refresh_everything(self):
        self.rate_var.set(f"{self.app.rate_per_hour:.2f}")
        self.cap_var.set(str(len(self.app.spots)))

    def _on_save(self):
        try:
            rate = float(self.rate_var.get().replace(",", "."))
            if rate < 0:
                raise ValueError
            cap = int(self.cap_var.get())
            if cap <= 0:
                raise ValueError
            # actualizar
            # primero tarifa
            self.app.rate_per_hour = rate
            # luego capacidad
            if cap != len(self.app.spots):
                self.app._ensure_spots(cap)
            messagebox.showinfo("Configuración", "Configuración guardada.")
            self.parent._update_status()
            self.parent.parking_tab.refresh_everything()
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos para tarifa/capacidad.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class ReportsTab(ttk.Frame):
    def __init__(self, parent: MainFrame):
        super().__init__(parent.nb, padding=10)
        self.app = parent.master
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        cols = ("id", "placa", "puesto", "entrada", "salida", "total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c, w, a in [("id", 60, "center"), ("placa", 120, "w"), ("puesto", 80, "center"), ("entrada", 180, "center"), ("salida", 180, "center"), ("total", 100, "e")]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self.total_var = tk.StringVar(value="Total ingresos: 0.00")
        ttk.Label(footer, textvariable=self.total_var).pack(side="left")
        ttk.Button(footer, text="Actualizar", command=self.refresh_everything).pack(side="right")

    def refresh_everything(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total_sum = 0.0
        for t in self.app.closed_tickets:
            veh = next((v for v in self.app.vehicles if v["id"] == t["vehicle_id"]), None)
            spot = self.app.get_spot_by_id(t["spot_id"]) if t else None
            placa = veh["placa"] if veh else "?"
            puesto = spot["codigo"] if spot else "?"
            entrada = t["checkin"].strftime("%Y-%m-%d %H:%M:%S")
            salida = t["checkout"].strftime("%Y-%m-%d %H:%M:%S")
            total_sum += float(t["total"]) if t.get("total") else 0.0
            self.tree.insert("", "end", iid=str(t["id"]), values=(t["id"], placa, puesto, entrada, salida, f"{t['total']:.2f}"))
        self.total_var.set(f"Total ingresos: {total_sum:.2f}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
