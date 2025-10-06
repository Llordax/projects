import logging
import os

# Crear carpeta "logs" si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Crear el logger principal
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)

# Formatter común
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 🔹 Handler para ejecución normal
exec_handler = logging.FileHandler(f"{LOG_DIR}/execution.log")
exec_handler.setLevel(logging.INFO)
exec_handler.setFormatter(formatter)

# 🔸 Handler para errores
error_handler = logging.FileHandler(f"{LOG_DIR}/errors.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# 🔁 Evitar duplicados
if not logger.handlers:
    logger.addHandler(exec_handler)
    logger.addHandler(error_handler)
