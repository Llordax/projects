# =============================================================================
# MÓDULO: risk_management.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Calcula los niveles de Take Profit (TP) y Stop Loss (SL) para una operación.
# En esta versión scalper, solo hay un TP y un SL.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from typing import List, Tuple

def compute_tp_sl(entry_price: float, tp_pcts: List[float], sl_pcts: List[float]) -> Tuple[List[float], List[float]]:
    """Calcula los precios de TP y SL a partir del precio de entrada."""
    tps = [entry_price * (1 + pct) for pct in tp_pcts]
    sls = [entry_price * (1 - pct) for pct in sl_pcts]
    return tps, sls
