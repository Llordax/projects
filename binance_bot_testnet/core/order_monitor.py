# =============================================================================
# MÓDULO: order_monitor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Supervisa las operaciones abiertas (LONG o SHORT) y ejecuta su cierre cuando
# el precio alcanza el Take Profit (TP) o Stop Loss (SL).
#
# 💡 Cada operación tiene un ID único (order_id). Si otro hilo ya la cerró,
# este hilo termina automáticamente → evita duplicaciones.
#
# ✅ Seguro en hilos (thread-safe).
# ✅ Compatible con Binance Testnet y Producción.
# ✅ Cierra correctamente una sola vez por operación.
#
# ⚠️ NOTA IMPORTANTE:
# En versiones recientes del paquete `python-binance`, el método correcto para
# cancelar todas las órdenes abiertas es `cancel_all_open_orders()`.
# La llamada anterior (`cancel_open_orders()`) ha sido eliminada, y por eso
# aparecía el error:
#     'Client' object has no attribute 'cancel_open_orders'
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import time
from utils.logger import log_trade
from utils.logger_setup import logger
from services.binance_client import USE_TESTNET
from core.position_manager import remove_closed_trade, open_trades


# =============================================================================
# 👁️ FUNCIÓN: Monitorear TP/SL (seguro con ID)
# =============================================================================
def monitor_orders(client, symbol: str, open_price: float, quantity: float,
                   tp_price: float, sl_price: float, trade_type: str, order_id: str):
    """
    Monitorea el precio del activo y ejecuta el cierre de una operación
    específica (identificada por order_id).

    Cuando el precio alcanza el nivel de Take Profit (TP) o Stop Loss (SL),
    se registra la operación, se cancelan las órdenes abiertas restantes y
    se elimina del registro de operaciones activas.

    Args:
        client (Client): Instancia del cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        open_price (float): Precio de entrada de la operación.
        quantity (float): Cantidad operada.
        tp_price (float): Precio objetivo de Take Profit.
        sl_price (float): Precio de Stop Loss.
        trade_type (str): Tipo de operación ("LONG" o "SHORT").
        order_id (str): Identificador único de la operación.
    """
    print(f"👁️ Monitoreo iniciado → {symbol} ({trade_type}) [{order_id}]")
    logger.info(f"Iniciado monitoreo de {symbol} ({trade_type}) con ID={order_id}")

    # Bucle de monitoreo continuo (10s entre chequeos)
    while True:
        try:
            # 🧩 Si la operación ya fue cerrada por otro hilo, terminar
            if symbol not in open_trades or order_id not in open_trades[symbol]:
                print(f"🧩 [{symbol}] Monitoreo terminado (orden {order_id} ya cerrada).")
                break

            # 🔄 Obtener el precio actual
            current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
            exec_type, exec_price = None, None

            # 📊 Evaluar si se alcanzó TP o SL
            if trade_type == "LONG":
                if current_price >= tp_price:
                    exec_type, exec_price = "TP", current_price
                elif current_price <= sl_price:
                    exec_type, exec_price = "SL", current_price
            else:  # SHORT simulado
                if current_price <= tp_price:
                    exec_type, exec_price = "TP", current_price
                elif current_price >= sl_price:
                    exec_type, exec_price = "SL", current_price

            # Si no se alcanzó ningún nivel, esperar y continuar monitoreando
            if not exec_type:
                time.sleep(10)
                continue

            # 💰 Calcular beneficio o pérdida (PnL)
            pnl = (open_price - exec_price) * quantity if trade_type == "SHORT" else (exec_price - open_price) * quantity
            pnl = abs(pnl) if exec_type == "TP" else -abs(pnl)

            # Cerrar operación si sigue activa
            if symbol in open_trades and order_id in open_trades[symbol]:
                # Registrar resultado en el Excel de histórico
                log_trade(
                    order_id, symbol, f"{exec_type}_{trade_type}", quantity,
                    open_price, sl_price, tp_price, exec_price, pnl
                )

                print(f"✅ [{symbol}] {exec_type} ({trade_type}) ejecutado a {exec_price:.2f} | PnL={pnl:.4f}")

                # 🧹 Cancelar órdenes abiertas restantes (TP/SL pendientes)
                try:
                    client.cancel_all_open_orders(symbol=symbol)
                except Exception as cancel_err:
                    logger.warning(f"No se pudieron cancelar órdenes abiertas en {symbol}: {cancel_err}")
                    print(f"⚠️ No se pudieron cancelar órdenes abiertas en {symbol}: {cancel_err}")

                # Eliminar de la lista de operaciones activas
                remove_closed_trade(symbol, order_id)
                logger.info(f"🧹 {symbol} ({order_id}) cerrado correctamente ({exec_type})")
                break
            else:
                # Si otro hilo ya cerró esta orden, terminar sin duplicar
                print(f"⏹️ [{symbol}] Orden {order_id} ya cerrada por otro hilo.")
                break

        except Exception as e:
            # Registrar cualquier error de conexión o lógica, y reintentar
            logger.error(f"Error monitoreando {symbol} ({order_id}): {e}")
            print(f"❌ Error monitoreando {symbol} ({order_id}): {e}")
            time.sleep(10)
