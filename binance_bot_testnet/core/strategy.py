# =============================================================================
# MÓDULO: strategy.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo define la **estrategia de trading** utilizada por el bot.
#
# La lógica actual se basa en dos indicadores técnicos clave:
#   - **RSI (Relative Strength Index)**: mide la fuerza y velocidad del movimiento de precios.
#   - **EMA (Exponential Moving Average)**: media móvil ponderada que reacciona más
#     rápidamente a los cambios recientes del mercado.
#
# La estrategia busca señales de entrada al detectar:
#   ✅ Un cruce al alza de la EMA (EMA actual > EMA previa).
#   ✅ Un RSI superior a un umbral (indicando momentum alcista).
#
# Este módulo es modular y fácilmente extensible, permitiendo incorporar
# nuevos indicadores, condiciones de confirmación o estrategias combinadas.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - core.indicators.calculate_ema
#   - core.indicators.calculate_rsi
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from core.indicators import calculate_ema, calculate_rsi


# =============================================================================
# ⚙️ FUNCIÓN: Verificación de condiciones de entrada
# =============================================================================
def check_entry(rsi: float, ema_now: float, ema_prev: float) -> bool:
    """
    Evalúa si se cumplen las condiciones de entrada para una operación de compra.

    En esta estrategia básica, la señal se activa cuando:
        - El RSI está por debajo de 50 (indica posible recuperación desde zona de sobreventa).
        - La EMA actual supera a la EMA previa, indicando cruce al alza (tendencia alcista).

    Args:
        rsi (float): Valor actual del RSI.
        ema_now (float): Valor actual de la EMA.
        ema_prev (float): Valor anterior de la EMA.

    Returns:
        bool: `True` si se cumplen las condiciones de entrada, `False` en caso contrario.

    Ejemplo:
        >>> check_entry(45, 30200, 30000)
        True

    Notas:
        - Esta estrategia está pensada para detectar cambios de tendencia a corto plazo.
        - Puede modificarse fácilmente para estrategias inversas (venta) o neutras.
    """
    # Condición de entrada: RSI bajo + EMA cruza al alza
    return rsi < 50 and ema_now > ema_prev


# =============================================================================
# 📊 FUNCIÓN: Análisis de mercado
# =============================================================================
def analyze_market(df, ema_period: int, rsi_period: int):
    """
    Analiza el mercado aplicando los indicadores técnicos definidos (EMA y RSI)
    y evalúa si se cumplen las condiciones de entrada según la estrategia.

    Args:
        df (pd.DataFrame): DataFrame que contiene los precios (debe incluir columna 'close').
        ema_period (int): Número de periodos para calcular la EMA.
        rsi_period (int): Número de periodos para calcular el RSI.

    Returns:
        tuple:
            - signal (bool): `True` si hay señal de entrada según la estrategia.
            - rsi (float): Valor actual del RSI.
            - ema_now (float): EMA actual.
            - ema_prev (float): EMA del periodo anterior.

    Ejemplo:
        >>> signal, rsi, ema_now, ema_prev = analyze_market(df, 20, 14)
        >>> if signal:
        ...     print("📈 Señal de compra detectada")
    """
    # Calcular los indicadores técnicos principales
    df["ema"] = calculate_ema(df, ema_period)
    df["rsi"] = calculate_rsi(df, rsi_period)

    # Extraer los valores más recientes de RSI y EMA
    rsi = df["rsi"].iloc[-1]
    ema_now = df["ema"].iloc[-1]
    ema_prev = df["ema"].iloc[-2]

    # Evaluar si existe una señal de entrada según la estrategia definida
    signal = check_entry(rsi, ema_now, ema_prev)

    # Retornar resultados de análisis para decisión de trading
    return signal, rsi, ema_now, ema_prev
