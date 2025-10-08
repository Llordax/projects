# =============================================================================
# MÓDULO: indicators.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo contiene los **indicadores técnicos** utilizados por el bot de trading.
# 
# Actualmente incluye:
#   • EMA (Media Móvil Exponencial)
#   • RSI (Índice de Fuerza Relativa)
#
# Ambos indicadores son herramientas fundamentales en el análisis técnico:
#   - La **EMA** proporciona una media suavizada que da más peso a los precios
#     recientes, lo que permite detectar cambios de tendencia más rápido.
#   - El **RSI** mide la fuerza y velocidad de los movimientos de precio,
#     ayudando a identificar condiciones de sobrecompra o sobreventa.
#
# Estos indicadores son utilizados por el módulo de estrategia para determinar
# señales de entrada o salida en operaciones.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - pandas
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import pandas as pd


# =============================================================================
# 📈 FUNCIÓN: Cálculo de Media Móvil Exponencial (EMA)
# =============================================================================
def calculate_ema(data, period):
    """
    Calcula la **Media Móvil Exponencial (EMA)** de una serie de precios.

    La EMA otorga mayor peso a los precios más recientes, permitiendo una 
    respuesta más rápida ante cambios de tendencia, a diferencia de la media 
    móvil simple (SMA), que pondera todos los precios por igual.

    Args:
        data (pd.DataFrame): DataFrame que contiene al menos una columna `close`
            con los precios de cierre del activo.
        period (int): Número de periodos (ventana temporal) a considerar para 
            el cálculo de la EMA.

    Returns:
        pd.Series: Serie con los valores de la EMA correspondiente a la columna `close`.

    Ejemplo:
        >>> df['EMA_20'] = calculate_ema(df, 20)
    """
    # Se utiliza la función ewm() de pandas para calcular la media móvil exponencial
    return data['close'].ewm(span=period, adjust=False).mean()


# =============================================================================
# 💪 FUNCIÓN: Cálculo del Índice de Fuerza Relativa (RSI)
# =============================================================================
def calculate_rsi(data, period=14):
    """
    Calcula el **Índice de Fuerza Relativa (RSI)** para una serie de precios.

    El RSI es un oscilador que mide la velocidad y el cambio de los movimientos 
    de precios. Devuelve valores entre 0 y 100, donde:
        - RSI > 70 indica posible sobrecompra.
        - RSI < 30 indica posible sobreventa.

    Args:
        data (pd.DataFrame): DataFrame que contiene una columna `close` con los 
            precios de cierre del activo.
        period (int, optional): Número de periodos a utilizar en el cálculo.
            Por defecto, 14 (configuración estándar de Wilder).

    Returns:
        pd.Series: Serie con los valores del RSI en el rango [0, 100].

    Ejemplo:
        >>> df['RSI_14'] = calculate_rsi(df)
    """
    # Diferencia de precios entre periodos consecutivos
    delta = data['close'].diff()

    # Cálculo de ganancias y pérdidas medias durante el periodo
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    # Cálculo de la relación de fuerza (RS)
    rs = gain / loss

    # Cálculo del RSI utilizando la fórmula clásica de Wilder
    return 100 - (100 / (1 + rs))
