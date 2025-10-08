# =============================================================================
# MÓDULO: runner.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo se encarga de manejar la **ejecución robusta** del bot de trading,
# implementando un mecanismo de **reintentos automáticos** en caso de fallos.
#
# Su función principal permite ejecutar cualquier proceso (por ejemplo, la
# función principal del bot) de manera continua, capturando errores transitorios
# y reintentando su ejecución tras un periodo de espera.
#
# Esto evita que el bot se detenga por errores puntuales de red, API o tiempo
# de respuesta, asegurando una **operación estable y autónoma**.
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES PRINCIPALES:
#   ✅ Ejecutar funciones en bucle con recuperación ante errores.
#   ✅ Registrar excepciones en logs y consola.
#   ✅ Implementar pausas configurables entre reintentos.
#   ✅ Mantener el bot en funcionamiento continuo sin intervención manual.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - time (para gestionar los intervalos de espera)
#   - utils.logger_setup.logger (para registrar errores e información)
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import time
from utils.logger_setup import logger


# =============================================================================
# 🔁 FUNCIÓN: Ejecución continua con reintentos automáticos
# =============================================================================
def run_with_retry(func, interval=60):
    """
    Ejecuta una función con un mecanismo de reintentos automáticos en caso de error.

    Si la función falla, el error se captura, se registra en logs y se espera
    un intervalo antes de volver a intentar la ejecución. Este ciclo continúa
    indefinidamente, permitiendo que el bot se recupere de errores transitorios
    (por ejemplo, pérdida de conexión con Binance, timeouts o errores HTTP).

    Args:
        func (Callable): Función a ejecutar. No debe requerir argumentos.
        interval (int, optional): Tiempo de espera (en segundos) entre cada intento
            o ejecución continua. Por defecto es 60 segundos.

    Ejemplo:
        >>> def main_bot():
        ...     ejecutar_trading()
        ...
        >>> run_with_retry(main_bot, interval=30)

    Notas:
        - Este diseño garantiza que el bot siga funcionando de manera continua.
        - En caso de errores persistentes, estos se registran sin detener la ejecución.
        - Se recomienda usar intervalos moderados para evitar sobrecarga de API.
    """
    while True:
        try:
            # 🟢 Intentar ejecutar la función principal del bot
            func()
        except Exception as e:
            # ❌ Si ocurre un error, registrar y continuar después del intervalo
            print(f"❌ Error en ejecución del bot: {e}")
            logger.error(f"Error en ejecución del bot: {e}")

        # ⏳ Espera entre ejecuciones o reintentos
        print("⏳ Esperando siguiente chequeo...\n")
        logger.info("Esperando siguiente ejecución...")

        time.sleep(interval)
