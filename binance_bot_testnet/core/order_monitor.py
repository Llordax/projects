# =============================================================================
# MÓDULO: order_monitor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo se encarga de **supervisar en tiempo real las órdenes abiertas** 
# (Take Profit y Stop Loss) creadas por el bot en Binance.
#
# Su objetivo es detectar cuándo una orden se ejecuta (TP o SL), registrar
# automáticamente el resultado en los logs y en el archivo Excel de historial,
# y cancelar de forma segura las órdenes restantes.
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES PRINCIPALES:
#   ✅ Verifica continuamente el estado de las órdenes abiertas en Binance.
#   ✅ Detecta la ejecución real de TP o SL según el precio de mercado.
#   ✅ Calcula y normaliza el PnL (positivo en TP, negativo en SL).
#   ✅ Cancela automáticamente las órdenes no ejecutadas tras un cierre.
#   ✅ Compatible con modo Testnet (simulación de ejecuciones).
#
# -----------------------------------------------------------------------------
# ⚙️ MODO DE USO:
#   Se llama desde `execute_trade()` (en order_executor.py) después de colocar
#   los niveles de TP/SL. Permanece en bucle hasta detectar una ejecución.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import time
from utils.logger import log_trade
from utils.logger_setup import logger


# =============================================================================
# 👁️ FUNCIÓN PRINCIPAL: Monitorización de órdenes abiertas
# =============================================================================
def monitor_orders(client, symbol, open_price, quantity, simulate_testnet=True):
    """
    Supervisa las órdenes abiertas de un activo (TP/SL) y detecta cuándo se ejecutan.

    El ciclo de monitoreo consulta periódicamente el precio actual y el estado
    de las órdenes abiertas. Si una se ejecuta, registra el resultado y cancela
    las órdenes restantes. Si el modo Testnet está activado, se puede simular
    la ejecución de una orden para pruebas.

    Args:
        client (Client): Cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR" o "BTCUSDC").
        open_price (float): Precio de entrada de la operación.
        quantity (float): Cantidad comprada.
        simulate_testnet (bool): Si True, activa modo de simulación en testnet
            (emula ejecución de órdenes cuando no hay actividad real).
    """
    print(f"👁️  Monitoreando {symbol}... Esperando ejecución de TP o SL")
    logger.info(f"Monitoreando {symbol}... Esperando ejecución de TP o SL")

    active = True
    executed_order = None  # Almacena información de la orden ejecutada

    while active:
        try:
            # Obtener precio actual del mercado
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker["price"])

            # Recuperar las órdenes abiertas (normalmente TP y SL)
            open_orders = client.get_open_orders(symbol=symbol)

            # Si no hay órdenes abiertas (y no estamos en modo testnet), se detiene
            if not open_orders and not simulate_testnet:
                print("⚠️ No se encontraron órdenes abiertas, posible ejecución fuera del monitoreo.")
                logger.warning("No se encontraron órdenes abiertas, posible ejecución fuera del monitoreo.")
                break

            # ---------------------------------------------------------------------
            # 🔍 Revisión de las órdenes abiertas en busca de ejecución TP o SL
            # ---------------------------------------------------------------------
            for order in open_orders:
                side = order["side"]
                order_type = order["type"]
                price = float(order["price"])
                order_id = order["orderId"]

                # 🎯 TAKE PROFIT ejecutado (el precio actual >= precio del TP)
                if side == "SELL" and "LIMIT" in order_type and current_price >= price:
                    executed_order = ("TP", price, order_id)
                    active = False
                    break

                # 🛑 STOP LOSS ejecutado (el precio actual <= precio del SL)
                elif side == "SELL" and "STOP" in order_type and current_price <= price:
                    executed_order = ("SL", price, order_id)
                    active = False
                    break

            # ---------------------------------------------------------------------
            # 🧪 SIMULACIÓN EN TESTNET
            # ---------------------------------------------------------------------
            # Si no se ejecuta ninguna orden y estamos en testnet, se simula aleatoriamente
            if simulate_testnet and not executed_order and len(open_orders) > 0:
                from random import choice
                simulated = choice(["TP", "SL", None])
                if simulated:
                    price = float(open_orders[0]["price"])
                    executed_order = (simulated, price, open_orders[0]["orderId"])
                    print(f"🧪 Simulación Testnet: {simulated} ejecutado a {price}")
                    logger.info(f"Simulación Testnet: {simulated} ejecutado a {price}")
                    active = False

            # ---------------------------------------------------------------------
            # ✅ ORDEN EJECUTADA → Registro y limpieza de órdenes restantes
            # ---------------------------------------------------------------------
            if executed_order:
                type_, exec_price, order_id = executed_order

                # Calcular PnL (positivo si TP, negativo si SL)
                pnl = (exec_price - open_price) * quantity if type_ == "TP" else -abs((open_price - exec_price) * quantity)

                # Registrar en Excel y logs la ejecución
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

                # Cancelar las demás órdenes abiertas que no se ejecutaron
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

            # ---------------------------------------------------------------------
            # ⏱️ Espera entre comprobaciones (30 segundos)
            # ---------------------------------------------------------------------
            time.sleep(30)

        except Exception as e:
            # Manejo de errores durante la ejecución del bucle
            print(f"⚠️ Error durante la monitorización: {e}")
            logger.error(f"Error durante la monitorización: {e}")
            # En caso de error, se espera más tiempo antes del siguiente intento
            time.sleep(60)
