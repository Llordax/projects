"""
===============================================================================
MÓDULO: order_executor.py
-------------------------------------------------------------------------------
Responsable de la **ejecución de órdenes en Binance** y de la gestión completa 
del flujo de operaciones del bot de trading.

FUNCIONALIDADES PRINCIPALES:
    ✅ Ejecutar órdenes de compra al mercado (market orders).
    ✅ Calcular automáticamente la cantidad a comprar en función del balance EUR/USDT.
    ✅ Ajustar la cantidad al tamaño de lote permitido por Binance (LOT_SIZE).
    ✅ Validar el valor mínimo de operación (MIN_NOTIONAL).
    ✅ Colocar órdenes de Take Profit (TP) y Stop Loss (SL) válidas para Spot.
    ✅ Registrar cada operación ejecutada en logs y en un archivo Excel.
    ✅ Manejar errores y excepciones para evitar interrupciones en la ejecución.

Autor: Alejandro Llordén Rodríguez
Fecha: Octubre 2025
===============================================================================
"""

from binance.client import Client
from core.risk_management import compute_tp_sl
from utils.logger import log_trade
from utils.logger_setup import logger
import time
import math


# =============================================================================
# 🔧 FUNCIÓN AUXILIAR: Ajuste de cantidad según LOT_SIZE y MIN_NOTIONAL
# =============================================================================
def adjust_quantity_to_filters(client: Client, symbol: str, quantity: float, price: float) -> float:
    """
    Ajusta la cantidad a comprar o vender de acuerdo con las restricciones de Binance:
    LOT_SIZE (incremento válido) y MIN_NOTIONAL (valor mínimo en moneda cotizada).

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad propuesta.
        price (float): Precio actual del activo.

    Returns:
        float: Cantidad ajustada que cumple con LOT_SIZE y MIN_NOTIONAL.
    """
    try:
        symbol_info = client.get_symbol_info(symbol)
        lot_size, min_qty, min_notional = None, None, None

        for f in symbol_info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                lot_size = float(f["stepSize"])
                min_qty = float(f["minQty"])
            elif f["filterType"] == "MIN_NOTIONAL":
                min_notional = float(f["minNotional"])

        # Ajuste según LOT_SIZE
        if lot_size:
            quantity = math.floor(quantity / lot_size) * lot_size
        if min_qty and quantity < min_qty:
            quantity = min_qty

        # Ajuste según MIN_NOTIONAL
        if min_notional and (quantity * price) < min_notional:
            # Eleva la cantidad hasta cumplir el valor mínimo
            quantity = min_notional / price

        quantity = float(f"{quantity:.8f}")
        return quantity

    except Exception as e:
        logger.error(f"Error al ajustar cantidad según filtros Binance: {e}")
        return quantity


# =============================================================================
# 🟢 FUNCIÓN: Orden de compra al mercado
# =============================================================================
def place_market_buy(client: Client, symbol: str, quantity: float):
    """
    Ejecuta una orden de compra al mercado ajustando la cantidad automáticamente
    a los filtros de Binance.

    Args:
        client (Client): Cliente autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad inicial a comprar.

    Returns:
        dict | None: Respuesta de la orden ejecutada si es exitosa, o None si falla.
    """
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = adjust_quantity_to_filters(client, symbol, quantity, price)

        print(f"🟢 Ejecutando compra de {quantity} {symbol} al mercado...")
        logger.info(f"Ejecutando compra de {quantity} {symbol} al mercado...")

        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print("✅ Orden de compra ejecutada correctamente.")
        logger.info("Orden de compra ejecutada correctamente.")
        return order

    except Exception as e:
        print(f"❌ Error al ejecutar orden de compra: {e}")
        logger.error(f"Error al ejecutar orden de compra: {e}")
        return None


