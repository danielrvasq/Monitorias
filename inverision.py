#!/usr/bin/env python3
"""
Simulador de inversión con aportes mensuales e interés compuesto

Ejemplos de uso:
    python inversion_simulator.py --monto 1000 --aporte 200 --tasa 10 --meses 12
    python inversion_simulator.py --example

Este programa calcula cómo crece una inversión con aportes mensuales,
considerando una tasa de interés compuesta mensual.
"""
import sys


def calcular_crecimiento(monto_inicial, aporte_mensual, tasa_anual_pct, meses):
    """Calcula el saldo final y el detalle mes a mes.

    monto_inicial: capital inicial
    aporte_mensual: dinero que se agrega cada mes
    tasa_anual_pct: tasa anual en porcentaje
    meses: cantidad de meses
    """
    if meses <= 0:
        raise ValueError("El número de meses debe ser mayor que 0")
    if tasa_anual_pct < 0:
        raise ValueError("La tasa no puede ser negativa")

    r = tasa_anual_pct / 100 / 12  # tasa mensual
    saldo = monto_inicial
    historial = []

    for m in range(1, meses + 1):
        interes = saldo * r
        saldo += interes + aporte_mensual
        historial.append((m, interes, aporte_mensual, saldo))

    return saldo, historial


def imprimir_tabla(historial):
    """Muestra la tabla de evolución de la inversión."""
    print(f"{'Mes':>3}  {'Interés':>10}  {'Aporte':>10}  {'Saldo':>12}")
    print("-" * 45)
    for mes, interes, aporte, saldo in historial:
        print(f"{mes:3d}  {interes:10.2f}  {aporte:10.2f}  {saldo:12.2f}")


def main():
    """Modo de uso sencillo sin argparse."""
    args = sys.argv[1:]
    ejemplo = "--example" in args

    pos = [a for a in args if not a.startswith("-")]

    if ejemplo:
        monto = 1000.0
        aporte = 200.0
        tasa = 10.0
        meses = 12
        print("Ejemplo: monto inicial=1000, aporte mensual=200, tasa=10%, meses=12")
    elif len(pos) >= 4:
        try:
            monto = float(pos[0])
            aporte = float(pos[1])
            tasa = float(pos[2])
            meses = int(float(pos[3]))
        except Exception:
            print("Error en los argumentos. Usando valores por defecto.")
            monto, aporte, tasa, meses = 1000, 200, 10, 12
    else:
        # modo interactivo
        try:
            monto = float(input("Monto inicial [1000]: ") or 1000)
            aporte = float(input("Aporte mensual [200]: ") or 200)
            tasa = float(input("Tasa anual % [10]: ") or 10)
            meses = int(input("Meses [12]: ") or 12)
        except Exception:
            print("Entrada no válida. Usando valores por defecto.")
            monto, aporte, tasa, meses = 1000, 200, 10, 12

    saldo_final, historial = calcular_crecimiento(monto, aporte, tasa, meses)

    total_aportado = monto + aporte * meses
    ganancia = saldo_final - total_aportado

    print("\nResumen de la inversión:")
    print(f"Monto inicial: {monto:,.2f}")
    print(f"Aporte mensual: {aporte:,.2f}")
    print(f"Tasa anual: {tasa:.2f}%")
    print(f"Plazo: {meses} meses")
    print(f"Saldo final: {saldo_final:,.2f}")
    print(f"Total aportado: {total_aportado:,.2f}")
    print(f"Ganancia total: {ganancia:,.2f}")

    print()
    imprimir_tabla(historial)


if __name__ == "__main__":
    main()
