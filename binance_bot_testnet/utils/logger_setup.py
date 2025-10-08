# =============================================================================
# MÓDULO: logger_setup.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo configura el **sistema global de logging** para el bot de trading.
#
# Proporciona un `logger` centralizado que:
#   ✅ Muestra la información en consola (si se desea ampliar).
#   ✅ Guarda registros en archivos separados según su tipo:
#       - `execution.log`: Actividades generales, operaciones y eventos informativos.
#       - `errors.log`: Errores y excepciones críticas.
#   ✅ Gestiona automáticamente los niveles de severidad:
#       INFO, WARNING, ERROR, CRITICAL.
#
# Al importarse en cualquier parte del proyecto, permite registrar eventos mediante:
#
#     from utils.logger_setup import logger
#     logger.info("Mensaje informativo")
#     logger.error("Error detectado")
#
# -----------------------------------------------------------------------------
# 🧩 DETALLES TÉCNICOS:
#   - Se crean los archivos de log dentro del directorio `/logs`.
#   - Si los archivos no existen, se generan automáticamente.
#   - Utiliza el formato estándar de tiempo y nivel de log.
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


# =============================================================================
# 📂 CONFIGURACIÓN DEL DIRECTORIO DE LOGS
# =============================================================================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Crea la carpeta si no existe


# =============================================================================
# 🧠 CREACIÓN DEL LOGGER PRINCIPAL
# =============================================================================
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)  # Nivel base: registra INFO, WARNING, ERROR y CRITICAL


# =============================================================================
# 🎨 FORMATO DE MENSAJES
# =============================================================================
# Ejemplo de salida:
# 2025-10-08 10:22:11 - INFO - Orden ejecutada correctamente
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


# =============================================================================
# 🔹 HANDLER DE EJECUCIÓN NORMAL (INFO / OPERACIONES)
# =============================================================================
exec_handler = logging.FileHandler(f"{LOG_DIR}/execution.log")
exec_handler.setLevel(logging.INFO)
exec_handler.setFormatter(formatter)


# =============================================================================
# 🔸 HANDLER DE ERRORES Y EXCEPCIONES
# =============================================================================
error_handler = logging.FileHandler(f"{LOG_DIR}/errors.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)


# =============================================================================
# 🔁 EVITAR DUPLICADOS DE HANDLERS
# =============================================================================
# Esto impide que al reimportar el módulo se dupliquen las líneas de log.
if not logger.handlers:
    logger.addHandler(exec_handler)
    logger.addHandler(error_handler)


# =============================================================================
# ✅ CONFIRMACIÓN DE INICIALIZACIÓN
# =============================================================================
logger.info("Logger inicializado correctamente. Archivos de log creados en carpeta /logs")
