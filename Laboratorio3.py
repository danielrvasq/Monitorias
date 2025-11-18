#!/usr/bin/env python3
"""
Simulador de crédito / préstamo

Ejemplos de uso:
    python simulator.py --principal 10000 --rate 12 --months 24
    python simulator.py --example

Este script calcula la cuota mensual de un préstamo con pago fijo (anualidad)
y puede mostrar el cuadro de amortización mes a mes.
"""
import sys


def cuota_mensual(principal, tasa_anual_pct, meses):
    """Calcula la cuota mensual (anualidad) de forma sencilla.

    principal: monto del préstamo
    tasa_anual_pct: tasa anual en porcentaje (ej. 12)
    meses: número de meses
    """
    if meses <= 0:
        raise ValueError("El número de meses debe ser mayor que 0")
    if tasa_anual_pct == 0:
        return principal / meses
    r = tasa_anual_pct / 100.0 / 12.0
    return principal * r / (1 - (1 + r) ** (-meses))


def imprimir_amortizacion(principal, tasa_anual_pct, meses, cuota):
    """Imprime el cuadro de amortización usando solo operaciones básicas.
    No usa tipos ni estructuras complejas, solo un bucle y prints.
    """
    r = tasa_anual_pct / 100.0 / 12.0
    saldo = principal
    print(f"{'Mes':>3}  {'Pago':>10}  {'Interés':>10}  {'Capital':>10}  {'Saldo':>12}")
    print("-" * 55)
    for m in range(1, meses + 1):
        interes = saldo * r
        capital_pagado = cuota - interes
        # en la última cuota ajustamos para evitar pequeños saldos negativos
        if m == meses:
            capital_pagado = saldo
            cuota_real = interes + capital_pagado
            saldo = 0.0
        else:
            saldo = saldo - capital_pagado
            cuota_real = cuota
            if saldo < 1e-8:
                saldo = 0.0

        print(f"{m:3d}  {cuota_real:10.2f}  {interes:10.2f}  {capital_pagado:10.2f}  {saldo:12.2f}")


def main() -> None:
    """Uso sencillo sin argparse.

    Formas de usar:
    - `python simulator.py --example`  -> usa valores de demostración
    - `python simulator.py PRINCIPAL TASA MESES` -> argumentos posicionales (ignorando flags)
    - `python simulator.py` -> modo interactivo pidiendo valores por teclado
    - puede añadirse `--no-schedule` para no mostrar el cuadro de amortización
    """
    args = sys.argv[1:]
    ejemplo = "--example" in args
    no_schedule = "--no-schedule" in args

    # extraer argumentos posicionales (los que no empiezan con '-')
    pos = [a for a in args if not a.startswith("-")]

    if ejemplo:
        principal = 15000.0
        rate = 11.5
        months = 36
        print("Ejemplo: principal=15000, tasa=11.5%, meses=36")
    elif len(pos) >= 3:
        # tomar los tres primeros valores posicionales
        try:
            principal = float(pos[0])
        except Exception:
            principal = 10000.0
        try:
            rate = float(pos[1])
        except Exception:
            rate = 12.0
        try:
            months = int(float(pos[2]))
        except Exception:
            months = 12
    else:
        # modo interactivo sencillo
        try:
            raw = input("Principal (monto) [10000]: ")
            principal = float(raw) if raw.strip() else 10000.0
            raw = input("Tasa anual % [12]: ")
            rate = float(raw) if raw.strip() else 12.0
            raw = input("Plazo en meses [12]: ")
            months = int(raw) if raw.strip() else 12
        except Exception:
            print("Entrada no válida; usando valores por defecto.")
            principal = 10000.0
            rate = 12.0
            months = 12

    cuota = cuota_mensual(principal, rate, months)
    pago_total = cuota * months
    interes_total = pago_total - principal

    print("\nResumen:")
    print("Principal: {:,.2f}".format(principal))
    print("Tasa anual: {:.3f}%".format(rate))
    print("Plazo: {} meses".format(months))
    print("Pago mensual: {:,.2f}".format(cuota))
    print("Pago total: {:,.2f}".format(pago_total))
    print("Interés total: {:,.2f}".format(interes_total))

    if not no_schedule:
        print()
        imprimir_amortizacion(principal, rate, months, cuota)


if __name__ == "__main__":
    main()
