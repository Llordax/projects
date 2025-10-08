# 🤖 Binance Bot Testnet — Versión Documentada 2025

Bot de **trading automatizado** diseñado para operar en **Binance Testnet**, con una arquitectura modular, documentación técnica completa y gestión integral del riesgo.  
El sistema analiza datos del mercado, genera señales mediante indicadores técnicos, ejecuta operaciones simuladas, registra resultados y mantiene logs detallados de toda su actividad.

---

## 🚀 Características

- ✅ Integración nativa con **Binance Testnet** (API oficial)
- 🧩 Arquitectura modular y escalable (core, data, services, utils, config)
- ⚙️ Configuración flexible mediante `.env` y `settings.py`
- 🧠 Gestión de riesgo avanzada con **Take Profit (TP)** y **Stop Loss (SL)**
- 🪵 Sistema completo de logging (ejecución y errores)
- 🔁 Reintentos automáticos ante fallos de conexión o red
- 📊 Registro histórico de operaciones en formato **Excel**
- 🧮 Indicadores técnicos integrados: **EMA** y **RSI**
- 🧱 Totalmente documentado para mantenimiento y extensión futura

---

## 🧭 Diagrama de funcionamiento del bot

```mermaid
flowchart TD

A[Inicio del bot - main.py] --> B[Conexión a Binance (get_client)]
B --> C[Obtención de datos OHLCV (get_ohlcv)]
C --> D[Cálculo de indicadores técnicos (EMA, RSI)]
D --> E[Evaluación de estrategia (check_entry)]
E -->|Condición cumplida| F[Ejecución de trade (execute_trade)]
E -->|Condición no cumplida| G[Esperar siguiente ciclo]

F --> H[Colocación de órdenes TP/SL (place_tp_sl_orders)]
H --> I[Registro de operación (log_trade)]
I --> J[Monitoreo en tiempo real (monitor_orders)]
J --> K[Actualización de logs y Excel]

K --> L[run_with_retry() - Reintento continuo]
G --> L
```

🧩 **Resumen del flujo:**
1️⃣ El bot se conecta a Binance (Testnet o real según configuración).  
2️⃣ Obtiene datos de precios y calcula EMA y RSI.  
3️⃣ Evalúa las condiciones de entrada definidas por la estrategia.  
4️⃣ Si se cumplen, ejecuta una orden de compra y coloca TP/SL.  
5️⃣ Registra toda la información en Excel y logs.  
6️⃣ Supervisa las órdenes activas en tiempo real.  
7️⃣ En caso de error, `run_with_retry` mantiene la ejecución continua.

---

## 📂 Estructura del proyecto

```
binance_bot_testnet/
├── main.py                     # Punto de entrada principal del bot
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Claves API privadas (no se versiona)
│
├── config/
│   └── settings.py             # Configuración global: parámetros RSI/EMA, TP/SL, símbolo, etc.
│
├── core/
│   ├── indicators.py           # Cálculo de indicadores EMA y RSI
│   ├── order_executor.py       # Ejecución de órdenes, TP/SL, registro y monitoreo
│   ├── order_monitor.py        # Supervisión y detección de ejecución de órdenes
│   ├── risk_management.py      # Cálculo de niveles de Take Profit y Stop Loss
│   ├── runner.py               # Bucle de ejecución continua con reintentos
│   └── strategy.py             # Lógica de estrategia técnica (EMA + RSI)
│
├── data/
│   └── price_fetcher.py        # Obtención de velas OHLCV desde Binance
│
├── services/
│   └── binance_client.py       # Conexión y autenticación con Binance (Testnet/Producción)
│
├── utils/
│   ├── logger.py               # Registro de operaciones en Excel (historial de trades)
│   └── logger_setup.py         # Configuración centralizada del sistema de logging
│
└── logs/
    ├── execution.log           # Log de ejecución y eventos operativos
    └── errors.log              # Log de errores y excepciones
```

---

## ⚙️ Requisitos previos

