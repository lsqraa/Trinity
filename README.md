# TRINITY

> **High-Precision On-Premise WhatsApp Outbound Engine & Multi-Campaign Prospecting Orchestrator**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-2463eb.svg?style=flat-square)](https://www.python.org/)
[![UI PyQt6](https://img.shields.io/badge/UI-PyQt6-10b981.svg?style=flat-square)](https://www.riverbankcomputing.com/software/pyqt/)
[![Automation Playwright](https://img.shields.io/badge/Automation-Playwright-3f3f46.svg?style=flat-square)](https://playwright.dev/python/)
[![Storage SQLite](https://img.shields.io/badge/Storage-SQLite-09090b.svg?style=flat-square)](https://www.sqlite.org/)
[![Architecture Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal%20%2F%20DDD-blueviolet.svg?style=flat-square)](#arquitectura-del-sistema)

---

## Resumen del Sistema

**Trinity** es una plataforma de escritorio de grado empresarial diseñada para la ingesta, depuración y despacho controlado de campañas de prospección masiva (hasta 10,000 registros) a través de WhatsApp Web.

A diferencia de los scripts de mensajería masiva convencionales que provocan bloqueos inmediatos de cuenta, Trinity está estructurado bajo una **política de mitigación de riesgo estricta**:
- **Cuota Diaria Blindada:** Límite infranqueable de 45 envíos diarios (6 días por semana).
- **Ejecución On-Premise:** Sesión persistente mediante almacenamiento local de cookies (`data/browser_session/`), preservando la reputación de la IP residencial y garantizando que ningún dato sensible de clientes viaje a servidores de terceros.
- **Validación Sintáctica y E.164:** Normalización automática de números telefónicos ecuatorianos y rotación de plantillas personalizadas con adjuntos multimedia.

---

## Arquitectura del Sistema

El núcleo de Trinity sigue una **Arquitectura Hexagonal (Puertos y Adaptadores)** simplificada orientada al dominio, garantizando desacoplamiento total entre las reglas de negocio, la base de datos, la automatización del navegador y la interfaz gráfica.

```
 Trinity
 ├── app/
 │   ├── domain/               # Entidades de Negocio puras y Puertos (Interfaces)
 │   │   ├── entities.py       # Cliente, Envio, EstadoEnvio (Enums)
 │   │   └── ports.py          # IEnvioRepository, IWhatsAppSender, IExcelReader
 │   ├── services/             # Lógica de Aplicación y Orquestación
 │   │   ├── scheduler.py      # Control de cuota diaria y ciclo de despacho
 │   │   ├── validator.py      # Normalización y descarte de números telefónicos
 │   │   └── message_personalization.py # Asignación de copy e imagen por asesor
 │   ├── infrastructure/       # Adaptadores de Entrada y Salida
 │   │   ├── database/         # SQLiteAdapter (Persistencia relacional)
 │   │   ├── excel/            # PandasWorker (Extracción y parseo de Excel)
 │   │   └── whatsapp/         # PlaywrightWhatsAppBot (Page Object Model)
 │   └── ui/                   # Capa de Presentación PyQt6
 │       └── main_window.py    # Monolith Dark UI, QStackedWidget y QThread Worker
 ├── config/                   # Configuración central y logger estructurado
 └── data/                     # Base de datos SQLite y sesión local del navegador
```

---

## Características Principales

### 1. Motor de Automatización Web con Playwright (POM)
* Implementado con el patrón **Page Object Model (POM)** en `PlaywrightWhatsAppBot`.
* Manejo determinista de selectores web con tiempos de espera explícitos para:
  - Verificación de sesión activa y carga de chats.
  - Validación de existencia de cuenta de WhatsApp previo al envío.
  - Adjunto de imágenes y despacho de texto simulando cadencia de tipeo humano con pausas aleatorias.

### 2. Persistencia y Control de Estado SQLite
* Seguimiento transaccional de cada mensaje (`PENDIENTE`, `ENVIADO`, `FALLIDO`).
* Historial de auditoría para registrar el último error capturado por Playwright (`ChatNotFoundError`, timeout, etc.).
* Consultas atómicas de conteo diario que impiden superar el límite configurado (`DAILY_MESSAGE_LIMIT = 45`).

### 3. Interfaz de Usuario Monolith Dark (PyQt6)
Inspirada en herramientas analíticas de alta densidad técnica (Snowflake Snowsight / Bloomberg Terminal):
* **Flujo Continuo Multi-Pantalla (`QStackedWidget`):**
  * **Upload Interface:** Dropzone central con soporte completo para *Drag & Drop* de hojas de cálculo `.xlsx` y validación visual inmediata.
  * **Processing Dashboard:** Vista dividida 60/40 que integra la cola de envíos con insignias de estado y la consola de logs del sistema en tiempo real.
* **Concurrencia Segura:** Despacho ejecutado en un hilo de trabajo (`EnvioWorker(QThread)`) para mantener la interfaz fluida en todo momento.
* **Reseteo Autónomo de Cuota:** `QTimer` pasivo que actualiza métricas y rehabilita el botón de inicio al cruzar la medianoche de forma desatendida.

---

## Requisitos del Entorno

* **Sistema Operativo:** Windows 10/11, macOS o Linux.
* **Python:** 3.10 o superior.
* **Google Chrome / Chromium:** Descargado y gestionado automáticamente por Playwright.

---

## Instalación y Puesta en Marcha

### 1. Clonar el repositorio y crear el entorno virtual
```bash
git clone https://github.com/tu-usuario/trinity.git
cd trinity

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# O en Linux/macOS:
# source venv/bin/activate
```

### 2. Instalar dependencias del proyecto
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configuración de Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto (opcional para sobreescribir defaults):
```env
DAILY_MESSAGE_LIMIT=45
SEND_DELAY_MIN=15
SEND_DELAY_MAX=35
DB_PATH=data/trinity.db
BROWSER_SESSION_DIR=data/browser_session
```

### 4. Ejecutar Trinity
```bash
python main.py
```

> **Nota para el primer inicio:**  
> En la primera ejecución, Playwright iniciará el navegador Chromium para que vincules tu cuenta de WhatsApp escaneando el código QR. Una vez autenticado, la sesión se almacenará localmente en `data/browser_session/` y no requerirá escanearse nuevamente en días posteriores.

---

## Estructura del Archivo de Importación (Excel)

Trinity detecta automáticamente las columnas necesarias sin importar el orden exacto:

| Columna Requerida | Formatos Aceptados | Descripción |
| :--- | :--- | :--- |
| **Teléfono** | `TELEFONO`, `CELULAR`, `NUMERO` | Número nacional o internacional (ej. `0991234567` o `593991234567`). |
| **Asesor** | `ASESOR`, `AGENTE`, `VENDEDOR` | Nombre del asesor asignado para seleccionar el mensaje y adjunto. |
| **Nombre** | `NOMBRE`, `NOMBRES`, `CLIENTE` | Nombre del cliente para personalización de saludo. |

---

## Créditos y Mantenimiento

Desarrollado y mantenido por **ElMichi** & **lsqraa**.  
Proyecto concebido para la gestión controlada y segura de prospección empresarial.
