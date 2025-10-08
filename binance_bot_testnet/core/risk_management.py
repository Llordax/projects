# =============================================================================
# MÓDULO: risk_management.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo define las funciones de **gestión de riesgo** utilizadas por el bot.
# 
# Su objetivo principal es calcular de forma precisa los niveles de precios
# de **Take Profit (TP)** y **Stop Loss (SL)** basados en porcentajes configurados
# en la estrategia.
#
# Estos niveles permiten establecer márgenes de beneficio y límites de pérdida
# automáticos para cada operación ejecutada.
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES:
#   ✅ Calcular múltiplos niveles de Take Profit.
#   ✅ Calcular múltiplos niveles de Stop Loss.
#   ✅ Permitir configuración flexible mediante porcentajes de entrada.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from typing import List, Tuple


# =============================================================================
# 🎯 FUNCIÓN: Cálculo de niveles de Take Profit (TP) y Stop Loss (SL)
# =============================================================================
def compute_tp_sl(entry_price: float, tp_pcts: List[float], sl_pcts: List[float]) -> Tuple[List[float], List[float]]:
    """
    Calcula los niveles de **Take Profit (TP)** y **Stop Loss (SL)** para una operación.

    A partir del precio de entrada (`entry_price`), esta función genera los precios
    objetivo para las salidas con ganancia (TP) y los niveles de protección ante
    pérdida (SL), utilizando los porcentajes definidos en la estrategia.

    Args:
        entry_price (float): Precio de entrada de la operación.
        tp_pcts (List[float]): Lista de porcentajes de ganancia para cada nivel de TP.
            Ejemplo: [0.015, 0.03, 0.045] → TP1 = +1.5%, TP2 = +3%, TP3 = +4.5%.
        sl_pcts (List[float]): Lista de porcentajes de pérdida para cada nivel de SL.
            Ejemplo: [0.005, 0.01, 0.015] → SL1 = -0.5%, SL2 = -1%, SL3 = -1.5%.

    Returns:
        Tuple[List[float], List[float]]:
            - **tps**: Lista de precios de Take Profit.
            - **sls**: Lista de precios de Stop Loss.

    Ejemplo:
        >>> compute_tp_sl(30000, [0.015, 0.03], [0.01, 0.02])
        ([30450.0, 30900.0], [29700.0, 29400.0])

    Notas:
        - Los cálculos se realizan mediante incrementos y decrementos porcentuales
          sobre el precio de entrada.
        - Las listas `tp_pcts` y `sl_pcts` deben tener la misma longitud si se
          desean niveles simétricos.
    """
    # Calcular precios de Take Profit sumando el porcentaje al precio de entrada
    tps = [entry_price * (1 + pct) for pct in tp_pcts]

    # Calcular precios de Stop Loss restando el porcentaje al precio de entrada
    sls = [entry_price * (1 - pct) for pct in sl_pcts]

    # Devolver ambas listas como tupla (TPs, SLs)
    return tps, sls
