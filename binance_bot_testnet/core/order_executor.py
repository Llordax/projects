# =============================================================================
# MÓDULO: order_executor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo controla todo el flujo operativo de ejecución del bot:
#   1. Cálculo de cantidad de compra (según balance y porcentaje configurado)
#   2. Ejecución de la orden de compra al mercado.
#   3. Colocación de órdenes de Take Profit (TP) y Stop Loss (SL).
#   4. Registro del trade y monitoreo posterior.
#
# 🚀 Versión SCALPER SIMPLE:
#   - 1 Take Profit (+X%)
#   - 1 Stop Loss (-Y%)
#
# ⚙️ NUEVAS MEJORAS:
#   ✅ Cancelación automática de órdenes abiertas previas (para evitar error
#      `MAX_NUM_ALGO_ORDERS` cuando se alcanzan los límites de órdenes activas).
#   ✅ Documentación completa y trazabilidad con logs.
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
# 🔢 FUNCIÓN: Ajuste de cantidad según filtros de Binance
# =============================================================================
def adjust_quantity_to_filters(client: Client, symbol: str, quantity: float, price: float) -> float:
    """
    Ajusta la cantidad de compra o venta para cumplir con las restricciones
    de Binance (LOT_SIZE, MIN_NOTIONAL, etc.).

    Args:
        client (Client): Cliente de Binance autenticado.
        symbol (str): Par de trading, ej. "BTCEUR".
        quantity (float): Cantidad bruta calculada.
        price (float): Precio actual del activo.

    Returns:
        float: Cantidad ajustada y válida para la API.
    """
    try:
        info = client.get_symbol_info(symbol)
        lot, min_qty, min_notional = None, None, None

        # Recorre los filtros de Binance para obtener límites por símbolo
        for f in info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                lot = float(f["stepSize"])
                min_qty = float(f["minQty"])
            elif f["filterType"] == "MIN_NOTIONAL":
                min_notional = float(f["minNotional"])

        # Ajustes de tamaño de lote y valor mínimo
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
    """
    Ejecuta una orden de compra al mercado.

    Args:
        client (Client): Cliente de Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        quantity (float): Cantidad de compra ajustada.

    Returns:
        dict | None: Datos de la orden ejecutada, o None si falla.
    """
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        quantity = adjust_quantity_to_filters(client, symbol, quantity, price)

        # Formatear la cantidad según requisitos de Binance
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
# 🎯 FUNCIÓN: Cancelar órdenes abiertas (prevención de MAX_NUM_ALGO_ORDERS)
# =============================================================================
def cancel_existing_orders(client: Client, symbol: str):
    """
    Cancela todas las órdenes abiertas previas del símbolo indicado.
    Evita superar el límite de órdenes activas tipo STOP o LIMIT.

    Args:
        client (Client): Cliente de Binance autenticado.
        symbol (str): Par de trading, ej. "BTCEUR".
    """
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        if not open_orders:
            return

        for order in open_orders:
            try:
                client.cancel_order(symbol=symbol, orderId=order['orderId'])
                logger.info(f"🧹 Orden cancelada antes de nueva entrada: {order['orderId']}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo cancelar orden previa {order.get('orderId')}: {e}")

    except Exception as e:
        logger.error(f"Error al obtener órdenes abiertas: {e}")


# =============================================================================
# 🎯 FUNCIÓN: Colocar órdenes de Take Profit y Stop Loss
# =============================================================================
def place_tp_sl_orders(client: Client, symbol: str, quantity: float,
                       entry_price: float, tps: list, sls: list, qty_splits: list):
    """
    Coloca una orden de Take Profit (TP) y una de Stop Loss (SL).

    Args:
        client (Client): Cliente de Binance.
        symbol (str): Par de trading.
        quantity (float): Cantidad total a vender.
        entry_price (float): Precio de entrada.
        tps (list): Lista de precios de TP calculados.
        sls (list): Lista de precios de SL calculados.
        qty_splits (list): Fracciones de cantidad a aplicar por TP/SL.

    Notas:
        - Antes de crear las nuevas órdenes, se cancelan las previas.
        - En Testnet, las órdenes TP/SL no se ejecutan automáticamente;
          el monitoreo simula la ejecución.
    """
    try:
        # 🧹 Cancelar órdenes previas del mismo símbolo
        cancel_existing_orders(client, symbol)

        # Calcular precios TP y SL redondeados
        tp = round(tps[0], 2)
        sl = round(sls[0], 2)
        stop_price = round(sls[0] * 0.999, 2)

        # Ajustar cantidad a restricciones de Binance
        qty = adjust_quantity_to_filters(client, symbol, quantity, tp)
        safe_qty = format(qty, '.6f').rstrip('0').rstrip('.')

        # Crear orden de venta Take Profit
        client.order_limit_sell(
            symbol=symbol,
            quantity=safe_qty,
            price=f"{tp:.2f}",
            timeInForce=Client.TIME_IN_FORCE_GTC
        )

        # Crear orden de venta Stop Loss
        client.create_order(
            symbol=symbol,
            side='SELL',
            type='STOP_LOSS_LIMIT',
            quantity=safe_qty,
            price=f"{sl:.2f}",
            stopPrice=f"{stop_price:.2f}",
            timeInForce='GTC'
        )

        print(f"🎯 TP en {tp:.2f} | 🛑 SL en {sl:.2f}")
        logger.info(f"TP/SL colocados → TP={tp:.2f} | SL={sl:.2f}")

    except Exception as e:
        print(f"❌ Error al colocar TP/SL: {e}")
        logger.error(f"Error al colocar TP/SL: {e}")


