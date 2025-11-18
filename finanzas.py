#!/usr/bin/env python3
"""
Gestor de gastos personales
----------------------------
Aplicación con interfaz gráfica Tkinter que permite:
- Registrar ingresos y gastos.
- Calcular el balance total.
- Mostrar los registros en una tabla dinámica.
- Graficar el total de ingresos y gastos (usando matplotlib, si está disponible).

Requisitos opcionales:
    pip install matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Intentamos importar matplotlib (opcional)
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GestorGastosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Gastos Personales")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        # Lista para almacenar transacciones
        self.transacciones = []

        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz principal de la aplicación"""
        frame_superior = tk.LabelFrame(self.root, text="Registrar Transacción", padx=10, pady=10)
        frame_superior.pack(fill="x", padx=10, pady=10)

        # Campos de entrada
        tk.Label(frame_superior, text="Descripción:").grid(row=0, column=0, sticky="w")
        self.entry_desc = tk.Entry(frame_superior, width=40)
        self.entry_desc.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frame_superior, text="Monto:").grid(row=1, column=0, sticky="w")
        self.entry_monto = tk.Entry(frame_superior)
        self.entry_monto.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(frame_superior, text="Tipo:").grid(row=2, column=0, sticky="w")
        self.tipo_var = tk.StringVar(value="Gasto")
        ttk.Combobox(frame_superior, textvariable=self.tipo_var, values=["Gasto", "Ingreso"], width=37).grid(
            row=2, column=1, padx=5, pady=3
        )

        tk.Label(frame_superior, text="Categoría:").grid(row=3, column=0, sticky="w")
        self.entry_categoria = tk.Entry(frame_superior)
        self.entry_categoria.insert(0, "General")
        self.entry_categoria.grid(row=3, column=1, padx=5, pady=3)

        tk.Button(frame_superior, text="Agregar", command=self.agregar_transaccion, bg="#4CAF50", fg="white").grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Tabla de registros
        frame_tabla = tk.LabelFrame(self.root, text="Historial de Transacciones", padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("Fecha", "Descripción", "Categoría", "Tipo", "Monto")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=150)

        self.tabla.pack(fill="both", expand=True)

        # Barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Resumen inferior
        frame_resumen = tk.LabelFrame(self.root, text="Resumen Financiero", padx=10, pady=10)
        frame_resumen.pack(fill="x", padx=10, pady=5)

        self.label_ingresos = tk.Label(frame_resumen, text="Total ingresos: $0.00", fg="green", font=("Arial", 10, "bold"))
        self.label_ingresos.grid(row=0, column=0, padx=10)

        self.label_gastos = tk.Label(frame_resumen, text="Total gastos: $0.00", fg="red", font=("Arial", 10, "bold"))
        self.label_gastos.grid(row=0, column=1, padx=10)

        self.label_balance = tk.Label(frame_resumen, text="Balance: $0.00", fg="blue", font=("Arial", 10, "bold"))
        self.label_balance.grid(row=0, column=2, padx=10)

        tk.Button(frame_resumen, text="Eliminar selección", command=self.eliminar_transaccion, bg="#f44336", fg="white").grid(
            row=1, column=0, columnspan=1, pady=5
        )

        tk.Button(frame_resumen, text="Mostrar gráfica", command=self.mostrar_grafica, bg="#2196F3", fg="white").grid(
            row=1, column=1, columnspan=2, pady=5
        )

    def agregar_transaccion(self):
        """Agrega una transacción a la tabla y la lista"""
        desc = self.entry_desc.get().strip()
        categoria = self.entry_categoria.get().strip()
        tipo = self.tipo_var.get()

        try:
            monto = float(self.entry_monto.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        if not desc:
            messagebox.showwarning("Atención", "Por favor ingresa una descripción.")
            return

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.transacciones.append({
            "fecha": fecha,
            "descripcion": desc,
            "categoria": categoria,
            "tipo": tipo,
            "monto": monto
        })

        self.tabla.insert("", "end", values=(fecha, desc, categoria, tipo, f"${monto:,.2f}"))
        self.entry_desc.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)

        self.actualizar_resumen()

    def eliminar_transaccion(self):
        """Elimina la transacción seleccionada en la tabla"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una fila para eliminar.")
            return

        indice = self.tabla.index(seleccion[0])
        self.tabla.delete(seleccion)
        self.transacciones.pop(indice)
        self.actualizar_resumen()

    def actualizar_resumen(self):
        """Recalcula totales y actualiza etiquetas"""
        total_ingresos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "Ingreso")
        total_gastos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "Gasto")
        balance = total_ingresos - total_gastos

        self.label_ingresos.config(text=f"Total ingresos: ${total_ingresos:,.2f}")
        self.label_gastos.config(text=f"Total gastos: ${total_gastos:,.2f}")
        self.label_balance.config(text=f"Balance: ${balance:,.2f}")

        # Cambiar color según balance
        self.label_balance.config(fg="green" if balance >= 0 else "red")

    def mostrar_grafica(self):
        """Muestra una gráfica simple de ingresos vs gastos"""
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Matplotlib no está instalado.\nEjecuta: pip install matplotlib")
            return

        total_ingresos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "Ingreso")
        total_gastos = sum(t["monto"] for t in self.transacciones if t["tipo"] == "Gasto")

        if total_ingresos == 0 and total_gastos == 0:
            messagebox.showinfo("Información", "No hay datos para graficar.")
            return

        etiquetas = ["Ingresos", "Gastos"]
        valores = [total_ingresos, total_gastos]
        colores = ["#4CAF50", "#f44336"]

        plt.figure("Gráfica Financiera")
        plt.bar(etiquetas, valores, color=colores)
        plt.title("Distribución de Ingresos y Gastos")
        plt.ylabel("Monto ($)")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestorGastosApp(root)
    root.mainloop()
