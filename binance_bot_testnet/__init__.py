"""
Binance Bot Testnet
===================

Bot de trading automatizado para el entorno de pruebas (Testnet) de Binance.

Este paquete incluye todos los componentes necesarios para ejecutar una estrategia
de trading algorítmica, incluyendo conexión con la API de Binance, obtención de datos
de precios, cálculos de indicadores técnicos, ejecución de órdenes, gestión de riesgos
y registro detallado de operaciones.

Estructura principal:
    - config: Parámetros y ajustes generales del bot.
    - core: Lógica de negocio, estrategias e indicadores.
    - data: Obtención y preparación de datos desde Binance.
    - services: Conexión y autenticación con Binance API.
    - utils: Herramientas auxiliares (logging, almacenamiento de logs, etc.).

Uso:
    >>> from binance_bot_testnet.main import main
    >>> main()
"""
