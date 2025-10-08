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
    """Función principal que ejecuta el flujo del bot de trading.

    Esta función inicializa el cliente de Binance, obtiene los datos OHLCV
    recientes, calcula los indicadores técnicos (RSI y EMA), evalúa las condiciones
    de entrada mediante la estrategia definida y ejecuta la orden si se cumplen
    los criterios.

    Flujo general:
        1. Inicializa cliente de Binance.
        2. Descarga precios históricos del símbolo configurado.
        3. Calcula indicadores RSI y EMA.
        4. Verifica condiciones de entrada.
        5. Ejecuta trade si se cumplen condiciones.

    Logs:
        - Registra cada paso en `utils.logger_setup.logger`.

    Raises:
        Exception: Si ocurre un error inesperado durante la ejecución principal.
    """
    print("\n🚀 Bot iniciado")
    logger.info("Bot iniciado")

    client = get_client()
    print("🔑 Cliente Binance inicializado")
    logger.info("Cliente Binance inicializado")

    df = get_ohlcv(client, SYMBOL, INTERVAL)
    print(f"📊 Últimos precios de {SYMBOL}:")
    print(df.tail(3))
    logger.info("Datos OHLCV obtenidos correctamente")

    # Cálculo de indicadores técnicos
    df["ema"] = calculate_ema(df, EMA_PERIOD)
    df["rsi"] = calculate_rsi(df, RSI_PERIOD)

    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]

    print(f"📈 RSI actual: {rsi:.2f}")
    print(f"📈 EMA ahora: {ema_now:.2f}, EMA previa: {ema_prev:.2f}")
    logger.info(f"Indicadores RSI={rsi:.2f}, EMA actual={ema_now:.2f}, EMA previa={ema_prev:.2f}")

    # Evaluación de condiciones de entrada
    if check_entry(rsi, ema_now, ema_prev):
        print("✅ Condición de entrada cumplida")
        logger.info("Condición de entrada cumplida. Ejecutando trade...")
        execute_trade(client, df, SYMBOL, TP_PCTS, SL_PCTS, usdt_percentage=0.15)
    else:
        print("⛔ No se cumplen condiciones de entrada")
        logger.info("Condición de entrada no cumplida")


if __name__ == "__main__":
    """Punto de entrada del script.

    Verifica la conexión con la cuenta de Binance antes de iniciar el bot.
    En caso de éxito, muestra el balance disponible en la consola y
    posteriormente ejecuta la función principal con un mecanismo de reintento.
    """
    try:
        client = get_client()
        info = client.get_account()
        print("✅ Cuenta conectada. Balance disponible:")
        for asset in info['balances']:
            if float(asset['free']) > 0:
                print(f"{asset['asset']}: {asset['free']}")
        logger.info("Cuenta conectada y balance consultado correctamente")

        # Ejecutar el bot con manejo de errores y reintentos
        run_with_retry(main, interval=180)
    except Exception as e:
        print(f"❌ Error crítico al iniciar: {e}")
        logger.error(f"Error crítico al iniciar: {e}")
