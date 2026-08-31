# Component Library — PyQt6 Modern Enterprise Design System

> Copy-paste-ready PyQt6 components. Every component uses design tokens from
> `design_tokens.md` and is styled via the QSS patterns in `qss_patterns.md`.
> All comments are in Spanish to match the user's tutorial language.

---

## Table of Contents

1. [ThemeManager](#1-thememanager)
2. [AppShell](#2-appshell)
3. [SidebarNav](#3-sidebarnav)
4. [TopAppBar](#4-topappbar)
5. [StatCard](#5-statcard)
6. [DataTable](#6-datatable)
7. [SearchInput](#7-searchinput)
8. [Button Factories](#8-button-factories)
9. [ModalDialog](#9-modaldialog)
10. [ToastNotification](#10-toastnotification)

---

## 1. ThemeManager

```python
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeManager(QObject):
    """
    Gestor de temas para la aplicación.
    Permite alternar entre modo claro y oscuro en tiempo de ejecución.

    Uso:
        theme_mgr = ThemeManager(app)
        theme_mgr.apply_theme("light")  # Aplicar tema inicial
        theme_mgr.toggle()              # Alternar tema
    """

    # Señal emitida cuando el tema cambia — envía "light" o "dark"
    theme_changed = pyqtSignal(str)

    def __init__(self, app: QApplication):
        super().__init__()
        self._app = app
        self._current_theme = "light"

    @property
    def current_theme(self) -> str:
        """Retorna el tema actual ('light' o 'dark')."""
        return self._current_theme

    @property
    def is_dark(self) -> bool:
        """Retorna True si el tema actual es oscuro."""
        return self._current_theme == "dark"

    def apply_theme(self, theme: str):
        """
        Aplica el tema especificado a toda la aplicación.

        Args:
            theme: 'light' o 'dark'
        """
        if theme == "dark":
            self._app.setStyleSheet(get_dark_qss())
        else:
            self._app.setStyleSheet(get_light_qss())
        self._current_theme = theme
        self.theme_changed.emit(theme)

    def toggle(self):
        """Alterna entre tema claro y oscuro."""
        new_theme = "dark" if self._current_theme == "light" else "light"
        self.apply_theme(new_theme)
```

---

## 2. AppShell

Main application window with sidebar, top bar, and scrollable content area.

```python
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt


class AppShell(QMainWindow):
    """
    Ventana principal de la aplicación con layout empresarial:
    - Sidebar de navegación (240px fijo)
    - Barra superior (64px fijo)
    - Área de contenido scrollable

    Uso:
        shell = AppShell()
        shell.set_sidebar(mi_sidebar)
        shell.set_content(mi_pagina)
        shell.show()
    """

    def __init__(self, title: str = "Mi Aplicación", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(1280, 800)

        # ── Widget central con layout horizontal ──
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar (panel izquierdo) ──
        self._sidebar_container = QWidget()
        self._sidebar_container.setObjectName("sidebar")
        self._sidebar_container.setFixedWidth(SIDEBAR_WIDTH)
        self._sidebar_layout = QVBoxLayout(self._sidebar_container)
        self._sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self._sidebar_layout.setSpacing(0)
        main_layout.addWidget(self._sidebar_container)

        # ── Panel derecho (top bar + contenido) ──
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Barra superior
        self._topbar_container = QWidget()
        self._topbar_container.setObjectName("topBar")
        self._topbar_container.setFixedHeight(TOPBAR_HEIGHT)
        self._topbar_layout = QHBoxLayout(self._topbar_container)
        self._topbar_layout.setContentsMargins(SPACING_LG, 0, SPACING_LG, 0)
        right_layout.addWidget(self._topbar_container)

        # Área de contenido scrollable
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Widget interno del scroll con padding
        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(
            SPACING_LG, SPACING_LG, SPACING_LG, SPACING_LG
        )
        self._content_layout.setSpacing(SPACING_MD)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_area.setWidget(self._content_widget)

        right_layout.addWidget(self._scroll_area)
        main_layout.addWidget(right_panel)

    def set_sidebar(self, widget: QWidget):
        """Establece el widget del sidebar."""
        # Limpiar layout existente
        while self._sidebar_layout.count():
            item = self._sidebar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._sidebar_layout.addWidget(widget)

    def set_topbar(self, widget: QWidget):
        """Establece el widget de la barra superior."""
        while self._topbar_layout.count():
            item = self._topbar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._topbar_layout.addWidget(widget)

    def set_content(self, widget: QWidget):
        """Establece el contenido principal (dentro del scroll)."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._content_layout.addWidget(widget)

    def add_content_widget(self, widget: QWidget):
        """Agrega un widget al área de contenido."""
        self._content_layout.addWidget(widget)

    @property
    def content_layout(self) -> QVBoxLayout:
        """Acceso directo al layout del contenido para agregar widgets."""
        return self._content_layout
```

---

## 3. SidebarNav

```python
from dataclasses import dataclass, field
from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal


@dataclass
class NavItem:
    """
    Define un elemento de navegación del sidebar.

    Atributos:
        id: Identificador único del item
        label: Texto visible del item
        icon: Carácter o identificador de icono (Google Material Symbols / FontAwesome)
        section: Sección/grupo al que pertenece (opcional)
        on_click: Callback al hacer clic (opcional)
    """
    id: str
    label: str
    icon: str = ""
    section: str = ""
    on_click: Optional[Callable] = None


class SidebarNav(QWidget):
    """
    Panel de navegación lateral con soporte para:
    - Secciones agrupadas con encabezado
    - Estado activo con indicador visual
    - Iconos (Google Material Symbols o FontAwesome)
    - Perfil de usuario en el footer

    Señales:
        item_clicked(str): Emite el ID del item seleccionado
    """

    item_clicked = pyqtSignal(str)

    def __init__(
        self,
        title: str = "Mi App",
        items: list[NavItem] = None,
        parent=None
    ):
        super().__init__(parent)
        self._items = items or []
        self._buttons: dict[str, QPushButton] = {}
        self._active_id: str = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_SM, SPACING_MD, SPACING_SM, SPACING_MD)
        layout.setSpacing(SPACING_XS)

        # ── Logo / Título de la app ──
        title_label = QLabel(title)
        title_label.setObjectName("sidebarTitle")
        layout.addWidget(title_label)

        # ── Espacio después del título ──
        layout.addSpacing(SPACING_MD)

        # ── Items de navegación agrupados por sección ──
        current_section = None
        for item in self._items:
            # Agregar encabezado de sección si es nuevo
            if item.section and item.section != current_section:
                current_section = item.section
                section_label = QLabel(item.section.upper())
                section_label.setObjectName("sidebarSection")
                layout.addWidget(section_label)

            # Crear botón de navegación
            btn = QPushButton(f"  {item.icon}  {item.label}" if item.icon else item.label)
            btn.setObjectName("sidebarNavItem")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", "false")

            # Conectar señal de clic
            btn.clicked.connect(lambda checked, item_id=item.id: self._on_item_click(item_id))
            if item.on_click:
                btn.clicked.connect(lambda checked, cb=item.on_click: cb())

            layout.addWidget(btn)
            self._buttons[item.id] = btn

        # ── Spacer para empujar el footer hacia abajo ──
        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # ── Footer: perfil de usuario (opcional, se puede ocultar) ──
        self._user_section = QWidget()
        self._user_section.setVisible(False)
        user_layout = QHBoxLayout(self._user_section)
        user_layout.setContentsMargins(SPACING_SM, SPACING_SM, SPACING_SM, SPACING_SM)

        self._user_avatar = QLabel("👤")
        self._user_avatar.setFixedSize(32, 32)
        self._user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(self._user_avatar)

        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(0)
        self._user_name = QLabel("Usuario")
        self._user_name.setProperty("class", "label")
        self._user_email = QLabel("email@ejemplo.com")
        self._user_email.setProperty("class", "caption")
        user_info_layout.addWidget(self._user_name)
        user_info_layout.addWidget(self._user_email)
        user_layout.addWidget(user_info)
        user_layout.addStretch()

        layout.addWidget(self._user_section)

    def set_active(self, item_id: str):
        """Establece el item activo por su ID."""
        # Desactivar el item anterior
        if self._active_id and self._active_id in self._buttons:
            old_btn = self._buttons[self._active_id]
            old_btn.setProperty("active", "false")
            old_btn.style().unpolish(old_btn)
            old_btn.style().polish(old_btn)

        # Activar el nuevo item
        if item_id in self._buttons:
            self._active_id = item_id
            new_btn = self._buttons[item_id]
            new_btn.setProperty("active", "true")
            new_btn.style().unpolish(new_btn)
            new_btn.style().polish(new_btn)

    def set_user(self, name: str, email: str, avatar: str = "👤"):
        """Muestra el perfil de usuario en el footer del sidebar."""
        self._user_name.setText(name)
        self._user_email.setText(email)
        self._user_avatar.setText(avatar)
        self._user_section.setVisible(True)

    def _on_item_click(self, item_id: str):
        """Maneja el clic en un item de navegación."""
        self.set_active(item_id)
        self.item_clicked.emit(item_id)
```

---

## 4. TopAppBar

```python
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal


class TopAppBar(QWidget):
    """
    Barra superior de la aplicación (64px de alto).
    Contiene: título, campo de búsqueda, y botón de cambio de tema.

    Señales:
        search_changed(str): Emite el texto de búsqueda cuando cambia
        theme_toggle_clicked(): Emite cuando se hace clic en el botón de tema
    """

    search_changed = pyqtSignal(str)
    theme_toggle_clicked = pyqtSignal()

    def __init__(self, title: str = "Dashboard", parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self.setFixedHeight(TOPBAR_HEIGHT)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING_LG, 0, SPACING_LG, 0)
        layout.setSpacing(SPACING_MD)

        # ── Título de la página ──
        self._title = QLabel(title)
        self._title.setObjectName("topBarTitle")
        layout.addWidget(self._title)

        # ── Spacer central ──
        layout.addStretch()

        # ── Campo de búsqueda ──
        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍 Buscar...")
        self._search.setFixedWidth(280)
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(self.search_changed.emit)
        layout.addWidget(self._search)

        # ── Botón de cambio de tema ──
        self._theme_btn = QPushButton("🌙")
        self._theme_btn.setProperty("class", "ghost")
        self._theme_btn.setFixedSize(40, 40)
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.setToolTip("Cambiar tema claro/oscuro")
        self._theme_btn.clicked.connect(self.theme_toggle_clicked.emit)
        layout.addWidget(self._theme_btn)

    def set_title(self, title: str):
        """Actualiza el título de la barra superior."""
        self._title.setText(title)

    def set_theme_icon(self, is_dark: bool):
        """Cambia el icono del botón de tema según el modo actual."""
        self._theme_btn.setText("☀️" if is_dark else "🌙")
```

---

## 5. StatCard

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class StatCard(QWidget):
    """
    Tarjeta de estadística para dashboards.
    Muestra un valor numérico con etiqueta, icono y tendencia opcional.

    Ejemplo:
        card = StatCard(
            icon="analytics",  # Google Material Symbol o FontAwesome glyph
            value="1,234",
            label="Usuarios Activos",
            trend="+12.5%",
            trend_up=True
        )
    """

    def __init__(
        self,
        icon: str = "",
        value: str = "0",
        label: str = "Métrica",
        trend: str = "",
        trend_up: bool = True,
        parent=None
    ):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(CARD_MIN_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        layout.setSpacing(SPACING_SM)

        # ── Fila superior: icono + tendencia ──
        top_row = QHBoxLayout()
        top_row.setSpacing(SPACING_SM)

        icon_label = QLabel(icon)
        icon_label.setProperty("class", "headline")
        top_row.addWidget(icon_label)

        top_row.addStretch()

        # Indicador de tendencia (si se proporciona)
        if trend:
            trend_label = QLabel(trend)
            trend_label.setObjectName("statTrendUp" if trend_up else "statTrendDown")
            top_row.addWidget(trend_label)

        layout.addLayout(top_row)

        # ── Valor principal (número grande) ──
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)

        # ── Etiqueta descriptiva ──
        desc_label = QLabel(label)
        desc_label.setObjectName("statLabel")
        layout.addWidget(desc_label)

        # Guardar referencias para actualización dinámica
        self._value_label = value_label
        self._trend_label = trend_label if trend else None

    def set_value(self, value: str):
        """Actualiza el valor mostrado en la tarjeta."""
        self._value_label.setText(value)

    def set_trend(self, trend: str, is_up: bool):
        """Actualiza el indicador de tendencia."""
        if self._trend_label:
            self._trend_label.setText(trend)
            self._trend_label.setObjectName(
                "statTrendUp" if is_up else "statTrendDown"
            )
            self._trend_label.style().unpolish(self._trend_label)
            self._trend_label.style().polish(self._trend_label)
```

---

## 6. DataTable

```python
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QLabel,
    QAbstractItemView
)
from PyQt6.QtCore import Qt


class DataTable(QWidget):
    """
    Tabla de datos estilizada con:
    - Búsqueda/filtro integrado
    - Filas con colores alternos
    - Cabeceras con estilo
    - Modos de redimensionamiento de columnas

    Ejemplo:
        table = DataTable(
            columns=["Nombre", "Email", "Rol", "Estado"],
            data=[
                ["Ana García", "ana@empresa.com", "Admin", "Activo"],
                ["Carlos López", "carlos@empresa.com", "Editor", "Inactivo"],
            ],
            searchable=True
        )
    """

    def __init__(
        self,
        columns: list[str],
        data: list[list[str]] = None,
        searchable: bool = True,
        title: str = "",
        parent=None
    ):
        super().__init__(parent)
        self._columns = columns
        self._data = data or []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_SM)

        # ── Encabezado de la tabla (título + búsqueda) ──
        header_row = QHBoxLayout()
        header_row.setSpacing(SPACING_MD)

        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "subtitle")
            header_row.addWidget(title_label)

        header_row.addStretch()

        if searchable:
            self._search = QLineEdit()
            self._search.setPlaceholderText("🔍 Filtrar...")
            self._search.setClearButtonEnabled(True)
            self._search.setFixedWidth(240)
            self._search.textChanged.connect(self._filter_rows)
            header_row.addWidget(self._search)

        layout.addLayout(header_row)

        # ── Tabla ──
        self._table = QTableWidget()
        self._table.setColumnCount(len(columns))
        self._table.setHorizontalHeaderLabels(columns)
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self._table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        self._table.setWordWrap(False)

        # Configurar alturas de filas
        self._table.verticalHeader().setDefaultSectionSize(TABLE_ROW_HEIGHT)

        # Modo de redimensionamiento: la última columna se estira
        header = self._table.horizontalHeader()
        for i in range(len(columns) - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            len(columns) - 1, QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self._table)

        # Cargar datos iniciales
        if self._data:
            self.set_data(self._data)

    def set_data(self, data: list[list[str]]):
        """Carga datos en la tabla (reemplaza el contenido existente)."""
        self._data = data
        self._table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                item.setFlags(
                    item.flags() & ~Qt.ItemFlag.ItemIsEditable
                )  # Solo lectura
                self._table.setItem(row_idx, col_idx, item)

    def add_row(self, row_data: list[str]):
        """Agrega una fila al final de la tabla."""
        row_idx = self._table.rowCount()
        self._table.insertRow(row_idx)
        for col_idx, cell_value in enumerate(row_data):
            item = QTableWidgetItem(str(cell_value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._table.setItem(row_idx, col_idx, item)
        self._data.append(row_data)

    def clear(self):
        """Elimina todas las filas de la tabla."""
        self._table.setRowCount(0)
        self._data.clear()

    def get_selected_row(self) -> Optional[int]:
        """Retorna el índice de la fila seleccionada, o None."""
        selected = self._table.selectedItems()
        return selected[0].row() if selected else None

    def _filter_rows(self, text: str):
        """Filtra las filas de la tabla según el texto de búsqueda."""
        search_text = text.lower()
        for row in range(self._table.rowCount()):
            match = False
            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self._table.setRowHidden(row, not match)
```

---

## 7. SearchInput

```python
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt


class SearchInput(QLineEdit):
    """
    Campo de búsqueda estilizado con:
    - Placeholder descriptivo
    - Botón de limpiar integrado
    - Señal de búsqueda con debounce opcional

    Ejemplo:
        search = SearchInput(placeholder="Buscar usuarios...")
        search.search_submitted.connect(lambda text: print(f"Buscando: {text}"))
    """

    search_submitted = pyqtSignal(str)

    def __init__(
        self,
        placeholder: str = "🔍 Buscar...",
        width: int = 280,
        parent=None
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
        self.setFixedWidth(width)
        self.setObjectName("searchInput")

        # Emitir búsqueda al presionar Enter
        self.returnPressed.connect(
            lambda: self.search_submitted.emit(self.text())
        )

    def keyPressEvent(self, event):
        """Manejo especial de tecla Escape para limpiar."""
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
        super().keyPressEvent(event)
```

---

## 8. Button Factories

Helper functions that create properly configured buttons with the right
`class` property for QSS styling.

```python
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


def create_primary_button(text: str, icon: str = "") -> QPushButton:
    """
    Crea un botón primario (azul corporativo, texto blanco).

    Args:
        text: Texto del botón
        icon: Carácter o identificador de icono (Google Material Symbols / FontAwesome)

    Returns:
        QPushButton configurado con class="primary"
    """
    label = f"{icon}  {text}" if icon else text
    btn = QPushButton(label)
    btn.setProperty("class", "primary")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def create_ghost_button(text: str, icon: str = "") -> QPushButton:
    """
    Crea un botón fantasma (transparente, texto azul).
    Ideal para acciones secundarias o dentro de tarjetas.

    Args:
        text: Texto del botón
        icon: Carácter o identificador de icono (Google Material Symbols / FontAwesome)

    Returns:
        QPushButton configurado con class="ghost"
    """
    label = f"{icon}  {text}" if icon else text
    btn = QPushButton(label)
    btn.setProperty("class", "ghost")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def create_danger_button(text: str, icon: str = "") -> QPushButton:
    """
    Crea un botón de peligro (rojo, para acciones destructivas).
    Usar solo para eliminar, descartar, o acciones irreversibles.

    Args:
        text: Texto del botón
        icon: Carácter o identificador de icono (Google Material Symbols / FontAwesome)

    Returns:
        QPushButton configurado con class="danger"
    """
    label = f"{icon}  {text}" if icon else text
    btn = QPushButton(label)
    btn.setProperty("class", "danger")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def create_secondary_button(text: str, icon: str = "") -> QPushButton:
    """
    Crea un botón secundario (estilo por defecto — fondo blanco, borde gris).

    Args:
        text: Texto del botón
        icon: Carácter o identificador de icono (Google Material Symbols / FontAwesome)

    Returns:
        QPushButton con estilo por defecto (sin class especial)
    """
    label = f"{icon}  {text}" if icon else text
    btn = QPushButton(label)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn
```

---

## 9. ModalDialog

```python
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt


class ModalDialog(QDialog):
    """
    Diálogo modal estilizado con:
    - Barra de título con botón de cerrar
    - Área de contenido personalizable
    - Fila de botones de acción en el footer

    Ejemplo:
        dialog = ModalDialog(
            title="Confirmar Acción",
            parent=main_window
        )
        dialog.set_content_text("¿Estás seguro de que deseas continuar?")
        dialog.add_action_button("Cancelar", dialog.reject)
        dialog.add_action_button("Confirmar", dialog.accept, primary=True)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            print("Confirmado")
    """

    def __init__(
        self,
        title: str = "Diálogo",
        width: int = 480,
        parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(width)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setObjectName("modalDialog")

        # ── Layout principal ──
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Container con bordes redondeados ──
        container = QWidget()
        container.setObjectName("card")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(
            SPACING_LG, SPACING_LG, SPACING_LG, SPACING_LG
        )
        container_layout.setSpacing(SPACING_MD)

        # ── Barra de título ──
        title_row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setProperty("class", "headline")
        title_row.addWidget(title_label)
        title_row.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setProperty("class", "ghost")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        title_row.addWidget(close_btn)

        container_layout.addLayout(title_row)

        # ── Área de contenido ──
        self._content_area = QWidget()
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(SPACING_SM)
        container_layout.addWidget(self._content_area)

        # ── Footer con botones de acción ──
        self._actions_row = QHBoxLayout()
        self._actions_row.setSpacing(SPACING_SM)
        self._actions_row.addStretch()
        container_layout.addLayout(self._actions_row)

        main_layout.addWidget(container)

    def set_content_text(self, text: str):
        """Establece un texto simple como contenido del diálogo."""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setProperty("class", "body")
        self._content_layout.addWidget(label)

    def set_content_widget(self, widget: QWidget):
        """Establece un widget personalizado como contenido del diálogo."""
        # Limpiar contenido anterior
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._content_layout.addWidget(widget)

    def add_action_button(
        self,
        text: str,
        callback,
        primary: bool = False,
        danger: bool = False
    ):
        """
        Agrega un botón de acción al footer del diálogo.

        Args:
            text: Texto del botón
            callback: Función a ejecutar al hacer clic
            primary: Si True, usa estilo de botón primario
            danger: Si True, usa estilo de botón de peligro
        """
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        if danger:
            btn.setProperty("class", "danger")
        elif primary:
            btn.setProperty("class", "primary")

        btn.clicked.connect(callback)
        self._actions_row.addWidget(btn)
```

---

## 10. ToastNotification

```python
from PyQt6.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
)


class ToastNotification(QLabel):
    """
    Notificación tipo toast que aparece temporalmente sobre la interfaz.
    Se auto-oculta después del timeout configurado.

    Niveles disponibles: "info", "success", "warning", "error"

    Ejemplo:
        # Mostrar un toast de éxito
        toast = ToastNotification.show_toast(
            parent=main_window,
            message="Registro guardado exitosamente",
            level="success",
            duration_ms=3000
        )
    """

    def __init__(
        self,
        message: str,
        level: str = "info",
        duration_ms: int = 3000,
        parent: QWidget = None
    ):
        super().__init__(message, parent)
        self.setObjectName("toast")
        self.setProperty("level", level)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setFixedWidth(360)
        self.adjustSize()
        self.setMinimumHeight(44)

        # ── Efecto de opacidad para animación ──
        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)

        # ── Posicionar en la parte superior central del padre ──
        if parent:
            x = (parent.width() - self.width()) // 2
            y = SPACING_LG
            self.move(x, y)

        # ── Animación de entrada (fade in) ──
        self._fade_in = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_in.setDuration(DURATION_NORMAL)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)
        self._fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        # ── Animación de salida (fade out) ──
        self._fade_out = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_out.setDuration(DURATION_SLOW)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_out.finished.connect(self._on_fade_out_done)

        # ── Timer para auto-ocultar ──
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(duration_ms)
        self._timer.timeout.connect(self._start_fade_out)

        # Iniciar animación
        self.show()
        self.raise_()
        self._fade_in.start()
        self._timer.start()

    def _start_fade_out(self):
        """Inicia la animación de desaparición."""
        self._fade_out.start()

    def _on_fade_out_done(self):
        """Elimina el widget después de que termine la animación."""
        self.deleteLater()

    @staticmethod
    def show_toast(
        parent: QWidget,
        message: str,
        level: str = "info",
        duration_ms: int = 3000
    ) -> "ToastNotification":
        """
        Método estático de conveniencia para mostrar un toast.

        Args:
            parent: Widget padre donde se mostrará el toast
            message: Mensaje a mostrar
            level: Nivel del toast ("info", "success", "warning", "error")
            duration_ms: Duración en milisegundos antes de ocultarse

        Returns:
            Instancia del ToastNotification creado
        """
        toast = ToastNotification(
            message=message,
            level=level,
            duration_ms=duration_ms,
            parent=parent
        )
        return toast
```

---

## Component Integration Example

Here's how to combine all components into a complete application:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout


def main():
    """Ejemplo completo integrando todos los componentes."""
    app = QApplication(sys.argv)

    # ── Inicializar gestor de temas ──
    theme_mgr = ThemeManager(app)
    theme_mgr.apply_theme("light")

    # ── Crear shell de la aplicación ──
    shell = AppShell(title="Enterprise Dashboard")

    # ── Configurar sidebar ──
    nav_items = [
        NavItem("dashboard", "Dashboard", "📊", "Principal"),
        NavItem("users",     "Usuarios",  "👥", "Principal"),
        NavItem("reports",   "Reportes",  "📈", "Principal"),
        NavItem("settings",  "Ajustes",   "⚙️", "Sistema"),
        NavItem("help",      "Ayuda",     "❓", "Sistema"),
    ]
    sidebar = SidebarNav(title="🏢 MiEmpresa", items=nav_items)
    sidebar.set_active("dashboard")
    sidebar.set_user("Ana García", "ana@empresa.com")
    shell.set_sidebar(sidebar)

    # ── Configurar barra superior ──
    topbar = TopAppBar(title="Dashboard")
    topbar.theme_toggle_clicked.connect(theme_mgr.toggle)
    theme_mgr.theme_changed.connect(
        lambda theme: topbar.set_theme_icon(theme == "dark")
    )
    shell.set_topbar(topbar)

    # ── Tarjetas de estadísticas ──
    cards_row = QWidget()
    cards_layout = QHBoxLayout(cards_row)
    cards_layout.setContentsMargins(0, 0, 0, 0)
    cards_layout.setSpacing(SPACING_MD)

    cards_layout.addWidget(StatCard("👥", "1,234", "Usuarios Activos", "+12.5%", True))
    cards_layout.addWidget(StatCard("📦", "567", "Pedidos Hoy", "+3.2%", True))
    cards_layout.addWidget(StatCard("💰", "$89,012", "Ingresos Mensual", "-2.1%", False))
    cards_layout.addWidget(StatCard("⚡", "99.9%", "Uptime", "+0.1%", True))
    shell.add_content_widget(cards_row)

    # ── Tabla de datos ──
    table = DataTable(
        columns=["Nombre", "Email", "Rol", "Estado"],
        data=[
            ["Ana García",    "ana@empresa.com",    "Administrador", "Activo"],
            ["Carlos López",  "carlos@empresa.com", "Editor",        "Activo"],
            ["María Rodríguez", "maria@empresa.com", "Visor",       "Inactivo"],
            ["Juan Martínez", "juan@empresa.com",   "Editor",        "Activo"],
        ],
        searchable=True,
        title="Usuarios Recientes"
    )
    shell.add_content_widget(table)

    # ── Mostrar ventana ──
    shell.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

---

## Helper Utilities

### apply_shadow

```python
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


def apply_shadow(widget, shadow_def: dict):
    """
    Aplica un efecto de sombra a un widget usando los tokens de sombra.

    Args:
        widget: QWidget al que aplicar la sombra
        shadow_def: Diccionario con blur_radius, x_offset, y_offset, color
    """
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(shadow_def["blur_radius"])
    effect.setXOffset(shadow_def["x_offset"])
    effect.setYOffset(shadow_def["y_offset"])
    r, g, b, a = shadow_def["color"]
    effect.setColor(QColor(r, g, b, a))
    widget.setGraphicsEffect(effect)
```

### refresh_style

```python
def refresh_style(widget):
    """
    Fuerza la re-evaluación del stylesheet QSS en un widget.
    Necesario después de cambiar propiedades dinámicas con setProperty().
    """
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
```
