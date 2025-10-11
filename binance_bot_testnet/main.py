# =============================================================================
# MÓDULO: main.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Punto de entrada principal del bot de trading.
#
# Estrategia: TENDENCIA EMA200 + RSI(14)
# -----------------------------------------------------------------------------
# CONDICIONES DE ENTRADA:
#   • Tendencia ALCISTA → Precio > EMA200 y EMA200 actual > EMA200 previa.
#       → Señal LONG si RSI(14) < 50
#
#   • Tendencia BAJISTA → Precio < EMA200 y EMA200 actual < EMA200 previa.
#       → Señal SHORT si RSI(14) > 60
#
# GESTIÓN DE RIESGO:
#   • Ratio riesgo/beneficio 1 : 1.3
#   • Stop Loss (SL) = 1.65 %
#   • Take Profit (TP) = 2.11 %
#   • Capital usado en cada operación = 33.33 % del balance disponible.
#
# El bot analiza continuamente el mercado cada 5 minutos (por defecto) y,
# si se cumplen las condiciones, ejecuta automáticamente la operación
# correspondiente (LONG o SHORT).
#
# Todas las operaciones quedan registradas:
#   ✅ En consola
#   ✅ En logs (logs/execution.log)
#   ✅ En Excel (excel/trades_history.xlsx)
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from services.binance_client import get_client
from data.price_fetcher import get_ohlcv
from core.strategy import analyze_market
from core.order_executor import execute_trade
from core.runner import run_with_retry
from config.settings import (
    SYMBOL, INTERVAL,
    EMA_TREND_PERIOD, RSI_PERIOD,
    TP_PCT_LONG, SL_PCT_LONG,
    TP_PCT_SHORT, SL_PCT_SHORT,
    CAPITAL_ALLOCATION
)
from utils.logger_setup import logger
import time


# =============================================================================
# 🚀 FUNCIÓN PRINCIPAL: Ciclo operativo del bot
# =============================================================================
def main():
    """
    Ciclo principal del bot EMA200 + RSI.

    Pasos:
        1️⃣ Obtener datos OHLCV recientes desde Binance.
        2️⃣ Calcular indicadores EMA200 y RSI(14).
        3️⃣ Analizar la tendencia y condiciones de entrada.
        4️⃣ Ejecutar operación LONG o SHORT si se cumplen criterios.
        5️⃣ Registrar todas las acciones en consola y logs.

    Este ciclo se ejecuta en bucle mediante la función `run_with_retry()`.
    """
    print("\n🚀 Bot EMA200 + RSI iniciado")
    logger.info("🚀 Ciclo de análisis iniciado (EMA200 + RSI).")

    # =========================================================================
    # 📡 Conexión y descarga de datos
    # =========================================================================
    client = get_client()
    df = get_ohlcv(client, SYMBOL, INTERVAL)

    # =========================================================================
    # 🔍 Análisis de mercado
    # =========================================================================
    signal, trade_type, rsi, ema_now, ema_prev, price_now = analyze_market(
        df, EMA_TREND_PERIOD, RSI_PERIOD
    )

    # Mostrar y registrar los datos actuales
    print(f"📈 Precio={price_now:.2f} | EMA200={ema_now:.2f} | RSI={rsi:.2f}")
    logger.info(f"📈 Precio actual={price_now:.2f} | EMA200={ema_now:.2f} | RSI={rsi:.2f}")

    # =========================================================================
    # 🎯 Decisiones de entrada
    # =========================================================================
    if signal and trade_type == "LONG":
        print("🟢 Señal LONG detectada → ejecutando compra...")
        logger.info("🟢 Señal LONG detectada → ejecutando operación de compra (LONG).")

        execute_trade(
            client, df, SYMBOL,
            [TP_PCT_LONG], [SL_PCT_LONG],
            balance_pct=CAPITAL_ALLOCATION,
            trade_type="LONG"
        )

    elif signal and trade_type == "SHORT":
        print("🔴 Señal SHORT detectada → ejecutando venta (simulada)...")
        logger.info("🔴 Señal SHORT detectada → ejecutando operación de venta (SHORT).")

        execute_trade(
            client, df, SYMBOL,
            [TP_PCT_SHORT], [SL_PCT_SHORT],
            balance_pct=CAPITAL_ALLOCATION,
            trade_type="SHORT"
        )

    else:
        print("⏳ No hay señal de entrada válida en este ciclo.")
        logger.info("⏳ No se cumple ninguna condición de entrada (sin operación ejecutada).")

    # Esperar antes del siguiente análisis
    time.sleep(5)


# =============================================================================
# 🧠 BLOQUE DE EJECUCIÓN CONTINUA
# =============================================================================
if __name__ == "__main__":
    """
    Ejecución continua del bot (reanálisis cada 5 minutos).
    Se mantiene activo de forma indefinida, gestionando reintentos automáticos
    ante posibles errores transitorios de red o API de Binance.
    """
    try:
        client = get_client()
        info = client.get_account()

        print("✅ Conectado correctamente a Binance Testnet. Balance disponible:")
        logger.info("✅ Conectado correctamente a Binance Testnet. Mostrando balances disponibles:")

        # Mostrar balances con saldo positivo
        for asset in info['balances']:
            if float(asset['free']) > 0:
                balance_info = f"{asset['asset']}: {float(asset['free']):.6f}"
                print(balance_info)
                logger.info(balance_info)

        # Iniciar ciclo continuo con reintentos automáticos
        run_with_retry(main, interval=300)

    except Exception as e:
        print(f"❌ Error crítico al iniciar el bot: {e}")
        logger.error(f"❌ Error crítico al iniciar el bot: {e}")
