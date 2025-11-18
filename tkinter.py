#!/usr/bin/env python3
"""
Simulador de ahorro con interés compuesto
-----------------------------------------
Este programa permite al usuario calcular la evolución de un ahorro con interés
compuesto y aportes mensuales, usando una interfaz gráfica en Tkinter.

El usuario puede:
- Ingresar monto inicial, tasa anual, meses y aporte mensual.
- Ver los resultados calculados.
- Mostrar la tabla de evolución del saldo mes a mes.
"""

import tkinter as tk
from tkinter import ttk, messagebox


def calcular_crecimiento(monto_inicial, aporte_mensual, tasa_anual_pct, meses):
    """Calcula la evolución mes a mes del ahorro con interés compuesto."""
    if meses <= 0:
        raise ValueError("El número de meses debe ser mayor que 0")
    if tasa_anual_pct < 0:
        raise ValueError("La tasa no puede ser negativa")

    r = tasa_anual_pct / 100 / 12
    saldo = monto_inicial
    historial = []

    for m in range(1, meses + 1):
        interes = saldo * r
        saldo += interes + aporte_mensual
        historial.append((m, interes, aporte_mensual, saldo))

    return saldo, historial


class SimuladorAhorroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Ahorro con Interés Compuesto")
        self.root.geometry("720x520")
        self.root.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):
        frame_inputs = tk.Frame(self.root, padx=10, pady=10)
        frame_inputs.pack(fill="x")

        # Etiquetas y campos de entrada
        tk.Label(frame_inputs, text="Monto inicial:").grid(row=0, column=0, sticky="w")
        self.entry_monto = tk.Entry(frame_inputs)
        self.entry_monto.insert(0, "1000")
        self.entry_monto.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frame_inputs, text="Aporte mensual:").grid(row=1, column=0, sticky="w")
        self.entry_aporte = tk.Entry(frame_inputs)
        self.entry_aporte.insert(0, "200")
        self.entry_aporte.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(frame_inputs, text="Tasa anual (%):").grid(row=2, column=0, sticky="w")
        self.entry_tasa = tk.Entry(frame_inputs)
        self.entry_tasa.insert(0, "10")
        self.entry_tasa.grid(row=2, column=1, padx=5, pady=3)

        tk.Label(frame_inputs, text="Meses:").grid(row=3, column=0, sticky="w")
        self.entry_meses = tk.Entry(frame_inputs)
        self.entry_meses.insert(0, "12")
        self.entry_meses.grid(row=3, column=1, padx=5, pady=3)

        # Botón de cálculo
        tk.Button(frame_inputs, text="Calcular", command=self.calcular).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Marco de resultados
        self.frame_result = tk.LabelFrame(self.root, text="Resumen", padx=10, pady=10)
        self.frame_result.pack(fill="x", padx=10, pady=5)

        self.label_resultado = tk.Label(
            self.frame_result, text="", justify="left", font=("Arial", 10)
        )
        self.label_resultado.pack(anchor="w")

        # Tabla
        self.frame_tabla = tk.LabelFrame(self.root, text="Evolución mensual", padx=10, pady=10)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("Mes", "Interés", "Aporte", "Saldo")
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings", height=10
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=120)

        self.tabla.pack(fill="both", expand=True)

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def calcular(self):
        try:
            monto = float(self.entry_monto.get())
            aporte = float(self.entry_aporte.get())
            tasa = float(self.entry_tasa.get())
            meses = int(self.entry_meses.get())

            saldo_final, historial = calcular_crecimiento(monto, aporte, tasa, meses)
            total_aportado = monto + aporte * meses
            ganancia = saldo_final - total_aportado

            resumen = (
                f"Monto inicial: ${monto:,.2f}\n"
                f"Aporte mensual: ${aporte:,.2f}\n"
                f"Tasa anual: {tasa:.2f}%\n"
                f"Plazo: {meses} meses\n"
                f"Saldo final: ${saldo_final:,.2f}\n"
                f"Total aportado: ${total_aportado:,.2f}\n"
                f"Ganancia total: ${ganancia:,.2f}"
            )
            self.label_resultado.config(text=resumen)

            # Limpiar tabla antes de agregar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            # Insertar nueva información
            for mes, interes, aporte_m, saldo in historial:
                self.tabla.insert("", "end", values=(mes, f"{interes:.2f}", f"{aporte_m:.2f}", f"{saldo:.2f}"))

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAhorroApp(root)
    root.mainloop()
