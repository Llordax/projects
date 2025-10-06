from binance.client import Client
from core.risk_management import compute_tp_sl
from utils.logger import log_trade
from utils.logger_setup import logger
import time

def place_market_buy(client: Client, symbol: str, quantity: float):
    try:
        print(f"🟢 Ejecutando compra de {quantity} {symbol} al mercado...")
        logger.info(f"Ejecutando compra de {quantity} {symbol} al mercado...")
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print("✅ Orden de compra ejecutada.")
        logger.info("Orden de compra ejecutada.")
        return order
    except Exception as e:
        print(f"❌ Error al ejecutar orden de compra: {e}")
        logger.error(f"Error al ejecutar orden de compra: {e}")
        return None

def place_tp_sl_orders(client: Client, symbol: str, quantity: float, entry_price: float, tps: list, sls: list, qty_splits: list):
    for i in range(3):
        qty = round(quantity * qty_splits[i], 6)
        tp_price = round(tps[i], 2)
        sl_price = round(sls[i], 2)
        stop_price = round(sls[i] * 0.999, 2)

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

        try:
            client.order_stop_limit_sell(
                symbol=symbol,
                quantity=qty,
                price=str(sl_price),
                stopPrice=str(stop_price),
                timeInForce=Client.TIME_IN_FORCE_GTC
            )
            print(f"🛑 SL{i+1} colocado en {sl_price} (stop: {stop_price}) con {qty} {symbol}")
            logger.info(f"SL{i+1} colocado en {sl_price} (stop: {stop_price}) con {qty} {symbol}")
        except Exception as e:
            print(f"❌ Error en SL{i+1}: {e}")
            logger.error(f"Error en SL{i+1}: {e}")
        time.sleep(0.5)

def calculate_btc_quantity(client, symbol, usdt_percentage=0.15):
    try:
        usdt_balance = float(client.get_asset_balance(asset='USDT')['free'])
        usdt_to_use = usdt_balance * usdt_percentage
        btc_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        btc_quantity = round(usdt_to_use / btc_price, 6)

        print(f"💵 USDT disponible: {usdt_balance:.2f}")
        print(f"📌 Usando {usdt_percentage * 100:.0f}%: {usdt_to_use:.2f} USDT")
        print(f"💱 Precio BTC: {btc_price:.2f}")
        print(f"🟢 BTC a comprar: {btc_quantity}")

        logger.info(f"USDT disponible: {usdt_balance:.2f}, usando: {usdt_to_use:.2f} USDT, precio BTC: {btc_price:.2f}, BTC a comprar: {btc_quantity}")

        return btc_quantity
    except Exception as e:
        print(f"❌ Error al calcular cantidad de BTC: {e}")
        logger.error(f"Error al calcular cantidad de BTC: {e}")
        return 0.0

def execute_trade(client, df, symbol, tp_pcts, sl_pcts, usdt_percentage):
    buy_quantity = calculate_btc_quantity(client, symbol, usdt_percentage)
    if buy_quantity == 0:
        print("❌ Cantidad calculada inválida. No se ejecuta la compra.")
        logger.warning("Cantidad calculada inválida. No se ejecuta la compra.")
        return

    buy_order = place_market_buy(client, symbol, buy_quantity)
    if not buy_order:
        print("❌ No se pudo ejecutar la compra. Se omiten TP/SL.")
        logger.error("No se pudo ejecutar la compra. Se omiten TP/SL.")
        return

    entry_price = float(buy_order['fills'][0]['price'])
    print(f"📌 Precio real de entrada: {entry_price}")
    logger.info(f"Precio real de entrada: {entry_price}")

    tps, sls = compute_tp_sl(entry_price, tp_pcts, sl_pcts)
    place_tp_sl_orders(client, symbol, buy_quantity, entry_price, tps, sls, [0.33, 0.33, 0.34])

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
        logger.info("📒 Operación registrada en Excel")
    except Exception as e:
        print(f"❌ Error al guardar operación en Excel: {e}")
        logger.error(f"Error al guardar operación en Excel: {e}")
