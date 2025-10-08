# =============================================================================
# MÓDULO: logger.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo se encarga del **registro de operaciones (trades)** ejecutadas por el bot.
#
# Cada operación se guarda en un archivo Excel (`excel/trades_history.xlsx`), lo que 
# permite mantener un historial estructurado de las operaciones realizadas.
# 
# El registro incluye información clave:
#   - ID de la orden ejecutada.
#   - Símbolo del activo (ticker).
#   - Tipo de orden (buy/sell/TP/SL).
#   - Cantidad operada y precios (entrada, SL, TP, cierre).
#   - Resultado de la operación (PnL).
#
# Además de almacenarse en el Excel, cada evento también se registra en los logs
# generales del bot mediante el sistema de `logger_setup.py`.
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES PRINCIPALES:
#   ✅ Crear automáticamente el archivo y directorios si no existen.
#   ✅ Agregar cada nueva operación al historial sin sobrescribir las anteriores.
#   ✅ Normalizar el valor del PnL (positivo = ganancia, negativo = pérdida).
#   ✅ Reportar todas las acciones mediante el logger global.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - pandas (para manipulación del historial Excel)
#   - os (para manejo de rutas)
#   - datetime (para marca temporal)
#   - utils.logger_setup.logger (para registrar eventos)
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import os
import pandas as pd
from datetime import datetime
from utils.logger_setup import logger


# =============================================================================
# 📂 CONFIGURACIÓN DE RUTA Y ESTRUCTURA DE ARCHIVO
# =============================================================================
FILE_PATH = "excel/trades_history.xlsx"  # Ruta del archivo Excel de historial
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)  # Crear carpeta /excel si no existe


# =============================================================================
# 🧾 ESTRUCTURA DE COLUMNAS DEL HISTORIAL
# =============================================================================
COLUMNS = [
    "timestamp", "order_id", "ticker", "order_type",
    "qty", "price_open", "price_sl", "price_tp",
    "price_closed", "pnl"
]


# =============================================================================
# 🧮 FUNCIÓN: Registrar una operación (trade)
# =============================================================================
def log_trade(order_id, ticker, order_type, qty, price_open, price_sl, price_tp, price_closed, pnl):
    """
    Registra una operación ejecutada en un archivo Excel.

    La función agrega una nueva fila al archivo de historial (`trades_history.xlsx`),
    incluyendo los datos relevantes de la operación: precios, cantidades, tipo de orden
    y resultado financiero (PnL). Si el archivo no existe, lo crea automáticamente.

    Args:
        order_id (str | int): Identificador único de la orden ejecutada.
        ticker (str): Par de trading (por ejemplo, "BTCEUR").
        order_type (str): Tipo de operación ("buy", "sell", "TP", "SL", etc.).
        qty (float): Cantidad de activo operada.
        price_open (float): Precio de apertura o compra.
        price_sl (float): Nivel de Stop Loss.
        price_tp (float): Nivel de Take Profit.
        price_closed (float): Precio al que se cerró la operación.
        pnl (float): Beneficio o pérdida de la operación.

    Ejemplo:
        >>> log_trade(
        ...     order_id=12345,
        ...     ticker="BTCEUR",
        ...     order_type="buy",
        ...     qty=0.01,
        ...     price_open=30000,
        ...     price_sl=29500,
        ...     price_tp=30500,
        ...     price_closed=30400,
        ...     pnl=40.0
        ... )
    """
    # 📅 Registrar timestamp UTC del evento
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Normalizar el PnL (positivo = ganancia, negativo = pérdida)
    pnl_value = abs(pnl) if pnl >= 0 else -abs(pnl)

    # Crear un nuevo registro en formato DataFrame
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
        "pnl": pnl_value
    }])

    try:
        # 📂 Si el archivo ya existe, cargar su contenido y añadir la nueva operación
        if os.path.exists(FILE_PATH):
            df_existing = pd.read_excel(FILE_PATH)
            df_updated = pd.concat([df_existing, new_trade], ignore_index=True)
            logger.info(f"📘 Archivo existente cargado: {FILE_PATH}")
        else:
            # 🆕 Crear nuevo archivo de historial si no existe
            df_updated = new_trade
            logger.info(f"🆕 Creando nuevo archivo de historial: {FILE_PATH}")

        # Guardar el DataFrame actualizado en Excel
        df_updated.to_excel(FILE_PATH, index=False)
        logger.info(f"✅ Operación {order_id} registrada correctamente en {FILE_PATH}")

        # Confirmar visualmente en consola
        print(f"🧾 Operación registrada: {ticker} ({order_type}) — PnL: {pnl_value:.2f}")

    except Exception as e:
        # Manejo de errores durante el guardado del historial
        logger.error(f"❌ Error al registrar operación {order_id}: {e}")
        print(f"❌ Error al registrar operación: {e}")
        raise
