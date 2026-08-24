## 1. ESTRUCTURA COMPLETA DE DIRECTORIOS
```text
trinity/
├── app/
│   ├── __init__.py
│   ├── domain/              # CAPA 3: NÚCLEO DE DOMINIO (Reglas de Datos y Contratos)
│   │   ├── __init__.py
│   │   ├── entities.py      # Estructuras de datos puras (Cliente, Agente)
│   │   └── ports.py         # Interfaces abstractas (Contratos/Enchufes)
│   ├── services/            # CAPA 2: LÓGICA DE NEGOCIO (El Cerebro/Orquestador)
│   │   ├── __init__.py
│   │   ├── agent_brain.py   # Lógica e interacciones con Inteligencia Artificial
│   │   ├── scheduler.py     # Control de cuotas (45 diarios) y cronograma
│   │   └── validator.py     # Reglas de normalización de teléfonos
│   ├── infrastructure/      # CAPA 4: INFRAESTRUCTURA (Herramientas y adaptadores)
│   │   ├── __init__.py
│   │   ├── excel/           # Implementación de Pandas para leer .xlsx
│   │   │   └── pandas_worker.py
│   │   ├── database/        # Implementación de SQLite para persistencia local
│   │   │   └── sqlite_adapter.py
│   │   └── whatsapp/        # Implementación de Playwright para WhatsApp Web
│   │       └── playwright_bot.py
│   └── ui/                  # CAPA 1: PRESENTACIÓN (Interfaz nativa)
│       ├── __init__.py
│       └── main_window.py   # Ventanas, botones y lógica visual (Tkinter)
├── config/                  # Configuración centralizada y lectura de entorno
│   ├── __init__.py
│   └── settings.py          # Objeto 'settings' global
├── data/                    # Persistencia local (Sesión de navegador, trinity.db) [.gitignore]
├── docs/                    # Documentación técnica
│   └── ARCHITECTURE.md
├── tests/                   # Pruebas unitarias
├── .env                     # Variables secretas y llaves de API [.gitignore]
├── .gitignore               # Archivos ignorados por control de versiones
├── main.py                  # Punto de entrada único (Ensamblador e Inyección de Dependencias)
├── requirements.txt         # Dependencias del proyecto
└── AGENTS.md                # Prompts y roles de los agentes de IA
---

## 2. POR QUE SE DECIDIO USAR ESTRA ARQUITECTURA?
Porque de este modo, la aplicación es 100% escalable porque las herramientas (Playwright, Pandas, PyQt6, etc.) se vuelven piezas de Lego intercambiables, blindando el cerebro de tu proyecto ante cualquier cambio tecnológico futuro.
---

## 3. COMO SE USARA?
Paso 1 (La UI dispara la acción): Abres la interfaz gráfica en tu computadora y arrastras el Excel. La UI (app/ui/) no sabe leer Excel; solo toma la ruta del archivo y se la pasa al Servicio.

Paso 2 (El Servicio coordina): El Servicio (app/services/scheduler.py) recibe la ruta. Llama al adaptador de Pandas para extraer los 10k clientes (aprocimadamente pueden ser mas) y le ordena al adaptador de SQLite: "Guárdalos a todos".

Paso 3 (El bucle diario seguro): Cada día, al presionar "Iniciar", el Servicio le pide a SQLite los 45 clientes de hoy. Para cada cliente, el Servicio llama a message_personalizations.py el cual simplemente tiene un diccionario de los tipos de mensajes y los tipos de imagenes que se pueden enviar esto es algo que se hace manualmente por la persona en el codigo (app/services/message_personalizations.py) para generar el mensaje personalizado.

## Paso 4 **TODAVIA EN DESARROLLO** (La Infraestructura ejecuta): El Servicio le pasa el teléfono y el mensaje al bot de Playwright (app/infrastructure/whatsapp/). Playwright abre el navegador de tu computadora escribe el texto, hace clic en enviar, espera el tiempo aleatorio (ej. 45 segundos) y le devuelve un True al Servicio. SQLite marca al cliente como "ENVIADO".

