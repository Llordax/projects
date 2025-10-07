"""
Módulo de conexión con Binance (Testnet o Producción).

Este módulo proporciona la función `get_client()` que inicializa y devuelve
una instancia autenticada del cliente de Binance. Permite conectarse tanto
a la red de pruebas (Testnet) como a la red real (Producción), según la
configuración del parámetro `USE_TESTNET`.

Las credenciales se cargan de forma segura desde un archivo `.env` mediante
la librería `python-dotenv`, evitando exponer las claves API directamente
en el código fuente.
"""

from binance.client import Client
import os
from dotenv import load_dotenv
from utils.logger_setup import logger

# Carga de variables de entorno desde el archivo .env
load_dotenv()

# ⚙️ Cambia esto a False si quieres operar en producción real
USE_TESTNET = True

def get_client():
    """Inicializa y devuelve un cliente de Binance autenticado.

    Esta función obtiene las claves API (`BINANCE_API_KEY` y `BINANCE_API_SECRET`)
    desde el archivo `.env`, crea una instancia del cliente de Binance y
    configura automáticamente el entorno de conexión (Testnet o Producción).

    Returns:
        Client: Instancia autenticada del cliente de Binance lista para operar.

    Raises:
        EnvironmentError: Si no se encuentran las variables de entorno requeridas.
        Exception: Si ocurre un error al inicializar el cliente.
    """
    try:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.critical("❌ Claves API no encontradas en el archivo .env.")
            raise EnvironmentError("Las claves BINANCE_API_KEY o BINANCE_API_SECRET no están definidas.")

        client = Client(api_key=api_key, api_secret=api_secret)
        logger.info("🔐 Cliente Binance inicializado correctamente.")

        # Configurar entorno
        if USE_TESTNET:
            client.API_URL = "https://testnet.binance.vision/api"
            print("🧪 Conectado a Binance Spot TESTNET")
            logger.info("Conectado a Binance Spot TESTNET.")
        else:
            print("⚠️ Conectado a Binance REAL (producción)")
            logger.warning("Conectado a Binance REAL (producción).")

        return client

    except EnvironmentError as e:
        print(f"❌ Error de configuración: {e}")
        logger.critical(f"Error de configuración: {e}")
        raise

    except Exception as e:
        print(f"❌ Error al inicializar el cliente Binance: {e}")
        logger.error(f"Error al inicializar el cliente Binance: {e}")
        raise
