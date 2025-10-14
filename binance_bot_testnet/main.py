# =============================================================================
# MÓDULO: main.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Punto de entrada principal del bot de trading.
#
# Estrategia técnica:
#   📈 EMA200 + RSI(14)
#   • LONG → Tendencia alcista + RSI < 50
#   • SHORT → Tendencia bajista + RSI > 60
#
# Características clave:
#   ✅ Hasta 2 operaciones simultáneas por símbolo.
#   ✅ Monitoreo TP/SL en hilos paralelos (seguro con ID único por trade).
#   ✅ Registro completo de cada operación (Excel + logs).
#   ✅ Control de riesgo y capital configurable.
#   ✅ Compatibilidad con Binance Testnet.
#
# -----------------------------------------------------------------------------
# ⚙️ Flujo del programa:
#   1️⃣ Conexión con Binance (modo Testnet o real).
#   2️⃣ Muestra balance y activos.
#   3️⃣ Obtiene datos de mercado (OHLCV).
#   4️⃣ Analiza condiciones de entrada (EMA200 + RSI).
#   5️⃣ Si hay señal y el límite no está superado → abre operación.
#   6️⃣ Cada operación lanza un hilo de monitoreo TP/SL independiente.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from services.binance_client import get_client, USE_TESTNET
from data.price_fetcher import get_ohlcv
from core.strategy import analyze_market
from core.order_executor import execute_trade
from core.position_manager import can_open_new_trade, register_new_trade, list_open_trades
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
# 🪙 FUNCIÓN AUXILIAR: Mostrar activos y balance disponible
# =============================================================================
def show_account_assets(client):
    """
    Muestra los activos disponibles en la cuenta de Binance (modo Testnet o Real)
    y el balance actual en EUR.

    Esto permite verificar que el bot dispone de saldo suficiente antes
    de ejecutar nuevas operaciones.
    """
    print("\n💰 --- ACTIVOS DISPONIBLES EN BINANCE ---")
    account = client.get_account()
    total_assets = 0.0

    for asset in account['balances']:
        free = float(asset['free'])
        locked = float(asset['locked'])
        if free > 0 or locked > 0:
            print(f"🔹 {asset['asset']}: libre={free:.6f}, bloqueado={locked:.6f}")
            logger.info(f"Activo {asset['asset']} → libre={free:.6f}, bloqueado={locked:.6f}")
            if asset['asset'] == "EUR":
                total_assets = free

    print(f"💶 Balance disponible en EUR: {total_assets:.2f}\n")
    logger.info(f"Balance actual en EUR: {total_assets:.2f}")


# =============================================================================
# 🚀 FUNCIÓN PRINCIPAL: Ciclo de ejecución del bot
# =============================================================================
def main(show_assets_once=[True]):
    """
    Ejecuta un ciclo completo de análisis y decisión de trading.

    Este ciclo se repite automáticamente cada 10 segundos,
    controlado por el módulo runner (run_with_retry).
    """
    client = get_client()

    # -------------------------------------------------------------------------
    # Mostrar activos solo la primera vez que se ejecuta el bot
    # -------------------------------------------------------------------------
    if show_assets_once[0]:
        show_account_assets(client)
        show_assets_once[0] = False

    # -------------------------------------------------------------------------
    # Mostrar balance actual en EUR antes de cada análisis
    # -------------------------------------------------------------------------
    balances = client.get_account()["balances"]
    eur_balance = next((float(b["free"]) for b in balances if b["asset"] == "EUR"), 0.0)
    print(f"💶 Balance actual en EUR: {eur_balance:.2f}")

    # -------------------------------------------------------------------------
    # Obtener datos de mercado (velas OHLCV)
    # -------------------------------------------------------------------------
    df = get_ohlcv(client, SYMBOL, INTERVAL)

    # Analizar condiciones de entrada según EMA200 + RSI(14)
    signal, trade_type, rsi, ema_now, ema_prev, price_now = analyze_market(df, EMA_TREND_PERIOD, RSI_PERIOD)
    print(f"📈 Precio={price_now:.2f} | EMA200={ema_now:.2f} | RSI={rsi:.2f}")

    # -------------------------------------------------------------------------
    # Control de número máximo de operaciones abiertas
    # -------------------------------------------------------------------------
    if not can_open_new_trade(SYMBOL):
        print("⏸️ Límite de 2 operaciones abiertas alcanzado. Esperando...")
        logger.info(f"⏸️ No se abrirán nuevas operaciones en {SYMBOL} (máximo alcanzado).")
        list_open_trades()  # 🧾 Muestra las operaciones activas
        time.sleep(10)
        return

    # -------------------------------------------------------------------------
    # Decisión de entrada: LONG o SHORT
    # -------------------------------------------------------------------------
    if signal and trade_type in ("LONG", "SHORT"):
        print(f"🎯 Señal {trade_type} detectada → Ejecutando operación...")
        tp = [TP_PCT_LONG] if trade_type == "LONG" else [TP_PCT_SHORT]
        sl = [SL_PCT_LONG] if trade_type == "LONG" else [SL_PCT_SHORT]

        # Ejecutar operación y lanzar hilo de monitoreo
        order = execute_trade(client, df, SYMBOL, tp, sl, CAPITAL_ALLOCATION, trade_type)

        # Registrar la operación si fue creada correctamente
        if order:
            order_id = order.get("orderId", f"SIMULATED_{trade_type}")
            register_new_trade(SYMBOL, order_id)
            print(f"🧾 Operación {trade_type} registrada con ID: {order_id}")
        else:
            print("❌ No se pudo ejecutar la orden de entrada.")
            logger.warning("❌ Falló la ejecución de la orden.")
    else:
        print("⏳ No hay señal de entrada válida.")
        logger.info("⏳ Sin señales válidas para entrar al mercado.")

    # Espera antes del siguiente análisis (frecuencia: 10s)
    time.sleep(10)


# =============================================================================
# 🧠 BLOQUE PRINCIPAL: Ejecución continua con tolerancia a fallos
# =============================================================================
if __name__ == "__main__":
    """
    Ejecuta el bot de forma continua utilizando `run_with_retry()`, que garantiza
    reintentos automáticos en caso de error de conexión o excepción no controlada.
    """
    try:
        # Intervalo de ejecución del runner = 300s (5 minutos)
        run_with_retry(main, interval=300)
    except Exception as e:
        print(f"❌ Error crítico en ejecución: {e}")
        logger.error(f"❌ Error crítico en ejecución: {e}")
