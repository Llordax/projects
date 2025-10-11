# =============================================================================
# MÓDULO: strategy.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Define las condiciones de entrada de la estrategia de trading.
#
# Estrategia avanzada: TENDENCIA EMA200 + RSI(14)
# -----------------------------------------------------------------------------
# ANÁLISIS DE TENDENCIA:
#   • Tendencia ALCISTA:
#       - El precio actual está por encima de la EMA200.
#       - La EMA200 actual es mayor que la EMA200 del periodo anterior.
#
#   • Tendencia BAJISTA:
#       - El precio actual está por debajo de la EMA200.
#       - La EMA200 actual es menor que la EMA200 del periodo anterior.
#
#   • Si no se cumple ninguna de las dos condiciones, se considera LATERAL.
#
# CONDICIONES DE ENTRADA:
#   • LONG → Tendencia alcista + RSI(14) < 50
#   • SHORT → Tendencia bajista + RSI(14) > 60
#
# Todas las evaluaciones se registran en consola y en logs para trazabilidad.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import pandas as pd
from core.indicators import calculate_ema, calculate_rsi
from utils.logger_setup import logger


# =============================================================================
# 🧠 FUNCIÓN PRINCIPAL: Análisis del mercado
# =============================================================================
def analyze_market(df: pd.DataFrame, ema_period: int, rsi_period: int):
    """
    Analiza la tendencia (EMA200) y las condiciones de entrada (RSI).

    Args:
        df (pd.DataFrame): DataFrame con datos OHLCV.
        ema_period (int): Periodo para la EMA (normalmente 200).
        rsi_period (int): Periodo para el RSI (por defecto 14).

    Returns:
        tuple:
            signal (bool): True si hay señal de entrada.
            trade_type (str | None): "LONG", "SHORT" o None.
            rsi (float): Valor del RSI actual.
            ema_now (float): EMA200 actual.
            ema_prev (float): EMA200 del periodo anterior.
            price_now (float): Precio de cierre más reciente.
    """

    # =========================================================================
    # 📈 Cálculo de indicadores técnicos
    # =========================================================================
    df["ema"] = calculate_ema(df, ema_period)
    df["rsi"] = calculate_rsi(df, rsi_period)

    price_now = df["close"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]
    rsi = df["rsi"].iloc[-1]

    # =========================================================================
    # 📊 Determinación de la tendencia
    # =========================================================================
    if price_now > ema_now and ema_now > ema_prev:
        trend = "ALCISTA"
        reason = (
            f"El precio actual ({price_now:.2f}) está por encima de la EMA200 ({ema_now:.2f}), "
            f"y la EMA200 actual ({ema_now:.2f}) es mayor que la EMA200 previa ({ema_prev:.2f})."
        )
    elif price_now < ema_now and ema_now < ema_prev:
        trend = "BAJISTA"
        reason = (
            f"El precio actual ({price_now:.2f}) está por debajo de la EMA200 ({ema_now:.2f}), "
            f"y la EMA200 actual ({ema_now:.2f}) es menor que la EMA200 previa ({ema_prev:.2f})."
        )
    else:
        trend = "LATERAL"
        reason = (
            f"No hay confirmación de tendencia: el precio ({price_now:.2f}) y la EMA200 ({ema_now:.2f}) "
            f"no muestran una dirección clara respecto al periodo anterior ({ema_prev:.2f})."
        )

    # Registrar tendencia y explicación
    msg_trend = f"📊 Tendencia detectada: {trend}. {reason}"
    print(msg_trend)
    logger.info(msg_trend)

    # =========================================================================
    # ⚙️ Evaluación de condiciones de entrada (RSI)
    # =========================================================================
    signal = False
    trade_type = None

    if trend == "ALCISTA" and rsi < 50:
        signal = True
        trade_type = "LONG"
        msg_entry = (
            f"✅ Condiciones de entrada LONG detectadas: tendencia ALCISTA y RSI={rsi:.2f} < 50."
        )
        print(msg_entry)
        logger.info(msg_entry)

    elif trend == "BAJISTA" and rsi > 60:
        signal = True
        trade_type = "SHORT"
        msg_entry = (
            f"✅ Condiciones de entrada SHORT detectadas: tendencia BAJISTA y RSI={rsi:.2f} > 60."
        )
        print(msg_entry)
        logger.info(msg_entry)

    else:
        msg_no_entry = (
            f"⏳ No se cumplen condiciones de entrada: tendencia={trend}, RSI={rsi:.2f}."
        )
        print(msg_no_entry)
        logger.info(msg_no_entry)

    # =========================================================================
    # 📤 Devolver resultados
    # =========================================================================
    return signal, trade_type, rsi, ema_now, ema_prev, price_now
