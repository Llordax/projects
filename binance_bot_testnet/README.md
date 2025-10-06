# 🤖 Binance Spot Trading Bot - RSI + EMA50 Estrategia Escalonada

Bot automatizado para operar en el mercado Spot de Binance utilizando la estrategia RSI + EMA50, con toma de ganancias (TP) y stop loss (SL) escalonados. Incluye integración con la Testnet de Binance, registro en Excel, y sistema de logging para seguimiento de actividad y errores.

---

## ⚙️ Características

- 📈 Estrategia basada en:
  - RSI < 50 + EMA50 creciente para compras
- 💸 Compra usando el 15% del saldo USDT disponible
- 🎯 TP y SL escalonados (3 niveles)
- 📊 Registro automático de operaciones en Excel (`/excel/trades_history.xlsx`)
- 🧾 Sistema de logs detallados:
  - Logs de ejecución: `logs/execution.log`
  - Logs de errores: `logs/errors.log`
- 🧪 Compatible con Binance Spot Testnet (modo demo)

---

## 🗂️ Estructura del Proyecto

