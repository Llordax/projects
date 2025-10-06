# core/runner.py
import time
from utils.logger_setup import logger

def run_with_retry(func, interval=60):
    while True:
        try:
            func()
        except Exception as e:
            print(f"❌ Error en ejecución del bot: {e}")
            logger.error(f"Error en ejecución del bot: {e}")
        print("⏳ Esperando siguiente chequeo...\n")
        logger.info("Esperando siguiente ejecución...")
        time.sleep(interval)
