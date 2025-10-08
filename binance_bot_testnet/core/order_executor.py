# =============================================================================
# MÓDULO: order_executor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# ----------------------------------------------------------------------------- 
# Este módulo gestiona **toda la ejecución operativa** del bot de trading en Binance.
# 
# Funcionalidades principales:
#   ✅ Ejecuta órdenes de compra al mercado.
#   ✅ Calcula automáticamente la cantidad a invertir en función del balance disponible.
#   ✅ Ajusta la cantidad de compra según los filtros de Binance (LOT_SIZE, MIN_NOTIONAL).
#   ✅ Coloca órdenes de Take Profit (TP) y Stop Loss (SL) válidas para Spot.
#   ✅ Registra las operaciones ejecutadas en logs y Excel.
#   ✅ Supervisa en tiempo real la ejecución de TP/SL.
#   ✅ Gestiona de forma segura excepciones y errores.
#
# Este módulo actúa como **capa intermedia** entre la estrategia del bot y la API de Binance,
# asegurando que cada operación cumpla los parámetros de riesgo, formato y restricciones del exchange.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - binance.client.Client
#   - core.risk_management.compute_tp_sl
#   - core.order_monitor.monitor_orders
#   - utils.logger.log_trade
#   - utils.logger_setup.logger
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from binance.client import Client
from core.risk_management import compute_tp_sl
from core.order_monitor import monitor_orders  # 👁️ NUEVO: módulo que detecta ejecución TP/SL
from utils.logger import log_trade
from utils.logger_setup import logger
import time
import math


