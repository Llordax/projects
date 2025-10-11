# =============================================================================
# MÓDULO: order_monitor.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo se encarga de **monitorear las operaciones abiertas (TP/SL)** y 
# ejecutar el cierre correspondiente cuando el precio alcanza los niveles 
# definidos de Take Profit (TP) o Stop Loss (SL).
#
# En **entorno de producción (USE_TESTNET = False)**, el bot confía en que 
# Binance ejecute automáticamente las órdenes LIMIT y STOP_LOSS_LIMIT cuando 
# el precio alcance los niveles establecidos.
#
# En **entorno de testnet (USE_TESTNET = True)**, Binance NO ejecuta 
# automáticamente las órdenes TP/SL, por lo que este módulo incluye una 
# **lógica de simulación** que detecta el cruce de precios y fuerza el cierre 
# virtual, registrando el resultado en el historial de operaciones.
#
# -----------------------------------------------------------------------------
# ⚙️ FUNCIONALIDADES PRINCIPALES:
#   ✅ Monitorear continuamente el precio actual del símbolo.
#   ✅ Detectar si el precio alcanza o supera el TP/SL configurado.
#   ✅ Ejecutar venta simulada (solo en Testnet).
#   ✅ Registrar en Excel el resultado de la operación (PnL).
#   ✅ En producción, esperar el estado "FILLED" de las órdenes reales.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - binance.client.Client → para consultar precios y órdenes abiertas.
#   - config.settings.USE_TESTNET → para diferenciar entorno real/simulado.
#   - utils.logger → para registrar operaciones cerradas.
#   - utils.logger_setup.logger → para logs en archivos y consola.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import time
from utils.logger import log_trade
from utils.logger_setup import logger
from config.settings import SYMBOL
from services.binance_client import USE_TESTNET


# =============================================================================
# 👁️ FUNCIÓN PRINCIPAL: Monitorear y ejecutar TP/SL
# =============================================================================
def monitor_orders(client, symbol: str, open_price: float, quantity: float):
    """
    Supervisa las órdenes TP/SL asociadas a una operación abierta.

    Si el entorno es Testnet, las órdenes se simulan (ya que Binance no las ejecuta 
    automáticamente). Si es entorno real, se espera la ejecución real (FILLED) 
    por parte del motor de Binance.

    Args:
        client (Client): Instancia del cliente Binance autenticado.
        symbol (str): Par de trading (por ejemplo, "BTCEUR").
        open_price (float): Precio de entrada de la operación.
        quantity (float): Cantidad total comprada.
    """

    print(f"👁️ Monitoreando {symbol}... esperando ejecución real o simulada de TP/SL.")
    logger.info(f"Monitoreando {symbol}... esperando ejecución real o simulada de TP/SL.")

    # -------------------------------------------------------------------------
    # 🔎 Obtener órdenes TP y SL activas
    # -------------------------------------------------------------------------
    try:
        orders = client.get_open_orders(symbol=symbol)
        tp_price, sl_price = None, None

        for o in orders:
            if o["type"] == "LIMIT":
                tp_price = float(o["price"])
            elif "STOP" in o["type"]:
                sl_price = float(o["stopPrice"])

        if not tp_price or not sl_price:
            print("⚠️ No se detectaron órdenes TP/SL válidas.")
            logger.warning("No se detectaron órdenes TP/SL válidas.")
            return

        print(f"🎯 TP: {tp_price:.2f} | 🛑 SL: {sl_price:.2f}")

    except Exception as e:
        logger.error(f"Error al obtener órdenes: {e}")
        print(f"❌ Error al obtener órdenes abiertas: {e}")
        return

    # -------------------------------------------------------------------------
    # 🔁 MODO TESTNET → Ejecución simulada
    # -------------------------------------------------------------------------
    if USE_TESTNET:
        print("🧪 Modo TESTNET activo → ejecución de TP/SL simulada.")
        while True:
            try:
                current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
                print(f"💹 Precio actual {symbol}: {current_price:.2f}")
                logger.info(f"Precio actual {symbol}: {current_price:.2f}")

                # =============================================================
                # 🎯 Detección robusta de TP/SL alcanzado o superado
                # =============================================================
                if current_price >= tp_price:
                    exec_type = "TP"
                    exec_price = current_price  # Usa precio actual
                elif current_price <= sl_price:
                    exec_type = "SL"
                    exec_price = current_price
                else:
                    time.sleep(5)
                    continue

                # =============================================================
                # 💰 Calcular PnL (Beneficio o Pérdida)
                # =============================================================
                pnl = (exec_price - open_price) * quantity
                pnl = abs(pnl) if exec_type == "TP" else -abs(pnl)

                # =============================================================
                # 🧾 Registrar la ejecución en Excel
                # =============================================================
                log_trade(
                    order_id="SIMULATED",
                    ticker=symbol,
                    order_type=exec_type,
                    qty=quantity,
                    price_open=open_price,
                    price_sl=sl_price,
                    price_tp=tp_price,
                    price_closed=exec_price,
                    pnl=pnl
                )

                print(f"✅ {exec_type} ejecutado a {exec_price:.2f} (simulado) | PnL: {pnl:.4f}")
                logger.info(f"{exec_type} ejecutado a {exec_price:.2f} (simulado) | PnL: {pnl:.4f}")
                print("🧾 Monitoreo finalizado correctamente (ejecución simulada detectada).")
                logger.info("Monitoreo finalizado correctamente (ejecución simulada detectada).")

                break  # 🛑 salir del bucle tras registrar la ejecución

            except Exception as e:
                logger.error(f"Error en monitorización (simulada): {e}")
                print(f"⚠️ Error en monitoreo simulado: {e}")
                time.sleep(10)

    # -------------------------------------------------------------------------
    # ⚙️ MODO PRODUCCIÓN → Espera de ejecución real en Binance
    # -------------------------------------------------------------------------
    else:
        print("⚙️ Modo PRODUCCIÓN activo → esperando ejecución real en Binance.")
        while True:
            try:
                # Revisar órdenes abiertas periódicamente
                open_orders = client.get_open_orders(symbol=symbol)

                # Si ya no hay órdenes abiertas → TP o SL ejecutado
                if not open_orders:
                    print("✅ Orden ejecutada en Binance (TP o SL alcanzado).")
                    logger.info("Orden ejecutada en Binance (TP o SL alcanzado).")

                    # Obtener el precio de cierre real (último precio)
                    closed_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
                    pnl = (closed_price - open_price) * quantity
                    pnl = abs(pnl) if closed_price > open_price else -abs(pnl)
                    exec_type = "TP" if pnl > 0 else "SL"

                    # Registrar trade cerrado real
                    log_trade(
                        order_id="REAL",
                        ticker=symbol,
                        order_type=exec_type,
                        qty=quantity,
                        price_open=open_price,
                        price_sl=sl_price,
                        price_tp=tp_price,
                        price_closed=closed_price,
                        pnl=pnl
                    )

                    print(f"✅ {exec_type} ejecutado a {closed_price:.2f} (real) | PnL: {pnl:.4f}")
                    logger.info(f"{exec_type} ejecutado a {closed_price:.2f} (real) | PnL: {pnl:.4f}")
                    break

                time.sleep(5)

            except Exception as e:
                logger.error(f"Error en monitorización (real): {e}")
                print(f"⚠️ Error en monitoreo real: {e}")
                time.sleep(10)