- Python **3.10+**  
- Cuenta en **Binance Testnet**  
- Claves API obtenidas en [https://testnet.binance.vision/](https://testnet.binance.vision/)  
- Recomendado: entorno virtual (`venv` o `conda`)

---

## 🔧 Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/tuusuario/binance_bot_testnet.git
cd binance_bot_testnet
```

2. **Crear y activar entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Crear archivo `.env` en la raíz del proyecto:**

```bash
BINANCE_API_KEY=tu_api_key
BINANCE_API_SECRET=tu_api_secret
```

5. **Configurar parámetros de trading en `config/settings.py`:**

```python
SYMBOL = "BTCEUR"
INTERVAL = "1h"
EMA_PERIOD = 50
RSI_PERIOD = 14
TP_PCTS = [0.015, 0.03, 0.045]
SL_PCTS = [0.005, 0.01, 0.015]
```

---

## ▶️ Ejecución

Ejecuta el bot con:

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

La estrategia técnica utilizada combina:
- **EMA (Exponential Moving Average):** Detecta tendencias y cruces alcistas/bajistas.  
- **RSI (Relative Strength Index):** Mide momentum y condiciones de sobrecompra/sobreventa.

Condición básica de entrada:
> RSI por debajo de 50 + EMA actual > EMA previa → Señal de compra

> ⚠️ Por razones de privacidad, la estrategia puede incluir ajustes adicionales no visibles públicamente.

Los niveles de **TP/SL** se definen como porcentajes relativos al precio de entrada en `config/settings.py`.

---

## 🧾 Logs e historial de operaciones

El bot registra toda la actividad en tiempo real en dos niveles:

### 🪵 Archivos de logs
```
logs/
├── execution.log   # Flujo general y órdenes ejecutadas
└── errors.log      # Errores, excepciones y fallos críticos
```

### 📘 Historial de operaciones (Excel)
Cada operación ejecutada se guarda en:
```
excel/trades_history.xlsx
```

Incluye:
- Timestamp  
- Order ID  
- Ticker  
- Tipo de orden (buy/sell/TP/SL)  
- Cantidad y precios (open/SL/TP/close)  
- Resultado de PnL  

---

## 🧱 Arquitectura técnica detallada

| Módulo | Función | Descripción |
|--------|----------|-------------|
| **main.py** | Orquestación general | Coordina la ejecución completa del bot |
| **core/indicators.py** | Cálculo técnico | Implementa EMA y RSI |
| **core/strategy.py** | Señal de entrada | Evalúa condiciones para ejecutar trades |
| **core/order_executor.py** | Ejecución operativa | Ejecuta compras, TP/SL y registra resultados |
| **core/order_monitor.py** | Supervisión activa | Detecta ejecuciones de TP/SL y cancela órdenes restantes |
| **core/risk_management.py** | Cálculo de riesgo | Define niveles de TP y SL según porcentajes |
| **core/runner.py** | Robustez | Mantiene ejecución con reintentos automáticos |
| **data/price_fetcher.py** | Datos de mercado | Descarga precios OHLCV desde Binance |
| **services/binance_client.py** | Conexión API | Gestiona autenticación y entorno Testnet/Real |
| **utils/logger_setup.py** | Logging global | Configura el sistema de registro (info y errores) |
| **utils/logger.py** | Historial de trades | Guarda todas las operaciones en Excel |

---

## 🧠 Buenas prácticas

- No reutilices las claves de **producción** en Testnet.  
- Ajusta los parámetros de `settings.py` antes de operar.  
- Supervisa regularmente los archivos de log (`logs/errors.log`).  
- Mantén el archivo `.env` fuera del control de versiones.  
- Usa entornos virtuales para aislar dependencias.  
- Prueba ampliamente el bot antes de usarlo en producción.

---

## 🧩 Dependencias principales

Listado en `requirements.txt`:

```
python-binance
pandas
numpy
python-dotenv
openpyxl
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
