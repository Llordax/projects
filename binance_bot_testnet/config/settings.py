# =============================================================================
# MÓDULO: settings.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo define la **configuración principal del bot de trading** para 
# Binance Testnet. 
#
# Contiene los parámetros y constantes base que controlan el comportamiento
# del sistema, como los periodos de indicadores técnicos, los niveles de
# Take Profit y Stop Loss, así como los símbolos y marcos temporales usados.
#
# Estas variables actúan como **punto central de configuración**, facilitando
# los ajustes de la estrategia sin modificar la lógica principal del código.
#
# -----------------------------------------------------------------------------
# ⚙️ PARÁMETROS DEFINIDOS:
#
# Indicadores técnicos:
#   - RSI_PERIOD: Ventana temporal usada para el RSI.
#   - EMA_PERIOD: Ventana temporal usada para la EMA.
#   - RSI_THRESHOLD: Nivel de referencia para la toma de decisiones RSI.
#
# Gestión de riesgo:
#   - TP_PCTS: Porcentajes de ganancia para cada Take Profit.
#   - SL_PCTS: Porcentajes de pérdida para cada Stop Loss.
#   - TP_QTY: Porción del volumen total asignado a cada nivel TP.
#   - SL_QTY: Porción del volumen total asignado a cada nivel SL.
#
# Parámetros de trading:
#   - SYMBOL: Par de trading principal.
#   - INTERVAL: Intervalo temporal de análisis.
#   - TRADE_QUANTITY: Cantidad base a operar o porcentaje del balance.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================


# =============================================================================
# 📈 Indicadores técnicos
# =============================================================================
RSI_PERIOD = 14            # Número de periodos usados para calcular el RSI
EMA_PERIOD = 50            # Número de periodos usados para calcular la EMA
RSI_THRESHOLD = 50         # Nivel de referencia RSI para entrada (neutralidad)


# =============================================================================
# 🎯 Gestión de riesgos y objetivos
# =============================================================================
TP_PCTS = [0.015, 0.03, 0.045]   # Porcentajes de ganancia (1.5%, 3%, 4.5%)
SL_PCTS = [0.005, 0.01, 0.015]   # Porcentajes de pérdida (0.5%, 1%, 1.5%)

TP_QTY = [0.33, 0.33, 0.34]      # Distribución de cantidad por nivel TP
SL_QTY = [0.33, 0.33, 0.34]      # Distribución de cantidad por nivel SL


# =============================================================================
# 💱 Parámetros de trading generales
# =============================================================================
SYMBOL = "BTCEUR"                # Par de trading usado por defecto
INTERVAL = "1h"                  # Intervalo temporal de las velas
TRADE_QUANTITY = 0.001           # Cantidad base o porcentaje del balance
