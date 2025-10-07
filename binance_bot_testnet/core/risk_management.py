"""
Módulo de gestión de riesgo.

Contiene funciones para calcular los niveles de precios de
Take Profit (TP) y Stop Loss (SL) basados en porcentajes definidos.
"""

from typing import List, Tuple

def compute_tp_sl(entry_price, tp_pcts, sl_pcts):
    """Calcula los niveles de Take Profit (TP) y Stop Loss (SL).

    A partir del precio de entrada (`entry_price`), esta función calcula los
    precios objetivo para las salidas con ganancia (TP) y los niveles de
    protección ante pérdida (SL) en base a porcentajes configurados.

    Args:
        entry_price (float): Precio de entrada de la operación.
        tp_pcts (List[float]): Lista de porcentajes de ganancia para cada TP.
            Ejemplo: [0.015, 0.03, 0.045] → TP1=+1.5%, TP2=+3%, TP3=+4.5%.
        sl_pcts (List[float]): Lista de porcentajes de pérdida para cada SL.
            Ejemplo: [0.005, 0.01, 0.015] → SL1=-0.5%, SL2=-1%, SL3=-1.5%.

    Returns:
        Tuple[List[float], List[float]]:
            - Lista de precios de Take Profit.
            - Lista de precios de Stop Loss.

    Ejemplo:
        >>> compute_tp_sl(30000, [0.015, 0.03], [0.01, 0.02])
        ([30450.0, 30900.0], [29700.0, 29400.0])
    """
    tps = [entry_price * (1 + pct) for pct in tp_pcts]
    sls = [entry_price * (1 - pct) for pct in sl_pcts]
    return tps, sls
