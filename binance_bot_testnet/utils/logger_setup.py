"""
Módulo de configuración global del sistema de logging.

Define un logger centralizado para el bot de trading que:
    - Muestra la información en consola.
    - Guarda los registros en dos archivos separados:
        * `execution.log`: registros informativos y operativos.
        * `errors.log`: errores y excepciones críticas.
    - Permite diferentes niveles de severidad (INFO, WARNING, ERROR, CRITICAL).

Este módulo debe importarse en cualquier otro archivo que requiera registrar
eventos o errores mediante:

    from utils.logger_setup import logger
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# 📂 Directorio donde se guardarán los logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 🧠 Crear el logger principal del bot
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)

# 🎨 Formato de los mensajes
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 🔹 Handler para ejecución normal (informativo)
exec_handler = logging.FileHandler(f"{LOG_DIR}/execution.log")
exec_handler.setLevel(logging.INFO)
exec_handler.setFormatter(formatter)

# 🔸 Handler para errores
error_handler = logging.FileHandler(f"{LOG_DIR}/errors.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# 🔁 Evitar duplicados al reimportar el módulo
if not logger.handlers:
    logger.addHandler(exec_handler)
    logger.addHandler(error_handler)

# ✅ Confirmación de inicialización
logger.info("Logger inicializado correctamente. Archivos de log creados en carpeta /logs")
