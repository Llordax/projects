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


def main():
    print("\n🚀 Bot iniciado")
    logger.info("Bot iniciado")

    client = get_client()
    print("🔑 Cliente Binance inicializado")
    logger.info("Cliente Binance inicializado")

    df = get_ohlcv(client, SYMBOL, INTERVAL)
    print(f"📊 Últimos precios de {SYMBOL}:")
    print(df.tail(3))
    logger.info("Datos OHLCV obtenidos correctamente")

    df["ema"] = calculate_ema(df, EMA_PERIOD)
    df["rsi"] = calculate_rsi(df, RSI_PERIOD)

    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]

    print(f"📈 RSI actual: {rsi:.2f}")
    print(f"📈 EMA ahora: {ema_now:.2f}, EMA previa: {ema_prev:.2f}")
    logger.info(f"Indicadores RSI={rsi:.2f}, EMA actual={ema_now:.2f}, EMA previa={ema_prev:.2f}")

    if check_entry(rsi, ema_now, ema_prev):
        print("✅ Condición de entrada cumplida")
        logger.info("Condición de entrada cumplida. Ejecutando trade...")
        execute_trade(client, df, SYMBOL, TP_PCTS, SL_PCTS, usdt_percentage=0.15)
    else:
        print("⛔ No se cumplen condiciones de entrada")
        logger.info("Condición de entrada no cumplida")


if __name__ == "__main__":
    try:
        client = get_client()
        info = client.get_account()
        print("✅ Cuenta conectada. Balance disponible:")
        for asset in info['balances']:
            if float(asset['free']) > 0:
                print(f"{asset['asset']}: {asset['free']}")
        logger.info("Cuenta conectada y balance consultado correctamente")

        run_with_retry(main, interval=10)
    except Exception as e:
        print(f"❌ Error crítico al iniciar: {e}")
        logger.error(f"Error crítico al iniciar: {e}")
