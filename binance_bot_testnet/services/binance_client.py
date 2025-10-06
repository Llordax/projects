# services/binance_client.py

from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# ⚙️ Cambia esto a False si quieres operar en producción real
USE_TESTNET = True

def get_client():
    client = Client(
        api_key=os.getenv("BINANCE_API_KEY"),
        api_secret=os.getenv("BINANCE_API_SECRET")
    )

    if USE_TESTNET:
        client.API_URL = "https://testnet.binance.vision/api"
        print("🧪 Conectado a Binance Spot TESTNET")
    else:
        print("⚠️ Conectado a Binance REAL (producción)")

    return client
