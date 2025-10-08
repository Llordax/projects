"""
Módulo de adquisición de datos de precios desde Binance.

Proporciona funciones para obtener datos OHLCV (Open, High, Low, Close, Volume)
directamente desde la API de Binance, que luego se utilizan en los cálculos
de indicadores técnicos y estrategias de trading.
"""

from binance.client import Client
import pandas as pd
from utils.logger_setup import logger

def get_ohlcv(client, symbol, interval, limit=100):
    """Obtiene los datos OHLCV recientes de un símbolo en Binance.

    Args:
        client (Client): Instancia autenticada del cliente de Binance.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        interval (str): Intervalo temporal de las velas (por ejemplo, "1h", "15m").
        limit (int, optional): Número máximo de velas a recuperar. Por defecto es 100.

    Returns:
        pd.DataFrame: DataFrame con columnas:
            ['timestamp', 'open', 'high', 'low', 'close', 'volume']

    Raises:
        Exception: Si la API de Binance no devuelve datos válidos.

    Ejemplo:
        >>> df = get_ohlcv(client, "BTCEUR", "1h")
        >>> df.head()
             timestamp     open     high      low    close   volume
        0  1691235600000  29500.0  29600.0  29450.0  29580.0  152.43
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(
            klines,
            columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "trades",
                "taker_buy_base", "taker_buy_quote", "ignore"
            ]
        )

        df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
        logger.info(f"Datos OHLCV obtenidos correctamente para {symbol} ({interval})")
        return df

    except Exception as e:
        logger.error(f"Error al obtener datos OHLCV: {e}")
        raise
