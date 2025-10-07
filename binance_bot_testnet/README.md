# Binance Bot Testnet 🤖

Un bot de trading automatizado para **Binance Testnet**, diseñado con una arquitectura modular y una estrategia técnica propietaria basada en indicadores de análisis de mercado.  
Permite analizar datos, ejecutar operaciones simuladas, gestionar el riesgo y registrar toda la actividad en logs detallados.

---

## 🚀 Características

- ✅ Integración con **Binance Testnet** (API oficial)  
- 🧩 Arquitectura modular (core, data, services, utils)  
- ⚙️ Configuración sencilla mediante `.env` y `settings.py`  
- 🧠 Gestión de riesgo con **Take Profit (TP)** y **Stop Loss (SL)**  
- 🪵 Registro completo de logs (errores y ejecución)  
- 🔁 Sistema de reintento automático en caso de fallos de conexión  
- 🔒 Estrategia privada no visible en el repositorio público  

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
│   └── strategy.py             # Estrategia de trading (no pública)
├── data/
│   └── price_fetcher.py        # Obtención de precios y velas OHLCV
├── services/
│   └── binance_client.py       # Conexión con la API de Binance
├── utils/
│   ├── logger.py               # Registro de operaciones
│   └── logger_setup.py         # Configuración del sistema de logging
└── logs/
    ├── execution.log           # Registro de operaciones ejecutadas
    └── errors.log              # Registro de errores
```

---

## ⚙️ Requisitos previos

- Python **3.10+**  
- Una cuenta de **Binance Testnet**  
- Claves API de Testnet: [https://testnet.binance.vision/](https://testnet.binance.vision/)  
- Se recomienda usar un **entorno virtual** de Python (`venv` o `conda`)

---

## 🔧 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/binance_bot_testnet.git
cd binance_bot_testnet
```

2. Crear y activar un **entorno virtual** (aislado, no visual):

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` en la raíz (⚠️ no subirlo a GitHub):

```bash
BINANCE_API_KEY=tu_api_key
BINANCE_API_SECRET=tu_api_secret
```

5. Configurar los parámetros de trading en `config/settings.py`:

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
📈 Indicadores calculados correctamente
✅ Condición de entrada cumplida
Ejecutando trade...
```

---

## 🧮 Estrategia de Trading

El bot utiliza una **estrategia técnica privada** desarrollada para pruebas en Binance Testnet.  
Se basa en indicadores de **tendencia y momentum**, junto con reglas de gestión de riesgo dinámico.  

> ⚠️ Por motivos de privacidad y seguridad, la lógica exacta de la estrategia no se detalla públicamente.

Los niveles de **Take Profit (TP)** y **Stop Loss (SL)** se configuran mediante los porcentajes definidos en `config/settings.py`.

---

## 🧱 Arquitectura técnica

| Módulo | Descripción |
|--------|--------------|
| **core/** | Lógica de negocio: indicadores, ejecución y riesgo |
| **services/** | Conexión y autenticación con la API de Binance |
| **data/** | Descarga de datos OHLCV del mercado |
| **utils/** | Logging, almacenamiento y registro de operaciones |
| **config/** | Parámetros globales del bot |
| **logs/** | Historial de ejecución y errores |

El archivo `main.py` coordina todo el flujo: conexión → datos → análisis → estrategia → ejecución → logging.

---

## 🧾 Logs e historial de operaciones

El bot guarda toda su actividad en la carpeta `logs/`:

```
logs/
├── execution.log   # Operaciones ejecutadas y flujo general
└── errors.log      # Errores o excepciones ocurridas
```

Además, cada operación se registra en un archivo Excel:
```
excel/trades_history.xlsx
```

Este historial incluye:
- Ticker, cantidad y tipo de orden  
- Precio de entrada y salida  
- Niveles de TP/SL  
- PnL (ganancia/pérdida)  

---

## 🧠 Buenas prácticas

- No reutilizar las claves de **producción** en testnet.  
- Ajustar los parámetros en `settings.py` según tus objetivos.  
- Revisar regularmente los logs (`logs/errors.log`).  
- Mantener el archivo `.env` fuera del repositorio.  
- Usar siempre un entorno virtual para aislar dependencias.  
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

Desarrollado por **Alejandro Llordén Rodríguez**  
📧 Email: allorden98@gmail.com  
🌐 GitHub: [https://github.com/Llordax](https://github.com/Llordax)

---

> ⚠️ **Aviso:** Este bot está destinado únicamente a fines educativos y de prueba.  
> No debe usarse con dinero real sin una comprensión completa del riesgo asociado.
