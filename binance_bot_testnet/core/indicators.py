# =============================================================================
# MÓDULO: indicators.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# ----------------------------------------------------------------------------- 
# Contiene los indicadores técnicos usados por el bot: EMA y RSI.
# Esta versión utiliza el RSI de Wilder (idéntico al de TradingView) y la EMA.
# ----------------------------------------------------------------------------- 
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import pandas as pd

def calculate_ema(data, period):
    """
    Calcula la Media Móvil Exponencial (EMA).
    Usa el mismo método que TradingView (ewm con adjust=False).
    """
    return data["close"].ewm(span=period, adjust=False).mean()


def calculate_rsi(data, period=14):
    """
    Calcula el Índice de Fuerza Relativa (RSI) usando el método de Wilder,
    que es el estándar utilizado por TradingView, MetaTrader y la mayoría
    de las plataformas profesionales.

    Args:
        data (pd.DataFrame): DataFrame con columna 'close'.
        period (int): Número de periodos para el RSI (por defecto 14).

    Returns:
        pd.Series: Serie con los valores de RSI.
    """
    delta = data["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # RSI de Wilder → medias exponenciales suavizadas
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
