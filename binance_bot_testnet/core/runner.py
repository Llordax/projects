"""
Módulo encargado de manejar la ejecución robusta del bot con reintentos automáticos.

Proporciona una función que ejecuta otra función y, en caso de que ocurra un error,
espera un tiempo antes de volver a intentarlo. Esto permite que el bot se recupere
de errores transitorios sin necesidad de reiniciarlo manualmente.
"""

import time
from utils.logger_setup import logger

def run_with_retry(func, interval=60):
    """Ejecuta una función con un mecanismo de reintentos ante errores.

    Si la función falla, se registrará el error y se esperará un tiempo antes
    de volver a intentar. Este proceso se repetirá hasta alcanzar el número
    máximo de reintentos permitidos.

    Args:
        func (Callable): Función a ejecutar. No debe recibir argumentos.
        max_retries (int, optional): Número máximo de intentos antes de abortar.
            Por defecto es 5.
        delay_seconds (int, optional): Tiempo de espera (en segundos) entre intentos.
            Por defecto es 10.

    Raises:
        Exception: Si se alcanzan todos los intentos sin éxito, el error final
        será lanzado para que el programa superior lo maneje.

    Ejemplo:
        >>> run_with_retry(main, max_retries=3, delay_seconds=5)
    """
    while True:
        try:
            func()
        except Exception as e:
            print(f"❌ Error en ejecución del bot: {e}")
            logger.error(f"Error en ejecución del bot: {e}")
        print("⏳ Esperando siguiente chequeo...\n")
        logger.info("Esperando siguiente ejecución...")
        time.sleep(interval)
