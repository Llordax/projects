# =============================================================================
# MÓDULO: logger.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# ----------------------------------------------------------------------------- 
# Registra todas las operaciones (trades) en un archivo Excel, incluyendo:
#   - Precios de entrada, SL, TP y cierre.
#   - Resultado (PnL).
#   - 💰 Capital invertido y capital recuperado.
# ----------------------------------------------------------------------------- 
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import os
import pandas as pd
from datetime import datetime
from utils.logger_setup import logger

FILE_PATH = "excel/trades_history.xlsx"
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

COLUMNS = [
    "timestamp", "order_id", "ticker", "order_type",
    "qty", "price_open", "price_sl", "price_tp",
    "price_closed", "pnl",
    "capital_inicial", "capital_final"  # 🆕 NUEVAS COLUMNAS
]


def log_trade(order_id, ticker, order_type, qty, price_open, price_sl, price_tp, price_closed, pnl):
    """Registra una operación ejecutada en Excel con capital inicial y final."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Calcular capital invertido y recuperado
    capital_inicial = qty * price_open
    capital_final = (qty * price_closed) if price_closed else 0.0

    pnl_value = abs(pnl) if pnl >= 0 else -abs(pnl)

    new_trade = pd.DataFrame([{
        "timestamp": timestamp,
        "order_id": order_id,
        "ticker": ticker,
        "order_type": order_type,
        "qty": qty,
        "price_open": price_open,
        "price_sl": price_sl,
        "price_tp": price_tp,
        "price_closed": price_closed,
        "pnl": pnl_value,
        "capital_inicial": capital_inicial,
        "capital_final": capital_final
    }])

    try:
        if os.path.exists(FILE_PATH):
            df_existing = pd.read_excel(FILE_PATH)
            df_updated = pd.concat([df_existing, new_trade], ignore_index=True)
        else:
            df_updated = new_trade

        df_updated.to_excel(FILE_PATH, index=False)
        logger.info(f"✅ Operación {order_id} registrada correctamente en {FILE_PATH}")
        print(f"🧾 Operación registrada: {ticker} ({order_type}) — PnL: {pnl_value:.2f}")

    except Exception as e:
        logger.error(f"❌ Error al registrar operación {order_id}: {e}")
        print(f"❌ Error al registrar operación: {e}")
