import re
import time
import random
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class WhatsAppScraperError(Exception):
    """Error base para los fallos controlados del envío por WhatsApp."""

class ChatNotFoundError(WhatsAppScraperError):
    pass

class SendFailedError(WhatsAppScraperError):
    pass

class PageNotReadyError(WhatsAppScraperError):
    pass

WHATSAPP_URL = "https://web.whatsapp.com/"
PROFILE_DIR = "Data/profile"
EXCEL_PATH = "Workbook1.xlsx"
LOGIN_TIMEOUT_SEC = 900

MESSAGES = {
    1: (
        "👋 ¡Hola! Nos contactaste anteriormente. Si no recuerdas haberlo hecho, por favor "
        "ignora este mensaje. En South American Language Center Cotopaxi "
        "tenemos una forma diferente de aprender: clases personalizadas, "
        "práctica y acompañamiento para que avances de verdad. "
        "🗣️✨🎯 Si tu objetivo es mejorar para estudiar, trabajar, viajar "
        "o comunicarte con más confianza, ¡este es un buen momento para comenzar! "
        "📲 Contáctanos y agenda tu prueba de ubicación. ¡Da el primer paso!"
    ),
    2: (
        "👋 ¡Hola! Nos contactaste tiempo atras, Si no fuiste tu porfavor "
        "ignora este mensaje. En South American Language Center Cotopaxi "
        "tenemos una forma diferente de aprender: clases personalizadas, "
        "experiencias prácticas y acompañamiento para que avances de verdad. "
        "🗣️✨ 🎯 Si estás buscando mejorar tu inglés para estudiar, trabajar, "
        "viajar o simplemente sentirte más seguro al hablar, este puede ser "
        "tu momento.📲 Escríbenos y agenda tu prueba de ubicación. ¡Empieza hoy!"
    ),
    3: (
        "👋 ¡Hola! Nos contactaste tiempo atrás y queremos ayudarte a continuar con tu proceso. Si no fuiste tú, por favor "
        "ignora este mensaje. En South American Language Center Cotopaxi "
        "ofrecemos clases personalizadas, práctica y acompañamiento "
        "para que aprender inglés sea más sencillo y puedas ver resultados. "
        "🗣️✨🎯 Si quieres mejorar tu inglés para estudiar, trabajar, viajar "
        "o hablar con mayor confianza, ¡este puede ser tu momento! "
        "📲 Escríbenos para conocer más y agenda tu prueba de ubicación. ¡Empieza hoy!"
    ),
    4: (    
        "👋 ¡Hola! Nos contactaste hace algún tiempo. Si no fuiste tú,"
        "por favor ignora este mensaje. En South American Language Center Cotopaxi"
        "tenemos una manera diferente de aprender: clases personalizadas, "
        "experiencias prácticas y acompañamiento para que realmente puedas avanzar."
        "🗣️✨🎯 Si quieres mejorar tu inglés para estudiar, trabajar,"
        "viajar o simplemente ganar confianza al hablar, ¡este puede ser"
        "el momento! 📲 Escríbenos y agenda tu prueba de ubicación. ¡Empieza hoy!"
    )
}

IMAGES = {
    1: r"C:\Users\brown\Downloads\salc.jpeg",
    2: r"C:\Users\brown\Downloads\salc.jpeg",
    3: r"C:\Users\brown\Downloads\salc.jpeg",
    4: r"C:\Users\brown\Downloads\salc.jpeg",
}

