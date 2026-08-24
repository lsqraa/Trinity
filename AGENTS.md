# BASE DE CONOCIMIENTO TÉCNICO: PROYECTO TRINITY
## Contexto de Arquitectura por Capas Orientada al Dominio (Hexagonal Simplificada)

**ESTE ES UN PROYECTO EN DESARROLLO** Recuerda siempre preguntar en que parte del desarrolo se encuentra para antes de crear cambios o hacer decisiones. Este archivo actúa como memoria de un chat anterior con otro agente que sirvio como ayuda en la toma de decisiones infraestructurales y research. 


---

## 1. CONTEXTO GENERAL DEL PROYECTO
- **Nombre:** Trinity
- **Propósito:** Automatización de prospección controlada y envío de mensajes de WhatsApp.
- **Volumen de datos:** Procesamiento masivo de archivos Excel (`.xlsx`) de hasta 10,000 clientes.
- **Regla de Negocio Crítica:** Enviar mensajes estrictamente a un máximo de 45 personas al día, 6 días a la semana (mitigación de riesgo de baneo).
- **Core Tecnológico:** 
  - **Presentación:** Interfaz de usuario nativa de Python (PyQt6 no definido aun).
  - **Lógica de Negocio:** Validación de teléfonos, orquestación de envíos y outputs
  - **Infraestructura:** Automatización web mediante **Playwright** (WhatsApp Web en navegador) y procesamiento de datos masivos con **Pandas**.
  - **Persistencia:** Base de datos relacional ligera integrada **SQLite** para control absoluto del estado.

---

## 2. ¿Por qué el proyecto es On-Premise?
Por tres razones críticas:
1. El bloqueo de WhatsApp Web: WhatsApp tiene sistemas avanzados de detección de robots. Si intentas correr Playwright en un servidor en la nube (donde las IPs cambian o pertenecen a centros de datos como Amazon), WhatsApp bloqueará la cuenta casi de inmediato.
2. Persistencia de la Sesión: Al abrir el navegador localmente, Playwright guarda las "cookies" y el historial en la carpeta data/browser_session/. Esto permite que solo escanees el código QR la primera vez. El programa recordará tu sesión localmente todos los días.
3. Privacidad de Datos Sensibles: Estás manejando información de 10,000 personas. Al ser On-Premise, esos datos nunca viajan ni se guardan en servidores externos de terceros; residen de forma segura en tu propio disco duro dentro de data/trinity.db.


