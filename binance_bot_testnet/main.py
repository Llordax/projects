# =============================================================================
# MÓDULO: main.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Punto de entrada principal del bot scalper.
# Revisa RSI y EMA cada minuto y ejecuta compra con 1 TP (+1.5%) y 1 SL (-0.5%).
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from services.binance_client import get_client
from data.price_fetcher import get_ohlcv
from core.indicators import calculate_rsi, calculate_ema
from core.strategy import check_entry
from core.order_executor import execute_trade
from core.runner import run_with_retry
from config.settings import SYMBOL, INTERVAL, EMA_PERIOD, RSI_PERIOD, TP_PCTS, SL_PCTS
from utils.logger_setup import logger
import time

def main():
    """Ciclo principal del bot scalper."""
    print("\n🚀 Bot Scalper iniciado")
    client = get_client()
    df = get_ohlcv(client, SYMBOL, INTERVAL)
    df["ema"] = calculate_ema(df, EMA_PERIOD)
    df["rsi"] = calculate_rsi(df, RSI_PERIOD)
    # Usamos solo velas cerradas para evitar discrepancias
    rsi = df["rsi"].iloc[-2]
    ema_now = df["ema"].iloc[-2]
    ema_prev = df["ema"].iloc[-3]
    print(f"📈 RSI={rsi:.2f} | EMA actual={ema_now:.2f} | EMA previa={ema_prev:.2f}")
    if check_entry(rsi, ema_now, ema_prev):
        print("✅ Señal detectada → ejecutando trade")
        execute_trade(client, df, SYMBOL, TP_PCTS, SL_PCTS, balance_pct=0.15)
    else:
        print("⏳ No hay señal de entrada por ahora.")
    time.sleep(5)

if __name__ == "__main__":
    """Ejecución continua del bot scalper (reanálisis cada 60 s)."""
    try:
        client = get_client()
        info = client.get_account()
        print("✅ Conectado a Binance Testnet. Balance:")
        for asset in info['balances']:
            if float(asset['free']) > 0:
                print(f"{asset['asset']}: {asset['free']}")
        run_with_retry(main, interval=300)
    except Exception as e:
        print(f"❌ Error crítico al iniciar: {e}")
        logger.error(f"Error crítico al iniciar: {e}")
