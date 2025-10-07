"""
Módulo de registro de operaciones (trades) ejecutadas por el bot.

Proporciona funciones para registrar cada operación en un archivo Excel o CSV,
manteniendo un historial que permite analizar el rendimiento de la estrategia.

Cada operación registrada incluye información clave como:
    - ID de la orden
    - Símbolo de trading
    - Tipo de orden (compra/venta)
    - Cantidad y precios de entrada/salida
    - Niveles de Take Profit y Stop Loss
    - Beneficio o pérdida (PnL)

Los registros también se reportan mediante el sistema de logging general del bot.
"""

import os
import pandas as pd
from datetime import datetime
from utils.logger_setup import logger

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
    """Registra una operación ejecutada en un archivo Excel.

    Si el archivo no existe, se crea automáticamente con las columnas adecuadas.
    Cada nueva operación se agrega como una nueva fila al final del archivo.

    Args:
        order_id (str): Identificador único de la orden.
        ticker (str): Símbolo de trading (por ejemplo, "BTCUSDT").
        order_type (str): Tipo de orden ("buy" o "sell").
        qty (float): Cantidad de la operación.
        price_open (float): Precio de entrada.
        price_sl (float): Nivel de stop-loss asociado.
        price_tp (float): Nivel de take-profit asociado.
        price_closed (float): Precio al momento de cerrar la operación.
        pnl (float): Ganancia o pérdida (Profit and Loss).

    Raises:
        Exception: Si ocurre un error al guardar el registro.
    """
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

    try:
        if os.path.exists(FILE_PATH):
            df_existing = pd.read_excel(FILE_PATH)
            df_updated = pd.concat([df_existing, new_trade], ignore_index=True)
            logger.info(f"📘 Archivo existente cargado: {FILE_PATH}")
        else:
            df_updated = new_trade
            logger.info(f"🆕 Creando nuevo archivo de historial: {FILE_PATH}")

        df_updated.to_excel(FILE_PATH, index=False)
        logger.info(f"✅ Operación {order_id} registrada correctamente en {FILE_PATH}")
        print(f"🧾 Operación registrada: {ticker} ({order_type}) — PnL: {pnl:.2f}")

    except Exception as e:
        logger.error(f"❌ Error al registrar operación {order_id}: {e}")
        print(f"❌ Error al registrar operación: {e}")
        raise