# =============================================================================
# 🎯 FUNCIÓN: Colocar órdenes TP/SL con validación de filtros
# =============================================================================
def place_tp_sl_orders(client: Client, symbol: str, quantity: float, entry_price: float,
                       tps: list, sls: list, qty_splits: list):
    """
    Coloca órdenes de Take Profit y Stop Loss válidas en Binance Spot.

    Args:
        client (Client): Cliente autenticado.
        symbol (str): Par de trading.
        quantity (float): Cantidad total comprada.
        entry_price (float): Precio de entrada.
        tps (list[float]): Niveles de Take Profit.
        sls (list[float]): Niveles de Stop Loss.
        qty_splits (list[float]): Proporciones de cantidad por nivel.
    """
    for i in range(3):
        qty = round(quantity * qty_splits[i], 8)
        tp_price = round(tps[i], 2)
        sl_price = round(sls[i], 2)
        stop_price = round(sls[i] * 0.999, 2)

        # Ajustar cantidad según filtros
        qty = adjust_quantity_to_filters(client, symbol, qty, tp_price)

        # TAKE PROFIT
        try:
            client.order_limit_sell(
                symbol=symbol,
                quantity=qty,
                price=str(tp_price),
                timeInForce=Client.TIME_IN_FORCE_GTC
            )
            print(f"🎯 TP{i+1} colocado en {tp_price} con {qty} {symbol}")
            logger.info(f"TP{i+1} colocado en {tp_price} con {qty} {symbol}")
        except Exception as e:
            print(f"❌ Error en TP{i+1}: {e}")
            logger.error(f"Error en TP{i+1}: {e}")
        time.sleep(0.5)

        # STOP LOSS
        try:
            qty = adjust_quantity_to_filters(client, symbol, qty, sl_price)
            client.create_order(
                symbol=symbol,
                side='SELL',
                type='STOP_LOSS_LIMIT',
                quantity=qty,
                price=str(sl_price),
                stopPrice=str(stop_price),
                timeInForce='GTC'
            )
            print(f"🛑 SL{i+1} colocado en {sl_price} (stop: {stop_price}) con {qty} {symbol}")
            logger.info(f"SL{i+1} colocado en {sl_price} (stop: {stop_price}) con {qty} {symbol}")
        except Exception as e:
            print(f"❌ Error en SL{i+1}: {e}")
            logger.error(f"Error en SL{i+1}: {e}")
        time.sleep(0.5)


# =============================================================================
# 💰 FUNCIÓN: Calcular cantidad a comprar
# =============================================================================
def calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=0.15):
    """
    Calcula la cantidad a comprar en función del balance disponible.

    Args:
        client (Client): Cliente autenticado.
        symbol (str): Par de trading.
        balance_asset (str): Moneda base (EUR, USDT, USDC, etc.).
        balance_pct (float): Porcentaje del balance a usar.

    Returns:
        float: Cantidad a comprar.
    """
    try:
        balance = float(client.get_asset_balance(asset=balance_asset)['free'])
        to_use = balance * balance_pct
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = round(to_use / price, 8)

        print(f"💵 {balance_asset} disponible: {balance:.2f}")
        print(f"📌 Usando {balance_pct * 100:.0f}%: {to_use:.2f} {balance_asset}")
        print(f"💱 Precio {symbol}: {price:.2f}")
        print(f"🟢 Cantidad calculada: {quantity}")
        logger.info(f"{balance_asset} disponible: {balance:.2f}, usando: {to_use:.2f}, precio {symbol}: {price:.2f}, cantidad: {quantity}")

        return quantity

    except Exception as e:
        print(f"❌ Error al calcular cantidad: {e}")
        logger.error(f"Error al calcular cantidad: {e}")
        return 0.0


# =============================================================================
# ⚙️ FUNCIÓN PRINCIPAL: Ejecución del trade completo
# =============================================================================
def execute_trade(client, df, symbol, tp_pcts, sl_pcts, balance_pct):
    """
    Ejecuta el flujo completo de una operación:
    1️⃣ Calcula cantidad.
    2️⃣ Compra al mercado.
    3️⃣ Coloca TP/SL.
    4️⃣ Registra la operación.
    """
    buy_qty = calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=balance_pct)
    if buy_qty <= 0:
        print("❌ Cantidad inválida. Se omite la operación.")
        logger.warning("Cantidad inválida. Se omite la operación.")
        return

    order = place_market_buy(client, symbol, buy_qty)
    if not order:
        print("❌ No se pudo ejecutar la compra.")
        logger.error("No se pudo ejecutar la compra.")
        return

    entry_price = float(order['fills'][0]['price'])
    print(f"📌 Precio real de entrada: {entry_price}")
    logger.info(f"Precio real de entrada: {entry_price}")

    tps, sls = compute_tp_sl(entry_price, tp_pcts, sl_pcts)
    place_tp_sl_orders(client, symbol, buy_qty, entry_price, tps, sls, [0.33, 0.33, 0.34])

    # Registro en Excel
    try:
        log_trade(
            order_id=order["orderId"],
            ticker=symbol,
            order_type="buy",
            qty=buy_qty,
            price_open=entry_price,
            price_sl=sls[0],
            price_tp=tps[-1],
            price_closed=entry_price,
            pnl=(tps[-1] - entry_price) * buy_qty
        )
        print("📒 Operación registrada correctamente en Excel.")
        logger.info("📒 Operación registrada correctamente en Excel.")
    except Exception as e:
        print(f"⚠️ Error al registrar operación: {e}")
        logger.error(f"Error al registrar operación: {e}")