# =============================================================================
# 💶 FUNCIÓN: Calcular cantidad de compra según balance disponible
# =============================================================================
def calculate_trade_quantity(client: Client, symbol: str,
                             balance_asset: str = 'EUR', balance_pct: float = 0.15) -> float:
    """
    Calcula la cantidad a comprar en función del balance disponible.

    Args:
        client (Client): Cliente de Binance autenticado.
        symbol (str): Par de trading (ejemplo "BTCEUR").
        balance_asset (str): Moneda base del balance (por defecto, EUR).
        balance_pct (float): Porcentaje del balance a invertir.

    Returns:
        float: Cantidad calculada (ajustada posteriormente a filtros).
    """
    try:
        bal = float(client.get_asset_balance(asset=balance_asset)['free'])
        use = bal * balance_pct
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        qty = round(use / price, 8)

        print(f"💶 Balance {balance_asset}: {bal:.2f} | Invirtiendo {use:.2f}")
        logger.info(f"Cantidad calculada: {qty} ({balance_pct*100:.1f}% del balance)")

        return qty

    except Exception as e:
        logger.error(f"Error al calcular cantidad: {e}")
        return 0.0


# =============================================================================
# 🚀 FUNCIÓN PRINCIPAL: Ejecución completa del trade
# =============================================================================
def execute_trade(client: Client, df, symbol: str, tp_pcts: list, sl_pcts: list, balance_pct: float):
    """
    Flujo completo de ejecución de una operación (compra + TP/SL + monitoreo).

    Pasos:
        1. Calcular la cantidad a invertir según balance.
        2. Ejecutar la orden de compra al mercado.
        3. Calcular niveles de Take Profit y Stop Loss.
        4. Colocar las órdenes de salida (TP/SL).
        5. Registrar la operación en el Excel y los logs.
        6. Iniciar monitoreo hasta ejecución simulada (en Testnet).

    Args:
        client (Client): Cliente de Binance autenticado.
        df (pd.DataFrame): DataFrame con datos de precios (no usado directamente).
        symbol (str): Par de trading.
        tp_pcts (list): Lista de porcentajes de ganancia.
        sl_pcts (list): Lista de porcentajes de pérdida.
        balance_pct (float): Porcentaje del balance a invertir.
    """
    # 1️⃣ Calcular cantidad a comprar
    qty = calculate_trade_quantity(client, symbol, balance_asset='EUR', balance_pct=balance_pct)
    if qty <= 0:
        logger.warning("Cantidad calculada <= 0. Operación cancelada.")
        return

    # 2️⃣ Ejecutar compra al mercado
    order = place_market_buy(client, symbol, qty)
    if not order:
        logger.error("Compra no ejecutada. Abortando ciclo.")
        return

    entry = float(order['fills'][0]['price'])

    # 3️⃣ Calcular precios TP y SL
    tps, sls = compute_tp_sl(entry, tp_pcts, sl_pcts)

    # 4️⃣ Colocar TP/SL (tras limpiar órdenes anteriores)
    place_tp_sl_orders(client, symbol, qty, entry, tps, sls, [1.0])

    # 5️⃣ Registrar trade inicial
    log_trade(order["orderId"], symbol, "buy", qty, entry, sls[0], tps[0], None, 0.0)

    # 6️⃣ Monitorear ejecución (simulada o real)
    monitor_orders(client, symbol, entry, qty)