# =============================================================================
# 🔧 FUNCIÓN AUXILIAR: Ajuste de cantidad según LOT_SIZE y MIN_NOTIONAL
# =============================================================================
def adjust_quantity_to_filters(client: Client, symbol: str, quantity: float, price: float) -> float:
    """
    Ajusta la cantidad de una orden para cumplir las restricciones del mercado en Binance.

    La función verifica los filtros de símbolo del par (symbol) y modifica la cantidad
    según los siguientes criterios:
        - LOT_SIZE: incrementos válidos de cantidad.
        - MIN_NOTIONAL: valor mínimo total de operación.

    Args:
        client (Client): Instancia autenticada del cliente de Binance.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad original propuesta para la operación.
        price (float): Precio actual del activo.

    Returns:
        float: Cantidad ajustada que cumple con los filtros de Binance.
    """
    try:
        symbol_info = client.get_symbol_info(symbol)
        lot_size, min_qty, min_notional = None, None, None

        # Se recorren los filtros para extraer restricciones relevantes del mercado
        for f in symbol_info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                lot_size = float(f["stepSize"])
                min_qty = float(f["minQty"])
            elif f["filterType"] == "MIN_NOTIONAL":
                min_notional = float(f["minNotional"])

        # Ajuste según tamaño de lote (LOT_SIZE)
        if lot_size:
            quantity = math.floor(quantity / lot_size) * lot_size

        # Evitar cantidades menores al mínimo permitido
        if min_qty and quantity < min_qty:
            quantity = min_qty

        # Asegurar que el valor total supere el mínimo notional
        if min_notional and (quantity * price) < min_notional:
            quantity = min_notional / price

        # Redondear a 8 decimales para evitar errores de precisión
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
    Ejecuta una orden de compra al mercado en Binance Spot.

    La función ajusta la cantidad automáticamente según los filtros de Binance
    antes de enviar la orden de compra.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad inicial a comprar.

    Returns:
        dict | None: Objeto de respuesta de la orden si es exitosa, o None si ocurre un error.
    """
    try:
        # Obtener precio de mercado actual y ajustar cantidad
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = adjust_quantity_to_filters(client, symbol, quantity, price)

        print(f"🟢 Ejecutando compra de {quantity} {symbol} al mercado...")
        logger.info(f"Ejecutando compra de {quantity} {symbol} al mercado...")

        # Envío de orden de compra tipo Market
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
    Coloca las órdenes de Take Profit (TP) y Stop Loss (SL) correspondientes a una operación abierta.

    Cada nivel de TP y SL se ajusta automáticamente según los filtros de Binance
    para cumplir los límites mínimos de cantidad y valor notional.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading.
        quantity (float): Cantidad total comprada.
        entry_price (float): Precio de entrada de la operación.
        tps (list[float]): Lista de niveles de Take Profit.
        sls (list[float]): Lista de niveles de Stop Loss.
        qty_splits (list[float]): Proporción de cantidad por cada nivel de salida.
    """
    for i in range(3):
        # Calcular cantidad y precios para cada nivel
        qty = round(quantity * qty_splits[i], 8)
        tp_price = round(tps[i], 2)
        sl_price = round(sls[i], 2)
        stop_price = round(sls[i] * 0.999, 2)  # Margen para activación del SL

        # Ajustar cantidad según filtros Binance
        qty = adjust_quantity_to_filters(client, symbol, qty, tp_price)

        # 🟩 Colocación de Take Profit
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

        # 🟥 Colocación de Stop Loss (orden de venta condicional)
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
    Calcula la cantidad de activo a comprar según el balance disponible y un porcentaje definido.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        balance_asset (str): Activo base en el que se posee el balance (por defecto 'EUR').
        balance_pct (float): Porcentaje del balance a invertir (ej. 0.15 = 15%).

    Returns:
        float: Cantidad del activo a comprar, ajustada a 8 decimales.
    """
    try:
        # Obtener balance disponible y calcular inversión
        balance = float(client.get_asset_balance(asset=balance_asset)['free'])
        to_use = balance * balance_pct
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = round(to_use / price, 8)

        # Mostrar información útil al usuario
        print(f"💵 {balance_asset} disponible: {balance:.2f}")
        print(f"📌 Usando {balance_pct * 100:.0f}%: {to_use:.2f} {balance_asset}")
        print(f"💱 Precio {symbol}: {price:.2f}")
        print(f"🟢 Cantidad calculada: {quantity}")

        logger.info(f"{balance_asset} disponible: {balance:.2f}, usando: {to_use:.2f}, "
                    f"precio {symbol}: {price:.2f}, cantidad: {quantity}")

        return quantity

    except Exception as e:
        print(f"❌ Error al calcular cantidad: {e}")
        logger.error(f"Error al calcular cantidad: {e}")
        return 0.0


# =============================================================================
# ⚙️ FUNCIÓN PRINCIPAL: Ejecución completa de una operación
# =============================================================================
def execute_trade(client, df, symbol, tp_pcts, sl_pcts, balance_pct):
    """
    Ejecuta el flujo operativo completo de un trade:
        1️⃣ Calcula la cantidad de compra en función del balance.
        2️⃣ Ejecuta la orden de compra al mercado.
        3️⃣ Calcula y coloca los niveles de Take Profit y Stop Loss.
        4️⃣ Registra la operación en Excel y logs.
        5️⃣ Inicia la monitorización activa de órdenes TP/SL.

    Args:
        client (Client): Cliente Binance autenticado.
        df (DataFrame): Dataset o estructura con información de entrada (no usado directamente).
        symbol (str): Par de trading.
        tp_pcts (list[float]): Porcentajes de Take Profit.
        sl_pcts (list[float]): Porcentajes de Stop Loss.
        balance_pct (float): Porcentaje del balance a invertir.
    """
    # 1️⃣ Calcular la cantidad de compra
    buy_qty = calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=balance_pct)
    if buy_qty <= 0:
        print("❌ Cantidad inválida. Se omite la operación.")
        logger.warning("Cantidad inválida. Se omite la operación.")
        return

    # 2️⃣ Ejecutar la compra al mercado
    order = place_market_buy(client, symbol, buy_qty)
    if not order:
        print("❌ No se pudo ejecutar la compra.")
        logger.error("No se pudo ejecutar la compra.")
        return

    # 3️⃣ Obtener el precio real de entrada de la orden ejecutada
    entry_price = float(order['fills'][0]['price'])
    print(f"📌 Precio real de entrada: {entry_price}")
    logger.info(f"Precio real de entrada: {entry_price}")

    # 4️⃣ Calcular niveles de TP y SL según porcentajes definidos
    tps, sls = compute_tp_sl(entry_price, tp_pcts, sl_pcts)
    place_tp_sl_orders(client, symbol, buy_qty, entry_price, tps, sls, [0.33, 0.33, 0.34])

    # 5️⃣ Registrar la operación en Excel y logs
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

    # 6️⃣ Iniciar la monitorización activa de órdenes TP/SL
    try:
        print("👁️ Iniciando monitoreo de TP/SL...")
        monitor_orders(client, symbol, entry_price, buy_qty)
    except Exception as e:
        print(f"⚠️ Error en monitorización: {e}")
        logger.error(f"Error en monitorización: {e}")
