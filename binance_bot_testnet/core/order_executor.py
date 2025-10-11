# =============================================================================
# MÓDULO: order_executor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo controla todo el flujo operativo de ejecución del bot:
#   1. Cálculo de cantidad según balance y porcentaje configurado.
#   2. Ejecución de la orden (compra o simulación de venta).
#   3. Colocación de órdenes de Take Profit (TP) y Stop Loss (SL).
#   4. Registro del trade y monitoreo posterior.
#
# 🚀 Versión TENDENCIA EMA200 + RSI:
#   - Admite operaciones LONG y SHORT.
#   - Ratio riesgo/beneficio 1:1.3.
#   - Uso del 33.33% del balance por operación.
#
# ⚙️ NOTA IMPORTANTE:
#   - En Binance Spot Testnet no se pueden abrir posiciones cortas reales.
#     Por lo tanto, las operaciones SHORT se simulan para backtesting.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from binance.client import Client
from core.risk_management import compute_tp_sl
from core.order_monitor import monitor_orders
from utils.logger import log_trade
from utils.logger_setup import logger
import math
import time


# =============================================================================
# 🔢 FUNCIÓN: Ajustar cantidad según filtros de Binance
# =============================================================================
def adjust_quantity_to_filters(client: Client, symbol: str, quantity: float, price: float) -> float:
    """Ajusta la cantidad de compra o venta según los filtros de Binance."""
    try:
        info = client.get_symbol_info(symbol)
        lot, min_qty, min_notional = None, None, None

        for f in info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                lot = float(f["stepSize"])
                min_qty = float(f["minQty"])
            elif f["filterType"] == "MIN_NOTIONAL":
                min_notional = float(f["minNotional"])

        if lot:
            quantity = math.floor(quantity / lot) * lot
        if min_qty and quantity < min_qty:
            quantity = min_qty
        if min_notional and (quantity * price) < min_notional:
            quantity = min_notional / price

        return round(quantity, 6)
    except Exception as e:
        logger.error(f"Error al ajustar cantidad: {e}")
        return quantity


# =============================================================================
# 🟢 FUNCIÓN: Ejecutar orden de compra al mercado
# =============================================================================
def place_market_buy(client: Client, symbol: str, quantity: float):
    """Ejecuta una orden de compra al mercado."""
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = adjust_quantity_to_filters(client, symbol, quantity, price)
        safe_qty = format(quantity, '.6f').rstrip('0').rstrip('.')
        print(f"🟢 Comprando {safe_qty} {symbol}...")
        order = client.order_market_buy(symbol=symbol, quantity=safe_qty)
        print("✅ Compra ejecutada correctamente.")
        return order
    except Exception as e:
        print(f"❌ Error al comprar: {e}")
        logger.error(f"Error al comprar: {e}")
        return None


# =============================================================================
# 💰 FUNCIÓN PRINCIPAL: Ejecutar operación LONG o SHORT
# =============================================================================
def execute_trade(client: Client, df, symbol: str, tp_pcts: list, sl_pcts: list,
                  balance_pct: float, trade_type: str):
    """
    Flujo completo de ejecución de una operación (LONG o SHORT).

    Args:
        client (Client): Cliente de Binance autenticado.
        df (pd.DataFrame): DataFrame de precios.
        symbol (str): Par de trading.
        tp_pcts (list): Porcentaje(s) de Take Profit.
        sl_pcts (list): Porcentaje(s) de Stop Loss.
        balance_pct (float): Porcentaje de capital a invertir.
        trade_type (str): "LONG" o "SHORT".
    """
    # 1️⃣ Calcular cantidad a comprar/vender
    from core.order_executor import calculate_trade_quantity
    qty = calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=balance_pct)
    if qty <= 0:
        logger.warning("Cantidad calculada <= 0. Operación cancelada.")
        return

    # 2️⃣ Obtener precio actual
    entry_price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    # 3️⃣ Ejecución según tipo de trade
    if trade_type == "LONG":
        print(f"🟢 Ejecutando LONG en {symbol} @ {entry_price:.2f}")
        order = place_market_buy(client, symbol, qty)
        tps = [entry_price * (1 + tp_pcts[0])]
        sls = [entry_price * (1 - sl_pcts[0])]
    else:
        print(f"🔴 Ejecutando SHORT (simulado) en {symbol} @ {entry_price:.2f}")
        order = {"orderId": "SIMULATED_SHORT", "fills": [{"price": str(entry_price)}]}
        tps = [entry_price * (1 - tp_pcts[0])]
        sls = [entry_price * (1 + sl_pcts[0])]

    if not order:
        logger.error("❌ No se pudo ejecutar la orden. Abortando ciclo.")
        return

    # 4️⃣ Colocar TP/SL (o simularlos en SHORT)
    place_tp_sl_orders(client, symbol, qty, entry_price, tps, sls, [1.0])

    # 5️⃣ Registrar operación
    log_trade(order["orderId"], symbol, trade_type.lower(), qty, entry_price, sls[0], tps[0], None, 0.0)

    # 6️⃣ Monitorear ejecución (simulada o real)
    monitor_orders(client, symbol, entry_price, qty)
