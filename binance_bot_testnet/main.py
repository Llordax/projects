# =============================================================================
# MÓDULO: main.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo es el **punto de entrada principal** del bot de trading.
#
# Coordina la ejecución completa del sistema:
#   1️⃣ Inicializa la conexión con Binance.
#   2️⃣ Obtiene los datos de precios (OHLCV) recientes.
#   3️⃣ Calcula los indicadores técnicos (RSI y EMA).
#   4️⃣ Evalúa las condiciones de entrada definidas en la estrategia.
#   5️⃣ Ejecuta operaciones de compra si se cumplen las condiciones.
#   6️⃣ Monitorea y gestiona automáticamente TP/SL y registros de operaciones.
#
# El módulo también implementa un sistema de **reintentos automáticos**
# a través de `core.runner.run_with_retry`, garantizando la continuidad
# del bot ante errores transitorios.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS CLAVE:
#   - Binance API (servicios de conexión y datos)
#   - Indicadores técnicos: EMA y RSI
#   - Estrategia de entrada basada en EMA y RSI
#   - Ejecutor de órdenes y gestor de riesgo
#   - Sistema de logging y reintentos automáticos
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import time
from services.binance_client import get_client
from data.price_fetcher import get_ohlcv
from core.indicators import calculate_rsi, calculate_ema
from core.strategy import check_entry
from core.risk_management import compute_tp_sl
from core.order_executor import execute_trade
from core.runner import run_with_retry

from config.settings import (
    SYMBOL,
    INTERVAL,
    EMA_PERIOD,
    RSI_PERIOD,
    TP_PCTS,
    SL_PCTS,
)

from utils.logger_setup import logger


# =============================================================================
# 🚀 FUNCIÓN PRINCIPAL: Flujo operativo del bot
# =============================================================================
def main():
    """
    Ejecuta el flujo completo del bot de trading en Binance.

    Esta función coordina todas las etapas de la ejecución automatizada:
        1️⃣ Inicializa el cliente Binance.
        2️⃣ Descarga los datos OHLCV del símbolo configurado.
        3️⃣ Calcula los indicadores técnicos (RSI y EMA).
        4️⃣ Evalúa las condiciones de entrada según la estrategia definida.
        5️⃣ Ejecuta una orden de trading si las condiciones se cumplen.

    Cada paso se registra mediante el sistema de logging (`logger`).

    Raises:
        Exception: Si ocurre un error inesperado durante el flujo principal.
    """
    print("\n🚀 Bot iniciado")
    logger.info("Bot iniciado")

    # 1️⃣ Inicializar cliente Binance
    client = get_client()
    print("🔑 Cliente Binance inicializado")
    logger.info("Cliente Binance inicializado")

    # 2️⃣ Obtener precios OHLCV recientes
    df = get_ohlcv(client, SYMBOL, INTERVAL)
    print(f"📊 Últimos precios de {SYMBOL}:")
    print(df.tail(3))
    logger.info("Datos OHLCV obtenidos correctamente")

    # 3️⃣ Calcular indicadores técnicos
    df["ema"] = calculate_ema(df, EMA_PERIOD)
    df["rsi"] = calculate_rsi(df, RSI_PERIOD)

    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]

    print(f"📈 RSI actual: {rsi:.2f}")
    print(f"📈 EMA ahora: {ema_now:.2f}, EMA previa: {ema_prev:.2f}")
    logger.info(f"Indicadores RSI={rsi:.2f}, EMA actual={ema_now:.2f}, EMA previa={ema_prev:.2f}")

    # 4️⃣ Evaluar condiciones de entrada de la estrategia
    if check_entry(rsi, ema_now, ema_prev):
        print("✅ Condición de entrada cumplida")
        logger.info("Condición de entrada cumplida. Ejecutando trade...")

        # 5️⃣ Ejecutar trade completo (compra, TP/SL, registro y monitoreo)
        execute_trade(client, df, SYMBOL, TP_PCTS, SL_PCTS, balance_pct=0.15)
    else:
        print("⛔ No se cumplen condiciones de entrada")
        logger.info("Condición de entrada no cumplida")


# =============================================================================
# 🧭 PUNTO DE ENTRADA PRINCIPAL DEL SCRIPT
# =============================================================================
if __name__ == "__main__":
    """
    Punto de entrada del programa.

    - Verifica la conexión con la cuenta de Binance.
    - Muestra el balance disponible de los activos.
    - Inicia la ejecución continua del bot mediante `run_with_retry()`.
    """
    try:
        # 🔍 Verificar conexión y mostrar balances disponibles
        client = get_client()
        info = client.get_account()

        print("✅ Cuenta conectada. Balance disponible:")
        for asset in info['balances']:
            if float(asset['free']) > 0:
                print(f"{asset['asset']}: {asset['free']}")

        logger.info("Cuenta conectada y balance consultado correctamente")

        # ▶️ Ejecutar el bot con reintentos automáticos
        run_with_retry(main, interval=180)

    except Exception as e:
        # ⚠️ Captura de errores críticos de inicialización
        print(f"❌ Error crítico al iniciar: {e}")
        logger.error(f"Error crítico al iniciar: {e}")
