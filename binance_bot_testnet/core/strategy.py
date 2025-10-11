# =============================================================================
# MÓDULO: strategy.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Define las condiciones de entrada de la estrategia de trading.
# En esta versión, se activa una compra cuando:
#   • RSI < 30 (indica posible sobreventa)
#   • EMA actual > EMA previa (indica cruce alcista)
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from core.indicators import calculate_ema, calculate_rsi

def check_entry(rsi: float, ema_now: float, ema_prev: float) -> bool:
    """Verifica si se cumple la condición de entrada."""
    return rsi < 50 and ema_now > ema_prev

def analyze_market(df, ema_period: int, rsi_period: int):
    """Analiza el mercado con EMA y RSI y retorna si hay señal de entrada."""
    df["ema"] = calculate_ema(df, ema_period)
    df["rsi"] = calculate_rsi(df, rsi_period)
    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]
    signal = check_entry(rsi, ema_now, ema_prev)
    return signal, rsi, ema_now, ema_prev
