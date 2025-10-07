"""
Módulo de indicadores técnicos usados por el bot de trading.

Contiene funciones para calcular la media móvil exponencial (EMA)
y el índice de fuerza relativa (RSI), dos de los indicadores más
utilizados en análisis técnico.
"""

import pandas as pd

def calculate_ema(data, period):
    """Calcula la media móvil exponencial (EMA) de una serie de precios.

    La EMA otorga mayor peso a los precios más recientes, lo que permite
    una respuesta más rápida ante cambios en la tendencia.

    Args:
        data (pd.DataFrame): DataFrame que contiene al menos una columna `close`
            con los precios de cierre.
        period (int): Número de periodos a considerar para el cálculo de la EMA.

    Returns:
        pd.Series: Serie de valores EMA correspondiente a la columna `close`.
    """
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calcula el índice de fuerza relativa (RSI) para una serie de precios.

    El RSI mide la velocidad y el cambio de los movimientos de precios,
    indicando condiciones de sobrecompra o sobreventa.

    Args:
        data (pd.DataFrame): DataFrame con una columna `close` que contiene
            los precios de cierre.
        period (int, optional): Número de periodos para el cálculo del RSI.
            Por defecto es 14.

    Returns:
        pd.Series: Serie con los valores RSI en el rango [0, 100].
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
