# =============================================================================
# MÓDULO: position_manager.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Gestiona las operaciones activas del bot y evita abrir más de dos operaciones
# simultáneas en el mismo símbolo.
#
# Estructura:
#   open_trades = {
#       "BTCEUR": ["SIMULATED_LONG_1234", "SIMULATED_SHORT_5678"]
#   }
#
# Las funciones permiten registrar, eliminar y listar operaciones.
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from utils.logger_setup import logger

open_trades = {}  # Diccionario global de operaciones activas
MAX_OPEN_TRADES_PER_SYMBOL = 2  # Límite máximo por símbolo


def can_open_new_trade(symbol: str) -> bool:
    """Verifica si se puede abrir una nueva operación en el símbolo dado."""
    current_trades = open_trades.get(symbol, [])
    if len(current_trades) >= MAX_OPEN_TRADES_PER_SYMBOL:
        logger.info(f"⛔ Máximo de {MAX_OPEN_TRADES_PER_SYMBOL} operaciones activas en {symbol}.")
        return False
    return True


def register_new_trade(symbol: str, order_id: str):
    """Registra una nueva operación abierta."""
    if symbol not in open_trades:
        open_trades[symbol] = []

    if order_id not in open_trades[symbol]:
        open_trades[symbol].append(order_id)
        logger.info(f"🆕 Operación registrada: {symbol} ({order_id})")
        print(f"🆕 Operación registrada: {symbol} ({order_id})")
    else:
        logger.warning(f"⚠️ Orden duplicada detectada: {order_id} en {symbol}")


def remove_closed_trade(symbol: str, order_id: str):
    """Elimina una operación cuando se cierra (por TP o SL)."""
    try:
        if symbol in open_trades and order_id in open_trades[symbol]:
            open_trades[symbol].remove(order_id)
            logger.info(f"✅ Operación cerrada eliminada: {symbol} ({order_id})")
            print(f"✅ Operación cerrada eliminada: {symbol} ({order_id})")

            if not open_trades[symbol]:
                del open_trades[symbol]
        else:
            logger.warning(f"⚠️ No se encontró la orden {order_id} en {symbol}.")
    except Exception as e:
        logger.error(f"❌ Error al eliminar operación {order_id}: {e}")
        print(f"❌ Error al eliminar operación {order_id}: {e}")


def list_open_trades():
    """Muestra todas las operaciones abiertas actualmente."""
    if not open_trades:
        print("📭 No hay operaciones abiertas.")
        logger.info("📭 No hay operaciones abiertas.")
        return

    print("📊 Operaciones abiertas:")
    for symbol, orders in open_trades.items():
        print(f" - {symbol}: {orders}")
    logger.info(f"Operaciones abiertas: {open_trades}")
