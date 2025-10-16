# =============================================================================
# MÓDULO: logger.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo se encarga de registrar todas las operaciones ejecutadas por el bot
# en un archivo Excel (formato .xlsx). Cada registro incluye:
#   - ID único de la orden.
#   - Tipo de operación (LONG, SHORT, TP, SL, etc.).
#   - Precios de entrada, TP y SL.
#   - Resultado económico (PnL).
#   - Capital invertido y capital recuperado.
#   - Timestamp UTC del registro.
#
# 💡 Características clave:
#   ✅ Escritura segura mediante Lock global → evita corrupción del archivo Excel.
#   ✅ Compatible con operaciones paralelas (múltiples hilos).
#   ✅ Creación automática de carpeta /excel si no existe.
#   ✅ Registros ordenados con timestamps precisos.
#
# ⚙️ Funcionamiento:
#   - Cada vez que una operación se ejecuta o cierra (TP/SL),
#     el bot llama a `log_trade()` para registrar el resultado.
#   - La escritura en Excel está protegida con `_excel_lock` para impedir accesos simultáneos.
#   - Si el archivo no existe, se crea con las columnas definidas.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import os
import pandas as pd
from datetime import datetime
from threading import Lock
from utils.logger_setup import logger


# =============================================================================
# 📂 CONFIGURACIÓN DE ARCHIVO DE SALIDA
# =============================================================================
FILE_PATH = "excel/trades_history.xlsx"
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

# Columnas del Excel de historial de operaciones
COLUMNS = [
    "timestamp", "order_id", "ticker", "order_type",
    "qty", "price_open", "price_sl", "price_tp",
    "price_closed", "pnl",
    "capital_inicial", "capital_final"
]


# =============================================================================
# 🔒 LOCK GLOBAL DE SINCRONIZACIÓN
# =============================================================================
# Este lock garantiza que solo un hilo acceda a escribir en el archivo Excel
# al mismo tiempo, evitando errores de escritura simultánea o corrupción de datos.
_excel_lock = Lock()


# =============================================================================
# 🧾 FUNCIÓN PRINCIPAL: Registrar una operación en Excel
# =============================================================================
def log_trade(order_id, ticker, order_type, qty, price_open, price_sl, price_tp, price_closed, pnl):
    """
    Registra una operación ejecutada en el archivo Excel.

    Args:
        order_id (str): ID único de la orden o simulación (por ejemplo, 'SIMULATED_LONG_1234').
        ticker (str): Par de trading, p.ej. "BTCEUR".
        order_type (str): Tipo de operación ("LONG", "SHORT", "TP_LONG", "SL_SHORT", etc.).
        qty (float): Cantidad total del activo operado.
        price_open (float): Precio de entrada.
        price_sl (float): Nivel de Stop Loss configurado.
        price_tp (float): Nivel de Take Profit configurado.
        price_closed (float | None): Precio de cierre (TP/SL alcanzado). Puede ser None si la operación está abierta.
        pnl (float): Beneficio o pérdida de la operación (positivo o negativo).

    Funcionalidad:
        - Calcula el capital inicial (qty * precio de entrada).
        - Calcula el capital final (qty * precio de cierre).
        - Asegura acceso exclusivo al archivo mediante Lock global.
        - Si el archivo no existe, lo crea con las columnas base.
        - Registra la operación y guarda el archivo actualizado.
    """
    # -------------------------------------------------------------------------
    # 🕒 Generar timestamp UTC
    # -------------------------------------------------------------------------
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------------------------------------------------------
    # 💰 Calcular métricas financieras
    # -------------------------------------------------------------------------
    capital_inicial = qty * price_open
    capital_final = (qty * price_closed) if price_closed else 0.0
    pnl_value = abs(pnl) if pnl >= 0 else -abs(pnl)

    # Crear DataFrame con la nueva operación
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

    # -------------------------------------------------------------------------
    # 🔒 Escritura protegida por Lock
    # -------------------------------------------------------------------------
    with _excel_lock:
        try:
            # Leer archivo existente si ya fue creado
            if os.path.exists(FILE_PATH):
                df_existing = pd.read_excel(FILE_PATH)
                df_updated = pd.concat([df_existing, new_trade], ignore_index=True)
            else:
                # Crear nuevo archivo si no existe
                df_updated = new_trade

            # Guardar el Excel actualizado
            df_updated.to_excel(FILE_PATH, index=False)

            logger.info(f"✅ Operación {order_id} registrada correctamente en {FILE_PATH}")
            print(f"🧾 Operación registrada: {ticker} ({order_type}) — PnL: {pnl_value:.2f}")

        except Exception as e:
            logger.error(f"❌ Error al registrar operación {order_id}: {e}")
            print(f"❌ Error al registrar operación: {e}")


# =============================================================================
# 📊 FUNCIÓN OPCIONAL: Inicializar archivo vacío (si se desea limpiar el histórico)
# =============================================================================
def initialize_trade_history():
    """
    Crea (o reinicia) el archivo de historial con las columnas base.
    Se puede usar manualmente antes de iniciar una sesión nueva.
    """
    with _excel_lock:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(FILE_PATH, index=False)
        logger.info("🧹 Archivo de historial inicializado.")
        print("🧹 Archivo de historial de trades reiniciado correctamente.")
