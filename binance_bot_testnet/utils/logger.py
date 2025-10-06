import os
import pandas as pd
from datetime import datetime

# Ruta del Excel donde se guarda el historial
FILE_PATH = "excel/trades_history.xlsx"

# Crear carpeta si no existe
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

# Columnas estándar del log
COLUMNS = [
    "timestamp", "order_id", "ticker", "order_type",
    "qty", "price_open", "price_sl", "price_tp",
    "price_closed", "pnl"
]

def log_trade(order_id, ticker, order_type, qty, price_open, price_sl, price_tp, price_closed, pnl):
    """Agrega una operación al Excel de historial"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
        "pnl": pnl
    }])

    if os.path.exists(FILE_PATH):
        df_existing = pd.read_excel(FILE_PATH)
        df_updated = pd.concat([df_existing, new_trade], ignore_index=True)
    else:
        df_updated = new_trade

    df_updated.to_excel(FILE_PATH, index=False)
