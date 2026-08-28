# Reglas de Negocio (Business Rules) - Proyecto Trinity

Este documento contiene las restricciones lógicas, límites operacionales y políticas de negocio obligatorias que el sistema **Trinity** debe hacer cumplir estrictamente en todas sus capas de código.

---

## 1. Políticas de Control de Envíos y Anti-Baneo
Para mitigar el riesgo de que los algoritmos de Meta clasifiquen la actividad como spam o automatización maliciosa, el código debe restringir el comportamiento bajo las siguientes reglas métricas:

*   **Límite Diario Estricto:** Ninguna instalación podrá enviar más de **45 mensajes en un periodo de 24 horas**.
*   **Frecuencia de Operación:** La campaña operará un máximo de **6 días a la semana**. El sistema debe permitir pausar o bloquear el envío el séptimo día de forma automatizada o manual.
*   **Intervalos de Retraso Humano (Human-like Delay):** Está estrictamente prohibido enviar mensajes con una frecuencia matemática fija (ej. cada 5 segundos). 
    *   Entre el envío de un mensaje y el siguiente, la capa de infraestructura debe aplicar un retraso aleatorio obligatorio basado en un rango variable (parámetros por defecto: mínimo 30 segundos, máximo 90 segundos).

---

## 2. Gestión de Datos y Estado de los Contactos
El procesamiento del archivo maestro de 10,000 clientes está sujeto a las siguientes reglas de integridad de datos:

*   **Idempotencia y Prevención de Duplicidad:** Un cliente **jamás** debe recibir el mismo mensaje dos veces en una campaña. El sistema debe garantizar que un número telefónico marcado como procesado quede fuera de futuros bucles de selección.
*   **Persistencia Inmediata por Registro:** El estado de cada cliente (`PENDIENTE`, `ENVIADO`, `FALLIDO`) debe actualizarse e impactar en la base de datos local inmediatamente después de que Playwright intente la acción de envío. No se permite acumular estados en memoria para guardados masivos al final del día (tolerancia a fallos por apagones).
*   **Ciclo de Vida del Estado del Cliente:**
    *   `PENDIENTE`: Estado inicial al importar desde Excel. Listo para ser seleccionado.
    *   `ENVIADO`: Confirmación exitosa por parte de la interfaz de automatización web.
    *   `FALLIDO`: Error en el proceso (número inválido, chat bloqueado o caída de sesión). Debe guardarse la marca de tiempo del fallo.

---

## 3. Validación y Normalización de Entradas
Antes de almacenar cualquier registro en la base de datos o pasárselo a la API de WhatsApp, la capa de lógica correspondiente debe forzar la limpieza del dato:

*   **Estructura Telefónica:** Se deben eliminar espacios en blanco, guiones, paréntesis o caracteres especiales. El número final debe contener únicamente dígitos numéricos junto con su respectivo código de país de forma obligatoria.
*   **Protección contra Inyecciones o Cargas Corruptas:** Si una fila del Excel no cuenta con los campos esenciales (`Nombre` y `Teléfono` válidos), el registro debe rechazarse inmediatamente o moverse a una cola de registros corruptos/omitidos, sin interrumpir la lectura del resto de las 10,000 filas.

---

## 4. Multi-Instalación On-Premise (Estrategia Share-Nothing)
Para escenarios donde una sucursal requiera distribuir la carga de los 10,000 contactos o mas en múltiples computadoras sin conectividad de red entre ellas:

*   **Aislamiento Total de Datos:** Cada computadora es soberana y opera de manera aislada con su propio archivo de base de datos local (`trinity.db`).
*   **División Preventiva en Origen:** Para evitar colisiones o envíos duplicados al mismo cliente desde dos máquinas distintas, el archivo maestro original de 10k debe ser fraccionado de manera determinista y única antes de ser importado por el software en cada computadora (División automatizada de archivos vía UI) esta parte sigue en revision y tambien es posible que el trabajo de dividir el archivo excel se haga manualmente.
