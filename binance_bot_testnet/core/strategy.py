# core/strategy.py
from core.indicators import calculate_ema, calculate_rsi

def check_entry(rsi, ema_now, ema_prev):
    """Condición de entrada: RSI < 50 y EMA actual > EMA previa."""
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
