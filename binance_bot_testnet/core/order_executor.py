# =============================================================================
# MÓDULO: order_executor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Controla el flujo completo de ejecución de una operación:
#   1. Cálculo del tamaño de posición (según balance y % configurado).
#   2. Ejecución de la orden (LONG real o SHORT simulado).
#   3. Colocación de Take Profit (TP) y Stop Loss (SL).
#   4. Registro del trade en Excel y logs.
#   5. Lanzamiento del monitoreo TP/SL en un hilo paralelo (thread-safe).
#
# 🚀 Versión paralelizada (EMA200 + RSI)
#   - Cada operación se ejecuta con un ID único (UUID8).
#   - Monitoreo concurrente mediante threading.Thread (modo daemon).
#   - Ratio riesgo/beneficio = 1:1.3.
#   - Capital usado por operación = 33.33%.
#
# ⚙️ NOTA IMPORTANTE:
#   - En Binance Spot Testnet no hay operaciones SHORT reales, se simulan.
#   - Cada hilo supervisa una operación concreta, evitando cierres duplicados.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import math
import threading
import uuid  # 🆕 Para generar IDs únicos por operación
from binance.client import Client
from core.order_monitor import monitor_orders
from utils.logger import log_trade
from utils.logger_setup import logger


# =============================================================================
# 🔢 FUNCIÓN: Ajustar cantidad según filtros de Binance
# =============================================================================
def adjust_quantity_to_filters(client: Client, symbol: str, quantity: float, price: float) -> float:
    """Ajusta la cantidad según los filtros de Binance (LOT_SIZE, MIN_NOTIONAL)."""
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
# 💰 FUNCIÓN: Calcular cantidad según balance
# =============================================================================
def calculate_trade_quantity(client: Client, symbol: str, balance_asset: str = 'EUR', balance_pct: float = 0.3333) -> float:
    """Calcula la cantidad a tradear según el balance disponible y el % asignado."""
    try:
        balances = client.get_account()['balances']
        asset_balance = next(
            (float(b['free']) for b in balances if b['asset'] == balance_asset), 0.0
        )

        if asset_balance <= 0:
            print(f"⚠️ No hay saldo disponible en {balance_asset}.")
            logger.warning(f"No hay saldo disponible en {balance_asset}.")
            return 0.0

        invest_amount = asset_balance * balance_pct
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        qty = invest_amount / price
        qty = adjust_quantity_to_filters(client, symbol, qty, price)
        return qty

    except Exception as e:
        logger.error(f"Error al calcular cantidad: {e}")
        print(f"❌ Error al calcular cantidad: {e}")
        return 0.0


# =============================================================================
# 🟢 FUNCIÓN: Ejecutar compra al mercado
# =============================================================================
def place_market_buy(client: Client, symbol: str, quantity: float):
    """Ejecuta una orden de compra al mercado (LONG real)."""
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
# 🎯 FUNCIÓN: Colocar órdenes TP/SL
# =============================================================================
def place_tp_sl_orders(client: Client, symbol: str, quantity: float, entry_price: float,
                       tp_prices: list, sl_prices: list, portions: list, trade_type: str):
    """Crea las órdenes de Take Profit y Stop Loss para la operación."""
    try:
        for tp, sl, portion in zip(tp_prices, sl_prices, portions):
            qty = quantity * portion
            qty = adjust_quantity_to_filters(client, symbol, qty, entry_price)

            print(f"📈 Configurando {trade_type} → TP: {tp:.2f} | SL: {sl:.2f}")
            logger.info(f"Configurando {trade_type} → TP: {tp:.2f} | SL: {sl:.2f}")

            side = "SELL" if trade_type == "LONG" else "BUY"

            client.create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=qty,
                price=f"{tp:.2f}",
                timeInForce="GTC"
            )
            client.create_order(
                symbol=symbol,
                side=side,
                type="STOP_LOSS_LIMIT",
                quantity=qty,
                price=f"{sl:.2f}",
                stopPrice=f"{sl:.2f}",
                timeInForce="GTC"
            )

        print("✅ Órdenes TP/SL colocadas correctamente.")
        logger.info("Órdenes TP/SL colocadas correctamente.")
    except Exception as e:
        print(f"❌ Error al colocar TP/SL: {e}")
        logger.error(f"Error al colocar TP/SL: {e}")


# =============================================================================
# 💰 FUNCIÓN PRINCIPAL: Ejecutar trade (con ID y threading)
# =============================================================================
def execute_trade(client: Client, df, symbol: str, tp_pcts: list, sl_pcts: list,
                  balance_pct: float, trade_type: str):
    """
    Ejecuta una operación LONG o SHORT con monitoreo en hilo paralelo.
    Cada operación obtiene un ID único (trade_id) para evitar duplicaciones.
    """
    qty = calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=balance_pct)
    if qty <= 0:
        logger.warning("Cantidad calculada <= 0. Operación cancelada.")
        return None

    entry_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    trade_id = str(uuid.uuid4())[:8]  # 🆕 ID único para esta operación

    if trade_type == "LONG":
        print(f"🟢 Ejecutando LONG ({trade_id}) en {symbol} @ {entry_price:.2f}")
        order = place_market_buy(client, symbol, qty)
        tps = [entry_price * (1 + tp_pcts[0])]
        sls = [entry_price * (1 - sl_pcts[0])]
        order_id = order["orderId"] if order else f"SIMULATED_LONG_{trade_id}"
    else:
        print(f"🔴 Ejecutando SHORT (simulado) ({trade_id}) en {symbol} @ {entry_price:.2f}")
        order = {"orderId": f"SIMULATED_SHORT_{trade_id}", "fills": [{"price": str(entry_price)}]}
        tps = [entry_price * (1 - tp_pcts[0])]
        sls = [entry_price * (1 + sl_pcts[0])]
        order_id = order["orderId"]

    if not order:
        logger.error("❌ No se pudo ejecutar la orden. Abortando ciclo.")
        return None

    place_tp_sl_orders(client, symbol, qty, entry_price, tps, sls, [1.0], trade_type)

    log_trade(order_id, symbol, trade_type.lower(), qty, entry_price, sls[0], tps[0], None, 0.0)

    # 🧵 Lanzar monitoreo paralelo con ID único
    threading.Thread(
        target=monitor_orders,
        args=(client, symbol, entry_price, qty, tps[0], sls[0], trade_type, order_id),
        daemon=True
    ).start()

    logger.info(f"🚀 Hilo de monitoreo iniciado para {symbol} ({trade_type}) ID={order_id}")
    return order
