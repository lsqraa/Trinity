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

## Reglas de Estilo de Código
1. Evita la sobre-documentación (Estilo IA):
  1. No uses docstrings estilo científico (con líneas de guiones --------- o explicaciones redundantes atributo por atributo).
  2. Si una clase, método o excepción tiene un nombre autoexplicativo (ej. ChatNotFoundError), no le agregues un docstring que repita lo que ya dice el nombre. Usa pass si la clase está vacía.
  3. Elimina comentarios que expliquen la arquitectura ("capa de infraestructura", "implementaciones futuras", etc.). Esas notas no van en el código de producción.
2. Consistencia en el manejo de errores y retornos:
  1. Si una función o método utiliza excepciones para controlar los fallos (ej. raise SendFailedError), su tipo de retorno debe ser None, no bool. No mezcles retornar False con lanzar excepciones para el mismo flujo de error. Si la función termina sin lanzar errores, el sistema asume que fue exitosa.
3. Diseño de Entidades de Dominio:
  1. Los IDs autoincrementales asignados por la base de datos (SQLite) deben ser opcionales en la entidad de Python (id: int | None = None). Esto nos permite instanciar el objeto al leer el Excel antes de que exista en la base de datos.
  2. Utiliza tipos de datos nativos avanzados como Enum para manejar estados fijos (ej. EstadoCliente) en lugar de pasar strings planos ('PENDIENTE', 'ENVIADO'). Esto evita errores de tipeo.
4. Estilo General: Escribe código directo, compacto, fuertemente tipado (type hints) y que vaya al grano. Piensa como un desarrollador senior humano, no como un generador de texto técnico.
5. No trabajar o hacer trabajo extra que no se te pidio, como test para los servicios, etc haz estrictamente lo que te pido yo y enfocate en lo que yo te diga que te enfoques.