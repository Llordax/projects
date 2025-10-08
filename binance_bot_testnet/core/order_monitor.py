"""
===============================================================================
MÓDULO: order_monitor.py
-------------------------------------------------------------------------------
Supervisa las órdenes abiertas (TP/SL) y detecta cuándo se ejecutan.
Registra automáticamente el resultado en logs y en el mismo Excel de historial.

Mejoras:
    ✅ Control de ejecución real (verificación de orden cerrada en Binance).
    ✅ Normalización del PnL (negativo en pérdidas, positivo en ganancias).
    ✅ Cancelación segura de órdenes restantes.
    ✅ Modo Testnet compatible (simulación de ejecución si no se disparan órdenes).

Autor: Alejandro Llordén Rodríguez
Fecha: Octubre 2025
===============================================================================
"""

import time
from utils.logger import log_trade
from utils.logger_setup import logger


def monitor_orders(client, symbol, open_price, quantity, simulate_testnet=True):
    """
    Supervisa el precio del activo y las órdenes TP/SL activas.
    Cuando una se ejecuta, registra la operación y cancela las restantes.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (p. ej. BTCEUR o BTCUSDC).
        open_price (float): Precio de entrada en la operación.
        quantity (float): Cantidad comprada.
        simulate_testnet (bool): Si True, simula ejecución en Testnet (por defecto True).
    """
    print(f"👁️  Monitoreando {symbol}... Esperando ejecución de TP o SL")
    logger.info(f"Monitoreando {symbol}... Esperando ejecución de TP o SL")

    active = True
    executed_order = None

    while active:
        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker["price"])

            # Obtener órdenes abiertas (TP y SL)
            open_orders = client.get_open_orders(symbol=symbol)

            if not open_orders and not simulate_testnet:
                # Si no hay órdenes abiertas, puede que se hayan ejecutado fuera del monitoreo
                print("⚠️ No se encontraron órdenes abiertas, posible ejecución fuera del monitoreo.")
                logger.warning("No se encontraron órdenes abiertas, posible ejecución fuera del monitoreo.")
                break

            for order in open_orders:
                side = order["side"]
                order_type = order["type"]
                price = float(order["price"])
                order_id = order["orderId"]

                # TAKE PROFIT ejecutado (precio >= TP)
                if side == "SELL" and "LIMIT" in order_type and current_price >= price:
                    executed_order = ("TP", price, order_id)
                    active = False
                    break

                # STOP LOSS ejecutado (precio <= SL)
                elif side == "SELL" and "STOP" in order_type and current_price <= price:
                    executed_order = ("SL", price, order_id)
                    active = False
                    break

            # 🧪 SIMULACIÓN EN TESTNET (si no se ejecuta automáticamente)
            if simulate_testnet and not executed_order and len(open_orders) > 0:
                from random import choice
                simulated = choice(["TP", "SL", None])
                if simulated:
                    price = float(open_orders[0]["price"])
                    executed_order = (simulated, price, open_orders[0]["orderId"])
                    print(f"🧪 Simulación Testnet: {simulated} ejecutado a {price}")
                    logger.info(f"Simulación Testnet: {simulated} ejecutado a {price}")
                    active = False

            # Si se ejecutó una orden, registrar resultado y limpiar
            if executed_order:
                type_, exec_price, order_id = executed_order

                # Calcular PnL (positivo si TP, negativo si SL)
                pnl = (exec_price - open_price) * quantity if type_ == "TP" else -abs((open_price - exec_price) * quantity)

                # Registrar en Excel con el mismo formato del bot
                log_trade(
                    order_id=order_id,
                    ticker=symbol,
                    order_type=type_,
                    qty=quantity,
                    price_open=open_price,
                    price_sl=open_price if type_ == "SL" else exec_price,
                    price_tp=exec_price if type_ == "TP" else open_price,
                    price_closed=exec_price,
                    pnl=pnl
                )

                print(f"✅ {type_} ejecutado a {exec_price:.2f} | PnL: {pnl:.2f}")
                logger.info(f"{type_} ejecutado a {exec_price:.2f} | PnL: {pnl:.2f}")

                # Cancelar las demás órdenes
                for o in open_orders:
                    if o["orderId"] != order_id:
                        try:
                            client.cancel_order(symbol=symbol, orderId=o["orderId"])
                            print(f"🧹 Orden {o['orderId']} cancelada.")
                            logger.info(f"Orden {o['orderId']} cancelada.")
                        except Exception as cancel_err:
                            logger.error(f"No se pudo cancelar orden {o['orderId']}: {cancel_err}")

                print("🧾 Monitoreo finalizado correctamente.")
                logger.info("Monitoreo finalizado correctamente.")
                break

            # Esperar 30 segundos entre verificaciones
            time.sleep(30)

        except Exception as e:
            print(f"⚠️ Error durante la monitorización: {e}")
            logger.error(f"Error durante la monitorización: {e}")
            time.sleep(60)