SEL_SEARCH_INPUT = "#side input"
SEL_COMPOSE_BOX = "[data-testid='conversation-compose-box-input']"
SEL_NEW_CHAT_BTN = (
    "[aria-label='Nuevo chat'], [aria-label='New chat'], "
    "[title='Nuevo chat'], [title='New chat'], "
    "#side [data-icon='chat']"
)
SEL_NEW_CONTACT_BTN = (
    "[aria-label='Nuevo contacto'], [aria-label='New contact'], "
    "[title='Nuevo contacto'], [title='New contact'], "
    "[role='button']:has-text('Nuevo contacto'), "
    "[role='button']:has-text('New contact')"
)
SEL_CONTACT_PHONE_INPUT = [
    "input[type='tel']",
    "input[name*='phone' i]",
    "input[placeholder*='teléfono' i]",
    "input[placeholder*='telefono' i]",
    "input[placeholder*='phone' i]",
    "input[aria-label*='teléfono' i]",
    "input[aria-label*='telefono' i]",
    "input[aria-label*='phone' i]",
]
SEL_CONTACT_NAME_INPUT = [
    "input[placeholder='Nombre']",
    "input[aria-label='Nombre']",
    "input[name='firstName']",
    "input[autocomplete='given-name']",
    "input[placeholder*='nombre' i]:not([placeholder*='usuario' i])",
    "input[aria-label*='nombre' i]:not([aria-label*='usuario' i])",
    "input[placeholder='First name']",
    "input[aria-label='First name']",
]
SEL_SAVE_CONTACT = [
    "button[aria-label='Guardar']",
    "button[aria-label='Save']",
    "button[title='Guardar']",
    "button[title='Save']",
    "[role='button'][aria-label='Guardar']",
    "[role='button'][aria-label='Save']",
    "button:has([data-icon='checkmark'])",
    "[role='button']:has([data-icon='checkmark'])",
    "button:has([data-icon='check'])",
    "[role='button']:has([data-icon='check'])",
]
PHONE_ON_WHATSAPP = re.compile(
    r"Este número de teléfono está en WhatsApp|This phone number is on WhatsApp",
    re.I,
)
PHONE_ALREADY_CONTACT = re.compile(
    r"Este número de teléfono ya está en tus contactos|"
    r"This phone number is already in your contacts",
    re.I,
)
ADDRESS_BOOK_CONFIRMATION = re.compile(
    r"Se añadirá este contacto a la libreta de contactos de tu teléfono|"
    r"This contact will be added to your phone's address book",
    re.I,
)
SEL_ATTACH_BTN = (
    "button[aria-label='Adjuntar'], button[data-testid='compose-btn-attach'], "
    "div[title='Adjuntar'], [aria-label*='Adjuntar']"
)
SEL_MEDIA_FILE_INPUT = "input[type='file'][accept*='video']"
SEL_MEDIA_PREVIEW = (
    "[data-testid='media-preview'], [data-testid='media-preview-content'], "
    "div[role='dialog'], img[src^='blob:'], video[src^='blob:']"
)
SEL_PHOTOS_MENU = re.compile(r"fotos? y videos|photos|imágenes y videos", re.I)
SEL_SEND_BUTTONS = [
    "button[data-testid='compose-btn-send']",
    "#main button[aria-label='Enviar']",
    "#main button[aria-label='Send']",
    "#main [role='button'][aria-label='Enviar']",
    "#main [role='button'][aria-label='Send']",
    "button:has([data-icon='wds-ic-send-filled'])",
    "[role='button']:has([data-icon='wds-ic-send-filled'])",
    "button:has([data-icon='send'])",
    "[role='button']:has([data-icon='send'])",
]

DIALOG_LABELS = [
    "Aceptar", "Continuar", "Enviar", "OK", "Listo",
    "Hecho", "Guardar", "Done", "Continue", "Ok", "Close", "Cerrar",
]

JS_CLICK_SEARCH_RESULT = """(num) => {
    const re = /usuarios que no est[áa]n en tus contactos|no se encuentr[ao] en tus contactos|tus contactos/i;
    const rowSel = "[role='button'], [role='row'], [role='option'], [data-testid='cell-frame-container']";
    const digits = (num || '').replace(/\\D/g, '');
    const tail = digits.slice(-9);
    let header = null;
    const all = document.querySelectorAll('span, div');
    for (const e of all) {
        if (e.childElementCount > 0) continue;
        const t = (e.textContent || '').trim();
        if (t.length > 3 && t.length < 60 && re.test(t)) { header = e; break; }
    }
    if (!header) return 'no-header';
    const bottom = header.getBoundingClientRect().bottom;
    const tryClick = (r) => {
        r.scrollIntoView({ block: 'center' });
        r.click();
        return 'clicked';
    };
    let scope = header;
    for (let i = 0; i < 8 && scope; i++) {
        scope = scope.parentElement;
        if (!scope) continue;
        const rows = scope.querySelectorAll(rowSel);
        for (const r of rows) {
            const b = r.getBoundingClientRect();
            if (b.top >= bottom - 10 && b.width > 0 && b.height > 0) {
                return tryClick(r);
            }
        }
    }
    scope = header;
    for (let i = 0; i < 8 && scope; i++) {
        scope = scope.parentElement;
        if (!scope) continue;
        const all = scope.querySelectorAll('*');
        for (const r of all) {
            const b = r.getBoundingClientRect();
            if (!(b.top >= bottom - 10 && b.width > 0 && b.height > 0)) continue;
            if (r.childElementCount > 0) continue;
            const txt = (r.textContent || '').replace(/\\D/g, '');
            if (tail && txt.indexOf(tail) !== -1) {
                return tryClick(r);
            }
        }
    }
    return 'no-row';
}"""


