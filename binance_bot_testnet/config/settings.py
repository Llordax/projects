# =============================================================================
# MÓDULO: settings.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo define la **configuración principal del bot de trading** para Binance Testnet.
#
# En esta nueva versión (modo TENDENCIA EMA200 + RSI), la estrategia opera con:
#   • Entradas en largo (LONG) cuando RSI < 50 y tendencia alcista.
#   • Entradas en corto (SHORT) cuando RSI > 60 y tendencia bajista.
#
# La tendencia se define según:
#   • Alcista: precio > EMA200 y EMA200 actual > EMA200 previa
#   • Bajista: precio < EMA200 y EMA200 actual < EMA200 previa
#
# Gestión de riesgo:
#   • Stop Loss (SL): ±1.65%
#   • Take Profit (TP): ±2.11%
#   • Ratio Riesgo/Beneficio = 1 : 1.3
#   • Uso del capital: 33.33% del balance disponible
#
# Permite operar con velas de 1m, 5m, 15m o 1h.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================


# =============================================================================
# 📈 Indicadores técnicos
# =============================================================================
RSI_PERIOD = 14             # Número de periodos usados para calcular el RSI
EMA_TREND_PERIOD = 200      # EMA utilizada para detectar la tendencia principal


# =============================================================================
# 🎯 Gestión de riesgos y objetivos
# =============================================================================
# Stop Loss (riesgo) y Take Profit (beneficio) expresados en porcentajes decimales
SL_PCT_LONG = 0.0165        # -1.65% para operaciones en largo
TP_PCT_LONG = 0.0211        # +2.11% para operaciones en largo

SL_PCT_SHORT = 0.0165       # +1.65% para operaciones en corto (inverso)
TP_PCT_SHORT = 0.0211       # -2.11% para operaciones en corto (inverso)

CAPITAL_ALLOCATION = 0.3333  # 33.33% del balance disponible en cada operación


# =============================================================================
# 💱 Parámetros de trading generales
# =============================================================================
SYMBOL = "BTCEUR"           # Par de trading usado por defecto
INTERVAL = "15m"            # Intervalo temporal (puede cambiarse a "1m", "5m" o "1h")
