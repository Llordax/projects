# Binance Bot Testnet 🤖

Un bot de trading automatizado para **Binance Testnet**, diseñado con una arquitectura modular y estrategias basadas en indicadores técnicos como **EMA** (Media Móvil Exponencial) y **RSI** (Índice de Fuerza Relativa).  
Permite analizar el mercado, ejecutar operaciones de prueba, gestionar el riesgo y registrar toda la actividad en logs detallados.

---

## 🚀 Características

- ✅ Integración con **Binance Testnet** (API oficial)
- 📊 Estrategia basada en **EMA y RSI**
- 🧩 Arquitectura modular (core, data, services, utils)
- ⚙️ Configuración sencilla mediante `.env` y `settings.py`
- 🧠 Gestión de riesgo con **Take Profit (TP)** y **Stop Loss (SL)**
- 🪵 Registro completo de logs (errores, ejecución)
- 🔁 Sistema de reintento automático en caso de fallos de conexión

---

## 📂 Estructura del proyecto

```
binance_bot_testnet/
├── main.py                     # Punto de entrada principal
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Claves de API y configuración privada
├── config/
│   └── settings.py             # Configuración global de parámetros
├── core/
│   ├── indicators.py           # Cálculo de indicadores técnicos
│   ├── order_executor.py       # Ejecución de órdenes
│   ├── risk_management.py      # Gestión de riesgo TP/SL
│   ├── runner.py               # Bucle principal con reintentos
│   └── strategy.py             # Lógica de estrategia (EMA y RSI)
├── data/
│   └── price_fetcher.py        # Obtención de precios y velas OHLCV
├── services/
│   └── binance_client.py       # Conexión con la API de Binance
├── utils/
│   ├── logger.py               # Funciones de logging
│   └── logger_setup.py         # Configuración del logger
└── logs/
    ├── execution.log           # Registro de operaciones
    └── errors.log              # Registro de errores
```

---

## ⚙️ Requisitos previos

- Python **3.10+**
- Una cuenta de **Binance Testnet**
- Claves API de Testnet ([https://testnet.binance.vision/](https://testnet.binance.vision/))
- Entorno virtual recomendado (`venv` o `conda`)

---

## 🔧 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/binance_bot_testnet.git
cd binance_bot_testnet
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` en la raíz:

```bash
BINANCE_API_KEY=tu_api_key
BINANCE_API_SECRET=tu_api_secret
```

4. Configurar los parámetros de trading en `config/settings.py`:

```python
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
EMA_PERIOD = 50
RSI_PERIOD = 14
TP_PCTS = [0.015, 0.03, 0.045]
SL_PCTS = [0.005, 0.01, 0.015]
```

---

## ▶️ Ejecución

Ejecutar el bot con:

```bash
python main.py
```

Salida esperada:

```
🚀 Bot iniciado
🧪 Conectado a Binance Spot TESTNET
📊 Últimos precios de BTCUSDT:
📈 RSI actual: 47.32
📈 EMA ahora: 27350.12, EMA previa: 27310.84
✅ Condición de entrada cumplida
Ejecutando trade...
```

---

## 🧮 Estrategia de Trading

El bot evalúa condiciones de entrada según:

```python
rsi < 50 and ema_now > ema_prev
```

- **RSI (Relative Strength Index)** indica zonas de sobrecompra/sobreventa.  
- **EMA (Exponential Moving Average)** identifica tendencias.  
- Si el RSI está bajo (indica posible sobreventa) y la EMA sube, el bot ejecuta una **entrada larga** en Testnet.

Los niveles de **Take Profit (TP)** y **Stop Loss (SL)** se calculan con porcentajes definidos en `settings.py`.

---

## 🧱 Arquitectura técnica

| Módulo | Descripción |
|--------|--------------|
| **core/** | Lógica de negocio: estrategias, riesgo, ejecución |
| **services/** | Clientes externos (Binance API) |
| **data/** | Fuentes de datos del mercado |
| **utils/** | Logging, herramientas comunes |
| **config/** | Parámetros globales de operación |
| **logs/** | Historial de ejecución y errores |

El archivo `main.py` coordina el flujo completo: conexión → obtención de precios → cálculo de indicadores → evaluación de estrategia → ejecución de trade → logging.

---

## 🧠 Buenas prácticas

- No reutilizar las claves de **producción** en testnet.  
- Ajustar `EMA_PERIOD` y `RSI_PERIOD` según tu estrategia.  
- Mantener los logs para diagnóstico (`logs/errors.log`).  
- Usar entorno virtual para aislar dependencias.  
- Realizar pruebas extensivas antes de operar con dinero real.

---

## 🧩 Dependencias principales

Listado en `requirements.txt`:

```
python-binance
pandas
numpy
python-dotenv
```

---

## 🪪 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.  
Puedes usarlo, modificarlo y distribuirlo libremente con la debida atribución.

---

## 📬 Contacto

Desarrollado por Alejandro Llordén Rodríguez  
📧 Email: allorden98@gmail.com 
🌐 GitHub: https://github.com/Llordax

---

> ⚠️ **Aviso:** Este bot está destinado únicamente a fines educativos y de prueba.  
> No debe usarse con dinero real sin una comprensión completa del riesgo asociado.