def load_contacts(excel_path: str) -> list[tuple[str, str]]:
    """Carga teléfono y asesor desde Workbook1.xlsx."""
    df = pd.read_excel(excel_path, dtype={"TELEFONO": "string", "ASESOR": "string"})
    required_columns = {"TELEFONO", "ASESOR"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise WhatsAppScraperError(
            "Faltan columnas en el Excel: " + ", ".join(sorted(missing_columns))
        )

    contacts = []
    for _, row in df.iterrows():
        phone = re.sub(r"\D", "", str(row["TELEFONO"]))
        advisor_name = str(row["ASESOR"]).strip() if pd.notna(row["ASESOR"]) else ""
        if phone and advisor_name:
            contacts.append((phone, advisor_name))
    return contacts


def human_delay(min_sec: float = 0.2, max_sec: float = 0.5) -> None:
    time.sleep(random.uniform(min_sec, max_sec))


def type_like_human(page: Page, selector: str, text: str) -> None:
    locator = page.locator(selector)
    locator.click(timeout=4000)
    human_delay(0.2, 0.4)
    locator.fill("", timeout=4000)
    human_delay(0.1, 0.2)
    for ch in text:
        locator.type(ch, delay=random.randint(60, 140), timeout=4000)


def dismiss_dialog(page: Page) -> None:
    try:
        dialog = page.locator("div[role='dialog']:visible").first
        if not (dialog.count() and dialog.is_visible()):
            return
        for label in DIALOG_LABELS:
            try: 
                btn = page.get_by_text(label, exact=True).first
                if btn.count() and btn.is_visible():
                    btn.click(timeout=1500)
                    human_delay(0.4, 0.9)
                    return
            except Exception:
                continue
        btns = dialog.locator("button")
        if btns.count():
            btns.last.click(timeout=1500)
            human_delay(0.4, 0.9)
    except Exception:
        pass


def click_first_visible(page: Page, selectors: list[str], timeout: int = 2000) -> bool:
    for selector in selectors:
        try:
            page.locator(selector).first.click(timeout=timeout)
            return True
        except Exception:
            continue
    return False


def fill_first_visible(page: Page, selectors: list[str], text: str) -> bool:
    """Escribe en el primer campo visible que coincida con los selectores."""
    for selector in selectors:
        locator = page.locator(selector)
        for index in range(locator.count()):
            field = locator.nth(index)
            try:
                if not field.is_visible():
                    continue
                field.click(timeout=2000)
                field.fill("", timeout=2000)
                field.type(text, delay=random.randint(60, 140), timeout=5000)
                return True
            except Exception:
                continue
    return False


def type_into_field(field, text: str) -> bool:
    """Limpia y escribe el texto carácter por carácter en un campo."""
    field.click(timeout=2000)
    field.fill("", timeout=2000)
    field.type(text, delay=random.randint(60, 140), timeout=5000)
    return True


def type_in_labeled_field(page: Page, labels: list[str], text: str) -> bool:
    """Prioriza el control asociado exactamente a la etiqueta indicada."""
    for label in labels:
        field = page.get_by_label(label, exact=True).first
        try:
            if field.count() and field.is_visible():
                return type_into_field(field, text)
        except Exception:
            continue
    return False


def fill_contact_phone(page: Page, phone: str) -> bool:
    """Rellena y comprueba el campo específico de teléfono."""
    if type_in_labeled_field(page, ["Número de teléfono", "Teléfono"], phone):
        return True

    for selector in SEL_CONTACT_PHONE_INPUT:
        fields = page.locator(selector)
        for index in range(fields.count()):
            field = fields.nth(index)
            try:
                if not field.is_visible():
                    continue
                type_into_field(field, phone)
                entered = re.sub(r"\D", "", field.input_value(timeout=1000))
                if entered.endswith(re.sub(r"\D", "", phone)):
                    return True
            except Exception:
                continue
    return False


def fill_contact_name(page: Page, advisor_name: str) -> bool:
    """Rellena exclusivamente el campo «Nombre», nunca «Nombre de usuario»."""
    if type_in_labeled_field(page, ["Nombre", "First name"], advisor_name):
        return True
    return fill_first_visible(page, SEL_CONTACT_NAME_INPUT, advisor_name)


def confirm_add_to_address_book(page: Page) -> bool:
    """Activa la opción que habilita el ✓ para guardar el contacto."""
    try:
        control = page.get_by_text(ADDRESS_BOOK_CONFIRMATION).first
        control.wait_for(state="visible", timeout=5000)
        control.evaluate(
            """element => {
                const target = element.closest(
                    'label, button, [role="button"], [role="checkbox"]'
                ) || element;
                target.click();
            }"""
        )
        human_delay(0.3, 0.6)
        return True
    except Exception:
        return False


def cancel_new_contact(page: Page) -> None:
    """Vuelve al listado de chats sin abrir ni enviar un mensaje."""
    back_buttons = [
        "button[aria-label='Atrás']",
        "button[aria-label='Back']",
        "[role='button'][aria-label='Atrás']",
        "[role='button'][aria-label='Back']",
        "button:has([data-icon='back'])",
        "[role='button']:has([data-icon='back'])",
    ]
    if not click_first_visible(page, back_buttons, timeout=1500):
        page.keyboard.press("Escape")
    human_delay(0.4, 0.8)


def phone_is_already_contact(page: Page) -> bool:
    try:
        page.get_by_text(PHONE_ALREADY_CONTACT).first.wait_for(
            state="visible", timeout=3000
        )
        return True
    except Exception:
        return False


def save_new_contact(page: Page) -> bool:
    """Pulsa el ✓ de guardar contacto."""
    # Selector basado en el HTML real del botón de guardar de WhatsApp.
    svgs = page.locator("svg:has(title)")
    for index in range(svgs.count() - 1, -1, -1):
        icon = svgs.nth(index)
        try:
            if not icon.is_visible():
                continue
            title = icon.locator("title").text_content(timeout=1000)
            if (title or "").strip() != "ic-check":
                continue
            try:
                icon.click(timeout=3000)
            except Exception:
                icon.evaluate(
                    """element => {
                        const target = element.closest('button, [role="button"]')
                            || element.parentElement;
                        target.click();
                    }"""
                )
            return True
        except Exception:
            continue

    if click_first_visible(page, SEL_SAVE_CONTACT, timeout=5000):
        return True

    icons = page.locator("[data-icon='checkmark'], [data-icon='check']")
    for index in range(icons.count() - 1, -1, -1):
        icon = icons.nth(index)
        try:
            if not icon.is_visible():
                continue
            icon.evaluate(
                """element => {
                    const target = element.closest('button, [role="button"]')
                        || element.parentElement;
                    target.click();
                }"""
            )
            return True
        except Exception:
            continue
    return False


def get_chat_header_text(page: Page) -> str:
    return page.evaluate(
        "() => { const h = document.querySelector('#main header'); "
        "return h ? h.textContent.trim() : ''; }"
    )


def click_search_result(page: Page, phone: str) -> str:
    try:
        return page.evaluate(JS_CLICK_SEARCH_RESULT, phone)
    except Exception:
        return "error"


def open_new_chat(page: Page, phone: str, advisor_name: str) -> bool:
    """Crea el contacto en WhatsApp y espera a que se abra su conversación."""
    new_contact = page.locator(SEL_NEW_CONTACT_BTN).first
    try:
        # Tras descartar un contacto existente, WhatsApp vuelve a esta pantalla
        # y deja «Nuevo contacto» visible. En ese caso no abrir Nuevo chat otra vez.
        if not (new_contact.count() and new_contact.is_visible()):
            page.locator(SEL_NEW_CHAT_BTN).first.click(timeout=5000)
            human_delay(0.15, 0.3)
        new_contact.wait_for(state="visible", timeout=5000)
        new_contact.click(timeout=5000)
    except Exception:
        page.keyboard.press("Escape")
        return False
    human_delay(0.3, 0.6)

    old_header = get_chat_header_text(page)

    # WhatsApp habilita la confirmación inferior únicamente después de llenar
    # Nombre y Número de teléfono, en este orden.
    if not fill_contact_name(page, advisor_name):
        page.keyboard.press("Escape")
        return False

    if not fill_contact_phone(page, phone):
        page.keyboard.press("Escape")
        return False

    if phone_is_already_contact(page):
        cancel_new_contact(page)
        return False

    try:
        page.get_by_text(PHONE_ON_WHATSAPP).first.wait_for(
            state="visible", timeout=8000
        )
    except Exception:
        # No crear el contacto si WhatsApp no confirma que el número existe.
        page.keyboard.press("Escape")
        return False

    if not confirm_add_to_address_book(page):
        page.keyboard.press("Escape")
        return False

    if not save_new_contact(page):
        page.keyboard.press("Escape")
        return False

    deadline = time.time() + 8
    while time.time() < deadline:
        if get_chat_header_text(page) != old_header:
            return True
        time.sleep(0.1)

    page.keyboard.press("Escape")
    human_delay(0.4, 0.8)
    return False


def is_preview_open(page: Page) -> bool:
    try:
        preview = page.locator(SEL_MEDIA_PREVIEW)
        for index in range(preview.count()):
            if preview.nth(index).is_visible():
                return True
        return False
    except Exception:
        return False


def attach_image(page: Page, image_path: str) -> bool:
    if not Path(image_path).is_file():
        raise SendFailedError(f"No se encontró la imagen: {image_path}")

    # WhatsApp tiene campos distintos para stickers y para "Fotos y videos".
    # El de medios acepta también video; seleccionarlo evita enviar el JPEG
    # como sticker.
    try:
        page.locator(SEL_MEDIA_FILE_INPUT).first.set_input_files(
            image_path, timeout=5000
        )
        return True
    except Exception:
        pass

    try:
        page.locator(SEL_ATTACH_BTN).first.click(timeout=5000)
    except Exception:
        return False
    human_delay(1.0, 1.8)

    try:
        with page.expect_file_chooser(timeout=8000) as chooser:
            page.locator("[role='menuitem']").filter(
                has_text=SEL_PHOTOS_MENU
            ).last.click(timeout=5000)
        chooser.value.set_files(image_path)
        return True
    except Exception:
        pass

    try:
        page.locator(SEL_MEDIA_FILE_INPUT).first.set_input_files(
            image_path, timeout=5000
        )
        return True
    except Exception:
        page.keyboard.press("Escape")
        return False


def send_current_message(page: Page) -> bool:
    return click_first_visible(page, SEL_SEND_BUTTONS)


def send_message_with_image(page: Page, text: str, image_path: str) -> None:
    
    type_like_human(page, SEL_COMPOSE_BOX, text)

    if not attach_image(page, image_path):
        raise SendFailedError("No se pudo adjuntar la imagen")

    deadline = time.time() + 15
    while time.time() < deadline:
        if is_preview_open(page):
            break
        time.sleep(0.25)

    if not is_preview_open(page):
        raise SendFailedError("WhatsApp no mostró la vista previa de la imagen")

    
    time.sleep(1)
    if not send_current_message(page):
        raise SendFailedError("No se encontró el botón para enviar la imagen")


def send_random_message_with_image(page: Page) -> None:
    """Envía aleatoriamente una de las tres combinaciones mensaje + imagen."""
    message_type = random.choice(tuple(MESSAGES))
    send_message_with_image(page, MESSAGES[message_type], IMAGES[message_type])


def wait_for_whatsapp_ready(page: Page) -> None:
    deadline = time.time() + LOGIN_TIMEOUT_SEC
    while time.time() < deadline:
        try:
            page.locator(SEL_SEARCH_INPUT).first.wait_for(
                state="visible", timeout=3000
            )
            return
        except PlaywrightTimeoutError:
            pass
        for label in ("Usar aquí", "Use here"):
            try:
                page.get_by_text(label, exact=True).click(timeout=1200)
            except Exception:
                pass
        time.sleep(3)
    raise PageNotReadyError(f"WhatsApp no cargó en {LOGIN_TIMEOUT_SEC}s")


def run_whatsapp_sender(
    excel_path: str = EXCEL_PATH,
    headless: bool = False,
) -> None:
    contacts = load_contacts(excel_path)

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=["--disable-notifications"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(WHATSAPP_URL)

        wait_for_whatsapp_ready(page)
        human_delay(2, 4)

        for phone, advisor_name in contacts:
            dismiss_dialog(page)
            if not open_new_chat(page, phone, advisor_name):
                continue
            dismiss_dialog(page)
            human_delay(0.6, 1.4)
            send_random_message_with_image(page)
            human_delay(3, 5)

        context.close()


if __name__ == "__main__":
    try:
        run_whatsapp_sender()
    except WhatsAppScraperError as e:
        print(f"[ERROR] {e}")
        exit(1)
