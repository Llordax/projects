# =============================================================================
# MÓDULO: order_monitor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Supervisa las operaciones abiertas (LONG o SHORT) y ejecuta su cierre cuando
# el precio alcanza el TP o SL.
#
# 💡 Cada operación tiene un ID único (order_id). Si otro hilo ya la cerró,
# este hilo termina automáticamente → evita duplicaciones.
#
# ✅ Seguro en hilos (thread-safe).
# ✅ Compatible con Testnet y Producción.
# ✅ Cierra correctamente una sola vez por operación.
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
    """
    print(f"👁️ Monitoreo iniciado → {symbol} ({trade_type}) [{order_id}]")
    logger.info(f"Iniciado monitoreo de {symbol} ({trade_type}) con ID={order_id}")

    while True:
        try:
            # 🧩 Si la operación ya fue cerrada, salir
            if symbol not in open_trades or order_id not in open_trades[symbol]:
                print(f"🧩 [{symbol}] Monitoreo terminado (orden {order_id} ya cerrada).")
                break

            current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
            exec_type, exec_price = None, None

            if trade_type == "LONG":
                if current_price >= tp_price:
                    exec_type, exec_price = "TP", current_price
                elif current_price <= sl_price:
                    exec_type, exec_price = "SL", current_price
            else:
                if current_price <= tp_price:
                    exec_type, exec_price = "TP", current_price
                elif current_price >= sl_price:
                    exec_type, exec_price = "SL", current_price

            if not exec_type:
                time.sleep(10)
                continue

            # 💰 Calcular beneficio o pérdida
            pnl = (open_price - exec_price) * quantity if trade_type == "SHORT" else (exec_price - open_price) * quantity
            pnl = abs(pnl) if exec_type == "TP" else -abs(pnl)

            # Solo cerrar si sigue activo
            if symbol in open_trades and order_id in open_trades[symbol]:
                log_trade(order_id, symbol, f"{exec_type}_{trade_type}", quantity,
                          open_price, sl_price, tp_price, exec_price, pnl)
                print(f"✅ [{symbol}] {exec_type} ({trade_type}) ejecutado a {exec_price:.2f} | PnL={pnl:.4f}")
                client.cancel_open_orders(symbol=symbol)
                remove_closed_trade(symbol, order_id)
                logger.info(f"🧹 {symbol} ({order_id}) cerrado correctamente ({exec_type})")
                break
            else:
                print(f"⏹️ [{symbol}] Orden {order_id} ya cerrada por otro hilo.")
                break

        except Exception as e:
            logger.error(f"Error monitoreando {symbol} ({order_id}): {e}")
            time.sleep(10)
