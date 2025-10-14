# =============================================================================
# MÓDULO: binance_client.py
# =============================================================================
# 📌 DESCRIPCIÓN GENERAL
# -----------------------------------------------------------------------------
# Este módulo gestiona la **conexión y autenticación con Binance**, tanto para
# el entorno de **pruebas (Testnet)** como para el entorno **real (Producción)**.
#
# La función principal `get_client()` inicializa y devuelve una instancia del
# cliente autenticado de Binance utilizando las claves API almacenadas de forma
# segura en el archivo `.env`.
#
# Este enfoque garantiza la **seguridad de las credenciales** y permite
# cambiar fácilmente entre entornos mediante la variable `USE_TESTNET`.
#
# -----------------------------------------------------------------------------
# 🧠 FUNCIONALIDADES PRINCIPALES:
#   ✅ Carga de credenciales API desde archivo `.env` (seguridad).
#   ✅ Inicialización automática del cliente Binance.
#   ✅ Selección de entorno (Testnet o Producción).
#   ✅ Registro detallado de eventos y errores.
#
# -----------------------------------------------------------------------------
# ⚠️ NOTAS DE SEGURIDAD:
#   - Nunca compartas el archivo `.env` con tus claves API reales.
#   - El entorno Testnet permite simular operaciones sin riesgo.
#   - Cambiar `USE_TESTNET = False` para operar en producción.
#
# -----------------------------------------------------------------------------
# 🧩 DEPENDENCIAS:
#   - binance.client.Client
#   - dotenv (para carga de variables de entorno)
#   - utils.logger_setup.logger (para registro de eventos)
#
# -----------------------------------------------------------------------------
# 👤 Autor: Alejandro Llordén Rodríguez
# 🗓️ Fecha: Octubre 2025
# =============================================================================

from binance.client import Client
import os
from dotenv import load_dotenv
from utils.logger_setup import logger


# =============================================================================
# 🔐 Carga de variables de entorno desde el archivo .env
# =============================================================================
load_dotenv()  # Lee las claves API almacenadas localmente en el archivo .env


# =============================================================================
# ⚙️ Configuración del entorno
# =============================================================================
# Si es True → conecta al entorno de pruebas (Testnet)
# Si es False → conecta a la red real (Producción)
USE_TESTNET = True


# =============================================================================
# 🚀 FUNCIÓN PRINCIPAL: Inicialización del cliente Binance
# =============================================================================
def get_client() -> Client:
    """
    Inicializa y devuelve un cliente autenticado de Binance.

    La función obtiene las claves API (`BINANCE_API_KEY` y `BINANCE_API_SECRET`)
    desde el archivo `.env`, crea una instancia del cliente de Binance y configura
    automáticamente el entorno (Testnet o Producción) según la variable global
    `USE_TESTNET`.

    Returns:
        Client: Instancia autenticada del cliente de Binance lista para realizar
        operaciones (consultas, órdenes, etc.).

    Raises:
        EnvironmentError: Si no se encuentran las variables de entorno requeridas.
        Exception: Si ocurre un error durante la inicialización del cliente.

    Ejemplo:
        >>> client = get_client()
        >>> info = client.get_account()
        >>> print(info)
    """
    try:
        # 🔑 Cargar credenciales de las variables de entorno
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        # Validar que las claves estén presentes
        if not api_key or not api_secret:
            logger.critical("❌ Claves API no encontradas en el archivo .env.")
            raise EnvironmentError("Las claves BINANCE_API_KEY o BINANCE_API_SECRET no están definidas.")

        # 🧩 Crear la instancia del cliente Binance
        client = Client(api_key=api_key, api_secret=api_secret)
        logger.info("🔐 Cliente Binance inicializado correctamente.")

        # 🌐 Configurar entorno de conexión
        if USE_TESTNET:
            client.API_URL = "https://testnet.binance.vision/api"
            print("\n🧪 Conectado a Binance Spot TESTNET ✅")
            logger.info("Conectado a Binance Spot TESTNET.")
        else:
            print("⚠️ Conectado a Binance REAL (producción)")
            logger.warning("Conectado a Binance REAL (producción).")

        # Devolver cliente listo para su uso
        return client

    except EnvironmentError as e:
        # Error crítico si faltan variables de entorno
        print(f"❌ Error de configuración: {e}")
        logger.critical(f"Error de configuración: {e}")
        raise

    except Exception as e:
        # Manejo genérico de errores de conexión o inicialización
        print(f"❌ Error al inicializar el cliente Binance: {e}")
        logger.error(f"Error al inicializar el cliente Binance: {e}")
        raise
