"""
===============================================================================
MÓDULO: order_executor.py
-------------------------------------------------------------------------------
Responsable de la **ejecución de órdenes en Binance** y de la gestión completa 
del flujo de operaciones del bot de trading.

FUNCIONALIDADES PRINCIPALES:
    ✅ Ejecutar órdenes de compra al mercado (market orders).
    ✅ Calcular automáticamente la cantidad a comprar en función del balance USDT.
    ✅ Ajustar la cantidad al tamaño de lote permitido por Binance (LOT_SIZE).
    ✅ Colocar órdenes de Take Profit (TP) y Stop Loss (SL) válidas para Spot.
    ✅ Registrar cada operación ejecutada en logs y en un archivo Excel.
    ✅ Manejar errores y excepciones para evitar interrupciones en la ejecución.

NOTAS:
    - Compatible con Binance Spot Testnet y producción.
    - Todos los logs se registran mediante el logger centralizado del bot.
    - El archivo Excel puede quedar bloqueado si está abierto: el módulo lo gestiona.
    - Se recomienda siempre probar en Testnet antes de operar en real.

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
# 🔧 FUNCIÓN AUXILIAR: Ajuste de cantidad según LOT_SIZE
# =============================================================================
def adjust_quantity_to_lot_size(client: Client, symbol: str, quantity: float) -> float:
    """
    Ajusta la cantidad a comprar o vender de acuerdo con las restricciones del par de trading.

    Binance impone reglas de tamaño de lote (LOT_SIZE), que definen:
        - stepSize: Incremento válido entre cantidades.
        - minQty: Cantidad mínima permitida.
        - maxQty: Cantidad máxima permitida.

    Esta función evita el error:
        ❌ APIError(code=-1013): Filter failure: LOT_SIZE

    Args:
        client (Client): Instancia autenticada del cliente de Binance.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad original calculada.

    Returns:
        float: Cantidad ajustada que cumple con LOT_SIZE.
    """
    try:
        symbol_info = client.get_symbol_info(symbol)
        lot_size = None
        min_qty = None

        # Buscar el filtro de tipo LOT_SIZE
        for f in symbol_info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                lot_size = float(f["stepSize"])
                min_qty = float(f["minQty"])
                break

        if lot_size:
            adjusted_qty = math.floor(quantity / lot_size) * lot_size
            if adjusted_qty < min_qty:
                adjusted_qty = min_qty
            adjusted_qty = float(f"{adjusted_qty:.8f}")
            return adjusted_qty

        return quantity

    except Exception as e:
        logger.error(f"Error al ajustar cantidad según LOT_SIZE: {e}")
        return quantity


# =============================================================================
# 🟢 FUNCIÓN: Orden de compra al mercado
# =============================================================================
def place_market_buy(client: Client, symbol: str, quantity: float):
    """
    Ejecuta una orden de compra al mercado (market order).

    Antes de enviarla, ajusta automáticamente la cantidad al tamaño de lote permitido.

    Args:
        client (Client): Cliente autenticado de Binance.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad inicial a comprar (se ajustará automáticamente).

    Returns:
        dict | None: Respuesta de la orden ejecutada si es exitosa, o None si falla.
    """
    try:
        adjusted_qty = adjust_quantity_to_lot_size(client, symbol, quantity)
        print(f"🟢 Ejecutando compra de {adjusted_qty} {symbol} al mercado...")
        logger.info(f"Ejecutando compra de {adjusted_qty} {symbol} al mercado...")

        order = client.order_market_buy(symbol=symbol, quantity=adjusted_qty)

        print("✅ Orden de compra ejecutada correctamente.")
        logger.info("Orden de compra ejecutada correctamente.")
        return order

    except Exception as e:
        print(f"❌ Error al ejecutar orden de compra: {e}")
        logger.error(f"Error al ejecutar orden de compra: {e}")
        return None


# =============================================================================
# 🎯 FUNCIÓN: Colocar órdenes TP/SL
# =============================================================================
def place_tp_sl_orders(client: Client, symbol: str, quantity: float, entry_price: float,
                       tps: list, sls: list, qty_splits: list):
    """
    Coloca automáticamente las órdenes de Take Profit (TP) y Stop Loss (SL) 
    según los niveles calculados en la estrategia.

    En Binance Spot, las órdenes Stop Limit se crean mediante `type='STOP_LOSS_LIMIT'`.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad total comprada.
        entry_price (float): Precio de entrada en la operación.
        tps (list[float]): Lista de precios objetivo (Take Profit).
        sls (list[float]): Lista de precios Stop Loss.
        qty_splits (list[float]): Porcentajes de división de cantidad entre niveles.
    """
    for i in range(3):
        qty = round(quantity * qty_splits[i], 6)
        tp_price = round(tps[i], 2)
        sl_price = round(sls[i], 2)
        stop_price = round(sls[i] * 0.999, 2)

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
# 💰 FUNCIÓN: Cálculo de cantidad BTC
# =============================================================================
def calculate_btc_quantity(client, symbol, usdt_percentage=0.15):
    """
    Calcula la cantidad de BTC a comprar según el balance disponible en USDT.

    El cálculo se basa en:
        - Balance actual en EUR.
        - Porcentaje configurado a invertir (por defecto 15%).
        - Precio actual del símbolo (BTCEUR).

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading.
        usdt_percentage (float): Porcentaje del balance a usar.

    Returns:
        float: Cantidad estimada de BTC a comprar (redondeada a 6 decimales).
    """
    try:
        usdt_balance = float(client.get_asset_balance(asset='EUR')['free'])
        usdt_to_use = usdt_balance * usdt_percentage
        btc_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        btc_quantity = round(usdt_to_use / btc_price, 6)

        print(f"💵 USDT disponible: {usdt_balance:.2f}")
        print(f"📌 Usando {usdt_percentage * 100:.0f}%: {usdt_to_use:.2f} EUR")
        print(f"💱 Precio BTC: {btc_price:.2f}")
        print(f"🟢 BTC a comprar (previo a ajuste): {btc_quantity}")

        logger.info(f"EUR disponible: {usdt_balance:.2f}, usando: {usdt_to_use:.2f} EUR, "
                    f"precio BTC: {btc_price:.2f}, BTC a comprar: {btc_quantity}")

        return btc_quantity

    except Exception as e:
        print(f"❌ Error al calcular cantidad de BTC: {e}")
        logger.error(f"Error al calcular cantidad de BTC: {e}")
        return 0.0


# =============================================================================
# ⚙️ FUNCIÓN PRINCIPAL: Ejecución completa del trade
# =============================================================================
def execute_trade(client, df, symbol, tp_pcts, sl_pcts, usdt_percentage):
    """
    Ejecuta el flujo completo de una operación de trading:

    1️⃣ Calcula la cantidad a comprar según el balance.
    2️⃣ Ajusta la cantidad según las reglas de Binance (LOT_SIZE).
    3️⃣ Ejecuta la orden de compra al mercado.
    4️⃣ Calcula y coloca los niveles de TP y SL.
    5️⃣ Registra la operación en logs y en Excel.

    Args:
        client (Client): Cliente Binance autenticado.
        df (pd.DataFrame): Datos OHLCV del activo.
        symbol (str): Par de trading.
        tp_pcts (list[float]): Porcentajes para Take Profit.
        sl_pcts (list[float]): Porcentajes para Stop Loss.
        usdt_percentage (float): Porcentaje del balance a usar.
    """
    # 1️⃣ Calcular la cantidad de BTC a comprar
    buy_quantity = calculate_btc_quantity(client, symbol, usdt_percentage)
    if buy_quantity == 0:
        print("❌ Cantidad calculada inválida. No se ejecuta la compra.")
        logger.warning("Cantidad calculada inválida. No se ejecuta la compra.")
        return

    # 2️⃣ Ajustar la cantidad a LOT_SIZE antes de comprar
    buy_quantity = adjust_quantity_to_lot_size(client, symbol, buy_quantity)

    # 3️⃣ Ejecutar orden de compra
    buy_order = place_market_buy(client, symbol, buy_quantity)
    if not buy_order:
        print("❌ No se pudo ejecutar la compra. Se omiten TP/SL.")
        logger.error("No se pudo ejecutar la compra. Se omiten TP/SL.")
        return

    # 4️⃣ Registrar el precio real de entrada
    entry_price = float(buy_order['fills'][0]['price'])
    print(f"📌 Precio real de entrada: {entry_price}")
    logger.info(f"Precio real de entrada: {entry_price}")

    # 5️⃣ Calcular y colocar órdenes TP/SL
    tps, sls = compute_tp_sl(entry_price, tp_pcts, sl_pcts)
    place_tp_sl_orders(client, symbol, buy_quantity, entry_price, tps, sls, [0.33, 0.33, 0.34])

    # 6️⃣ Registrar operación en Excel
    try:
        log_trade(
            order_id=buy_order["orderId"],
            ticker=symbol,
            order_type="buy",
            qty=buy_quantity,
            price_open=entry_price,
            price_sl=sls[0],
            price_tp=tps[-1],
            price_closed=entry_price,
            pnl=(tps[-1] - entry_price) * buy_quantity
        )
        print("📒 Operación registrada en Excel correctamente.")
        logger.info("📒 Operación registrada en Excel correctamente.")

    except PermissionError:
        print("⚠️ El archivo Excel está abierto. No se pudo escribir la operación.")
        logger.warning("El archivo Excel está abierto. No se pudo escribir la operación.")

    except Exception as e:
        print(f"❌ Error al guardar operación en Excel: {e}")
        logger.error(f"Error al guardar operación en Excel: {e}")
