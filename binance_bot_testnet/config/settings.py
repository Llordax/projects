"""
Configuración principal del bot de trading para Binance Testnet.

Este módulo define los parámetros base utilizados por el bot, incluyendo
indicadores técnicos, porcentajes de take-profit (TP) y stop-loss (SL),
símbolo de trading y configuración del timeframe.

Constantes:
    RSI_PERIOD (int): Número de periodos usados para calcular el RSI.
    EMA_PERIOD (int): Número de periodos usados para calcular la EMA.
    RSI_THRESHOLD (int): Nivel de referencia para evaluar señales RSI.

    TP_PCTS (list[float]): Porcentajes de ganancia para cada nivel de take-profit.
    SL_PCTS (list[float]): Porcentajes de pérdida permitidos para cada stop-loss.
    TP_QTY (list[float]): Proporción del total de la posición asignada a cada nivel TP.
    SL_QTY (list[float]): Proporción del total de la posición asignada a cada nivel SL.

    SYMBOL (str): Par de trading usado por el bot (por defecto: "BTCEUR").
    INTERVAL (str): Intervalo temporal de las velas (por ejemplo, "1h", "15m", etc.).
    TRADE_QUANTITY (float): Cantidad base por operación o porcentaje de balance.
"""

# --- Indicadores técnicos ---
RSI_PERIOD = 14
EMA_PERIOD = 50
RSI_THRESHOLD = 50

# --- Gestión de riesgos y objetivos ---
TP_PCTS = [0.015, 0.03, 0.045]
SL_PCTS = [0.005, 0.01, 0.015]
TP_QTY = [0.33, 0.33, 0.34]
SL_QTY = [0.33, 0.33, 0.34]

# --- Parámetros de trading ---
SYMBOL = "BTCEUR"
INTERVAL = "1h"
TRADE_QUANTITY = 0.001  # o porcentaje de balance