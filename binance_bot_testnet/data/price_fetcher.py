# =============================================================================
# MÓDULO: price_fetcher.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo gestiona la **adquisición de datos de precios (OHLCV)** desde la
# API de Binance.
#
# Los datos obtenidos son fundamentales para el análisis técnico del bot, ya que
# se utilizan en los cálculos de indicadores (EMA, RSI, etc.) y en la toma de 
# decisiones de la estrategia.
#
# El formato de datos recuperado corresponde a velas o "klines" que incluyen:
#   - O: Precio de apertura (Open)
#   - H: Precio máximo (High)
#   - L: Precio mínimo (Low)
#   - C: Precio de cierre (Close)
#   - V: Volumen (Volume)
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES:
#   ✅ Conectar con la API de Binance y solicitar datos OHLCV.
#   ✅ Convertir la respuesta cruda de la API en un DataFrame de pandas.
#   ✅ Registrar correctamente la obtención o errores en los logs.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - binance.client.Client → para acceder a la API de Binance.
#   - pandas → para estructurar los datos en DataFrame.
#   - utils.logger_setup.logger → para registrar la actividad.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from binance.client import Client
import pandas as pd
from utils.logger_setup import logger


# =============================================================================
# 📊 FUNCIÓN: Obtener datos OHLCV desde Binance
# =============================================================================
def get_ohlcv(client: Client, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
    """
    Obtiene los datos más recientes de velas OHLCV (Open, High, Low, Close, Volume)
    de un símbolo determinado en Binance.

    Los datos se devuelven en un `DataFrame` de pandas, ideal para análisis técnico
    y cálculos de indicadores como EMA, RSI, MACD, etc.

    Args:
        client (Client): Instancia autenticada del cliente de Binance.
        symbol (str): Par de trading (por ejemplo, "BTCEUR", "BTCUSDT").
        interval (str): Intervalo temporal de las velas (por ejemplo, "1h", "15m", "1d").
        limit (int, optional): Número máximo de velas a recuperar. Por defecto es 100.

    Returns:
        pd.DataFrame: DataFrame con las columnas:
            ['timestamp', 'open', 'high', 'low', 'close', 'volume'].
        Los valores están convertidos a tipo `float`.

    Raises:
        Exception: Si ocurre un error durante la conexión o los datos devueltos
        no son válidos.

    Ejemplo:
        >>> df = get_ohlcv(client, "BTCEUR", "1h")
        >>> df.head()
             timestamp     open     high      low    close   volume
        0  1691235600000  29500.0  29600.0  29450.0  29580.0  152.43

    Notas:
        - La función utiliza el endpoint `get_klines` de la API de Binance.
        - Los datos están en milisegundos en la columna `timestamp`.
        - Se recomienda convertir el timestamp a datetime para análisis visual.
    """
    try:
        # Solicitar datos OHLCV (velas) a la API de Binance
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

        # Crear DataFrame con las columnas principales devueltas por Binance
        df = pd.DataFrame(
            klines,
            columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "trades",
                "taker_buy_base", "taker_buy_quote", "ignore"
            ]
        )

        # Filtrar solo las columnas relevantes y convertir a tipo float
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)

        df = df[:-1]  # 🔒 Elimina la última vela (aún en formación)


        # Registrar éxito de obtención de datos
        logger.info(f"Datos OHLCV obtenidos correctamente para {symbol} ({interval})")

        return df

    except Exception as e:
        # Registrar error y propagar la excepción
        logger.error(f"Error al obtener datos OHLCV: {e}")
        raise
