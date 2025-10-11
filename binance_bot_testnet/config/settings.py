# =============================================================================
# MÓDULO: settings.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo define la **configuración principal del bot de trading** para Binance Testnet.
#
# En esta versión (modo SCALPER SIMPLE), la estrategia opera con:
#   • Un único Take Profit (TP) al +1.5%
#   • Un único Stop Loss (SL) al -0.5%
#
# Los parámetros definidos aquí controlan los indicadores técnicos, la gestión
# de riesgo y el comportamiento operativo general del bot.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================


# =============================================================================
# 📈 Indicadores técnicos
# =============================================================================
RSI_PERIOD = 14            # Número de periodos usados para calcular el RSI
EMA_PERIOD = 50            # Número de periodos usados para calcular la EMA
RSI_THRESHOLD = 50         # Nivel de referencia RSI para entrada


# =============================================================================
# 🎯 Gestión de riesgos y objetivos
# =============================================================================
TP_PCTS = [0.0125]          # +1.25% de ganancia
SL_PCTS = [0.005]          # -0.5% de pérdida

TP_QTY = [1.0]             # 100% de la posición para el TP
SL_QTY = [1.0]             # 100% de la posición para el SL


# =============================================================================
# 💱 Parámetros de trading generales
# =============================================================================
SYMBOL = "BTCEUR"          # Par de trading usado por defecto
INTERVAL = "15m"            # Intervalo temporal de análisis
TRADE_QUANTITY = 0.001     # Cantidad base o porcentaje del balance
