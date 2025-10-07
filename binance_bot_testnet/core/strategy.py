"""
Módulo de estrategia de trading.

Define la lógica de entrada al mercado basada en indicadores técnicos,
principalmente RSI (Relative Strength Index) y EMA (Exponential Moving Average).
La estrategia se puede extender o modificar fácilmente para adaptarse
a distintos activos o condiciones de mercado.
"""

from core.indicators import calculate_ema, calculate_rsi

def check_entry(rsi, ema_now, ema_prev):
    """Evalúa si se cumplen las condiciones de entrada para una operación.

    En esta estrategia básica:
        - Se busca una señal de cruce al alza de la EMA (actual > previa).
        - El RSI debe estar por encima de un umbral mínimo (por defecto 50).

    Args:
        rsi (float): Valor actual del RSI.
        ema_now (float): Valor actual de la EMA.
        ema_prev (float): Valor anterior de la EMA.

    Returns:
        bool: `True` si se cumplen las condiciones de entrada, `False` en caso contrario.

    Ejemplo:
        >>> check_entry(55, 30000, 29950)
        True
    """
    return rsi < 50 and ema_now > ema_prev

def analyze_market(df, ema_period, rsi_period):
    """
    Analiza el mercado calculando EMA y RSI y devuelve:
    - signal: True si se cumplen las condiciones de entrada
    - rsi: valor RSI actual
    - ema_now: EMA actual
    - ema_prev: EMA anterior
    """
    df["ema"] = calculate_ema(df, ema_period)
    df["rsi"] = calculate_rsi(df, rsi_period)

    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]

    signal = check_entry(rsi, ema_now, ema_prev)
    return signal, rsi, ema_now, ema_prev
