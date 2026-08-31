# QSS Patterns — PyQt6 Modern Enterprise Design System

> Complete Qt Style Sheet (QSS) reference with light and dark themes. All patterns
> use Python f-string interpolation with design token constants — **never hard-code
> hex values directly in QSS**.

---

## ThemeManager Class

Use this class to toggle between light and dark themes at runtime.

```python
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeManager(QObject):
    """Gestor de temas: alterna entre modo claro y oscuro."""

    theme_changed = pyqtSignal(str)  # Emite "light" o "dark"

    def __init__(self, app: QApplication):
        super().__init__()
        self._app = app
        self._current_theme = "light"

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @property
    def is_dark(self) -> bool:
        return self._current_theme == "dark"

    def apply_theme(self, theme: str):
        """Aplica el tema especificado ('light' o 'dark')."""
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

## Base QSS Template — Light Mode

```python
def get_light_qss() -> str:
    """Retorna el stylesheet completo para el modo claro."""
    return f"""
    /* ══════════════════════════════════════════════════════════════════
       RESET GLOBAL
       ══════════════════════════════════════════════════════════════════ */
    * {{
        margin: 0;
        padding: 0;
        font-family: {FONT_STACK};
        font-size: {FONT_SIZE_MD}px;
        color: {COLOR_ON_SURFACE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       VENTANA PRINCIPAL Y DIÁLOGOS
       ══════════════════════════════════════════════════════════════════ */
    QMainWindow {{
        background-color: {COLOR_BACKGROUND};
    }}

    QDialog {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-radius: {RADIUS_LG}px;
    }}

    QWidget {{
        background-color: transparent;
    }}

    /* ══════════════════════════════════════════════════════════════════
       SCROLLBARS (Estilo fino — 6px)
       ══════════════════════════════════════════════════════════════════ */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_OUTLINE_VARIANT};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLOR_OUTLINE};
    }}
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: none;
        height: 0;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {COLOR_OUTLINE_VARIANT};
        border-radius: 3px;
        min-width: 30px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {COLOR_OUTLINE};
    }}
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {{
        background: none;
        width: 0;
    }}

    /* ══════════════════════════════════════════════════════════════════
       BOTONES
       ══════════════════════════════════════════════════════════════════ */

    /* ── Botón por defecto (secundario) ── */
    QPushButton {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 600;
        min-height: 20px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_SURFACE_LOW};
        border-color: {COLOR_OUTLINE};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_SURFACE_HIGH};
    }}
    QPushButton:disabled {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_OUTLINE};
        border-color: {COLOR_OUTLINE_VARIANT};
    }}

    /* ── Botón primario ── */
    QPushButton[class="primary"] {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_ON_PRIMARY};
        border: none;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: {COLOR_PRIMARY_CONTAINER};
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: {COLOR_SURFACE_TINT};
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: {COLOR_OUTLINE_VARIANT};
        color: {COLOR_OUTLINE};
    }}

    /* ── Botón fantasma (ghost / text) ── */
    QPushButton[class="ghost"] {{
        background-color: transparent;
        color: {COLOR_PRIMARY};
        border: none;
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {COLOR_SURFACE_LOW};
    }}
    QPushButton[class="ghost"]:pressed {{
        background-color: {COLOR_SURFACE_HIGH};
    }}

    /* ── Botón de peligro (danger) ── */
    QPushButton[class="danger"] {{
        background-color: {COLOR_ERROR};
        color: {COLOR_ON_ERROR};
        border: none;
    }}
    QPushButton[class="danger"]:hover {{
        background-color: #a51515;
    }}
    QPushButton[class="danger"]:pressed {{
        background-color: {COLOR_ON_ERROR_CONTAINER};
    }}
    QPushButton[class="danger"]:disabled {{
        background-color: {COLOR_OUTLINE_VARIANT};
        color: {COLOR_OUTLINE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       INPUTS — QLineEdit, QTextEdit, QSpinBox, QComboBox
       ══════════════════════════════════════════════════════════════════ */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        selection-background-color: {COLOR_SURFACE_HIGHEST};
        selection-color: {COLOR_ON_SURFACE};
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {COLOR_PRIMARY};
        padding: {SPACING_SM - 1}px {SPACING_MD - 1}px;
    }}
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_OUTLINE};
    }}
    QLineEdit[readOnly="true"] {{
        background-color: {COLOR_SURFACE_LOW};
    }}

    QSpinBox, QDoubleSpinBox {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {COLOR_PRIMARY};
    }}
    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        background: transparent;
        border: none;
        width: 20px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {COLOR_SURFACE_HIGH};
    }}

    QComboBox {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        min-height: 20px;
    }}
    QComboBox:focus {{
        border: 2px solid {COLOR_PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
        subcontrol-origin: padding;
        subcontrol-position: center right;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_XS}px;
        selection-background-color: {COLOR_SURFACE_HIGH};
        selection-color: {COLOR_ON_SURFACE};
        outline: none;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TABLA — QTableWidget
       ══════════════════════════════════════════════════════════════════ */
    QTableWidget, QTableView {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_MD}px;
        gridline-color: {COLOR_OUTLINE_VARIANT};
        selection-background-color: {COLOR_SURFACE_HIGHEST};
        selection-color: {COLOR_ON_SURFACE};
        alternate-background-color: {COLOR_SURFACE_LOW};
        font-size: {FONT_SIZE_MD}px;
    }}
    QTableWidget::item, QTableView::item {{
        padding: {SPACING_SM}px {SPACING_MD}px;
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
    }}
    QTableWidget::item:selected, QTableView::item:selected {{
        background-color: {COLOR_SURFACE_HIGHEST};
    }}

    QHeaderView::section {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_ON_SURFACE_VARIANT};
        border: none;
        border-bottom: 2px solid {COLOR_OUTLINE_VARIANT};
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
        text-transform: uppercase;
    }}

    /* ══════════════════════════════════════════════════════════════════
       GROUPBOX
       ══════════════════════════════════════════════════════════════════ */
    QGroupBox {{
        background-color: {COLOR_SURFACE_LOWEST};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_MD}px;
        margin-top: 16px;
        padding: {SPACING_MD}px;
        padding-top: 28px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 {SPACING_SM}px;
        color: {COLOR_ON_SURFACE_VARIANT};
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       LABELS — Variantes tipográficas
       ══════════════════════════════════════════════════════════════════ */
    QLabel {{
        color: {COLOR_ON_SURFACE};
        background: transparent;
    }}
    QLabel[class="headline"] {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}
    QLabel[class="title"] {{
        font-size: {FONT_SIZE_2XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}
    QLabel[class="subtitle"] {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 600;
        color: {COLOR_ON_SURFACE};
    }}
    QLabel[class="body"] {{
        font-size: {FONT_SIZE_MD}px;
        font-weight: 400;
        color: {COLOR_ON_SURFACE};
    }}
    QLabel[class="label"] {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 500;
        color: {COLOR_ON_SURFACE_VARIANT};
    }}
    QLabel[class="caption"] {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 400;
        color: {COLOR_OUTLINE};
    }}
    QLabel[class="hero"] {{
        font-size: {FONT_SIZE_3XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       SIDEBAR
       ══════════════════════════════════════════════════════════════════ */
    #sidebar {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-right: 1px solid {COLOR_OUTLINE_VARIANT};
        min-width: {SIDEBAR_WIDTH}px;
        max-width: {SIDEBAR_WIDTH}px;
    }}

    #sidebarTitle {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 700;
        color: {COLOR_PRIMARY};
        padding: {SPACING_MD}px;
    }}

    #sidebarNavItem {{
        background-color: transparent;
        color: {COLOR_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        text-align: left;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        min-height: 36px;
    }}
    #sidebarNavItem:hover {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_ON_SURFACE};
    }}
    #sidebarNavItem[active="true"] {{
        background-color: {COLOR_SURFACE_HIGH};
        color: {COLOR_PRIMARY};
        font-weight: 600;
    }}

    #sidebarSection {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {COLOR_OUTLINE};
        padding: {SPACING_MD}px {SPACING_MD}px {SPACING_XS}px {SPACING_MD}px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TARJETAS (CARDS)
       ══════════════════════════════════════════════════════════════════ */
    #card {{
        background-color: {COLOR_SURFACE_LOWEST};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_MD}px;
    }}

    #statValue {{
        font-size: {FONT_SIZE_3XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}
    #statLabel {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 500;
        color: {COLOR_ON_SURFACE_VARIANT};
    }}
    #statTrendUp {{
        color: {COLOR_SUCCESS};
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
    }}
    #statTrendDown {{
        color: {COLOR_ERROR};
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOP BAR
       ══════════════════════════════════════════════════════════════════ */
    #topBar {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
        min-height: {TOPBAR_HEIGHT}px;
        max-height: {TOPBAR_HEIGHT}px;
        padding: 0 {SPACING_LG}px;
    }}

    #topBarTitle {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
        color: {COLOR_ON_SURFACE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       STATUS BAR
       ══════════════════════════════════════════════════════════════════ */
    QStatusBar {{
        background-color: {COLOR_SURFACE_LOW};
        color: {COLOR_ON_SURFACE_VARIANT};
        border-top: 1px solid {COLOR_OUTLINE_VARIANT};
        font-size: {FONT_SIZE_XS}px;
        padding: {SPACING_XS}px {SPACING_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       MENU BAR Y MENÚS
       ══════════════════════════════════════════════════════════════════ */
    QMenuBar {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
        padding: {SPACING_XS}px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: {SPACING_XS}px {SPACING_SM}px;
        border-radius: {RADIUS_SM}px;
    }}
    QMenuBar::item:selected {{
        background-color: {COLOR_SURFACE_HIGH};
    }}

    QMenu {{
        background-color: {COLOR_SURFACE_LOWEST};
        color: {COLOR_ON_SURFACE};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_XS}px;
    }}
    QMenu::item {{
        padding: {SPACING_SM}px {SPACING_MD}px;
        border-radius: {RADIUS_SM}px;
    }}
    QMenu::item:selected {{
        background-color: {COLOR_SURFACE_HIGH};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {COLOR_OUTLINE_VARIANT};
        margin: {SPACING_XS}px {SPACING_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOOLBAR
       ══════════════════════════════════════════════════════════════════ */
    QToolBar {{
        background-color: {COLOR_SURFACE_LOWEST};
        border-bottom: 1px solid {COLOR_OUTLINE_VARIANT};
        padding: {SPACING_XS}px;
        spacing: {SPACING_XS}px;
    }}
    QToolButton {{
        background: transparent;
        color: {COLOR_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_SM}px;
        padding: {SPACING_SM}px;
    }}
    QToolButton:hover {{
        background-color: {COLOR_SURFACE_HIGH};
        color: {COLOR_ON_SURFACE};
    }}
    QToolButton:pressed {{
        background-color: {COLOR_SURFACE_HIGHEST};
    }}
    QToolButton:checked {{
        background-color: {COLOR_SURFACE_HIGH};
        color: {COLOR_PRIMARY};
    }}

    /* ══════════════════════════════════════════════════════════════════
       PROGRESS BAR
       ══════════════════════════════════════════════════════════════════ */
    QProgressBar {{
        background-color: {COLOR_SURFACE_HIGH};
        border: none;
        border-radius: {RADIUS_SM}px;
        height: 8px;
        text-align: center;
        font-size: 0px;
    }}
    QProgressBar::chunk {{
        background-color: {COLOR_PRIMARY};
        border-radius: {RADIUS_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       CHECKBOX Y RADIO BUTTON
       ══════════════════════════════════════════════════════════════════ */
    QCheckBox {{
        spacing: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
        color: {COLOR_ON_SURFACE};
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {COLOR_OUTLINE};
        border-radius: {RADIUS_SM}px;
        background-color: {COLOR_SURFACE_LOWEST};
    }}
    QCheckBox::indicator:hover {{
        border-color: {COLOR_PRIMARY};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLOR_PRIMARY};
        border-color: {COLOR_PRIMARY};
    }}
    QCheckBox::indicator:disabled {{
        background-color: {COLOR_SURFACE_LOW};
        border-color: {COLOR_OUTLINE_VARIANT};
    }}

    QRadioButton {{
        spacing: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
        color: {COLOR_ON_SURFACE};
    }}
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {COLOR_OUTLINE};
        border-radius: 9px;
        background-color: {COLOR_SURFACE_LOWEST};
    }}
    QRadioButton::indicator:hover {{
        border-color: {COLOR_PRIMARY};
    }}
    QRadioButton::indicator:checked {{
        background-color: {COLOR_PRIMARY};
        border-color: {COLOR_PRIMARY};
    }}

    /* ══════════════════════════════════════════════════════════════════
       TAB WIDGET
       ══════════════════════════════════════════════════════════════════ */
    QTabWidget::pane {{
        background-color: {COLOR_SURFACE_LOWEST};
        border: 1px solid {COLOR_OUTLINE_VARIANT};
        border-top: none;
        border-radius: 0 0 {RADIUS_MD}px {RADIUS_MD}px;
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {COLOR_ON_SURFACE_VARIANT};
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        min-width: 80px;
    }}
    QTabBar::tab:hover {{
        color: {COLOR_ON_SURFACE};
        background-color: {COLOR_SURFACE_LOW};
    }}
    QTabBar::tab:selected {{
        color: {COLOR_PRIMARY};
        border-bottom: 2px solid {COLOR_PRIMARY};
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOOLTIP
       ══════════════════════════════════════════════════════════════════ */
    QToolTip {{
        background-color: {COLOR_INVERSE_SURFACE};
        color: {COLOR_INVERSE_ON_SURFACE};
        border: none;
        border-radius: {RADIUS_SM}px;
        padding: {SPACING_XS}px {SPACING_SM}px;
        font-size: {FONT_SIZE_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       SLIDER
       ══════════════════════════════════════════════════════════════════ */
    QSlider::groove:horizontal {{
        background: {COLOR_SURFACE_HIGH};
        height: 4px;
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {COLOR_PRIMARY};
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {COLOR_PRIMARY_CONTAINER};
    }}
    QSlider::sub-page:horizontal {{
        background: {COLOR_PRIMARY};
        border-radius: 2px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOAST NOTIFICATION
       ══════════════════════════════════════════════════════════════════ */
    #toast {{
        background-color: {COLOR_INVERSE_SURFACE};
        color: {COLOR_INVERSE_ON_SURFACE};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
    }}
    #toast[level="success"] {{
        background-color: {COLOR_SUCCESS};
        color: #ffffff;
    }}
    #toast[level="warning"] {{
        background-color: {COLOR_WARNING};
        color: #ffffff;
    }}
    #toast[level="error"] {{
        background-color: {COLOR_ERROR};
        color: {COLOR_ON_ERROR};
    }}
    """
```

---

## Dark QSS Template

```python
def get_dark_qss() -> str:
    """Retorna el stylesheet completo para el modo oscuro."""
    return f"""
    /* ══════════════════════════════════════════════════════════════════
       RESET GLOBAL — DARK MODE
       ══════════════════════════════════════════════════════════════════ */
    * {{
        margin: 0;
        padding: 0;
        font-family: {FONT_STACK};
        font-size: {FONT_SIZE_MD}px;
        color: {DARK_ON_SURFACE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       VENTANA PRINCIPAL Y DIÁLOGOS — DARK
       ══════════════════════════════════════════════════════════════════ */
    QMainWindow {{
        background-color: {DARK_BACKGROUND};
    }}

    QDialog {{
        background-color: {DARK_SURFACE_CONTAINER};
        border-radius: {RADIUS_LG}px;
    }}

    QWidget {{
        background-color: transparent;
    }}

    /* ══════════════════════════════════════════════════════════════════
       SCROLLBARS — DARK
       ══════════════════════════════════════════════════════════════════ */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {DARK_OUTLINE};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {DARK_ON_SURFACE_VARIANT};
    }}
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: none;
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {DARK_OUTLINE};
        border-radius: 3px;
        min-width: 30px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {DARK_ON_SURFACE_VARIANT};
    }}
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {{
        background: none;
        width: 0;
    }}

    /* ══════════════════════════════════════════════════════════════════
       BOTONES — DARK
       ══════════════════════════════════════════════════════════════════ */
    QPushButton {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 600;
        min-height: 20px;
    }}
    QPushButton:hover {{
        background-color: {DARK_SURFACE_HIGH};
        border-color: {DARK_OUTLINE};
    }}
    QPushButton:pressed {{
        background-color: {DARK_OUTLINE};
    }}
    QPushButton:disabled {{
        background-color: {DARK_SURFACE};
        color: {DARK_OUTLINE};
        border-color: {DARK_BORDER};
    }}

    QPushButton[class="primary"] {{
        background-color: {DARK_PRIMARY_CONTAINER};
        color: {DARK_PRIMARY};
        border: none;
    }}
    QPushButton[class="primary"]:hover {{
        background-color: #004db8;
    }}
    QPushButton[class="primary"]:pressed {{
        background-color: #00368c;
    }}
    QPushButton[class="primary"]:disabled {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_OUTLINE};
    }}

    QPushButton[class="ghost"] {{
        background-color: transparent;
        color: {DARK_PRIMARY};
        border: none;
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {DARK_SURFACE_CONTAINER};
    }}
    QPushButton[class="ghost"]:pressed {{
        background-color: {DARK_SURFACE_HIGH};
    }}

    QPushButton[class="danger"] {{
        background-color: #93000a;
        color: #ffdad6;
        border: none;
    }}
    QPushButton[class="danger"]:hover {{
        background-color: #a5000e;
    }}
    QPushButton[class="danger"]:pressed {{
        background-color: #7a0008;
    }}

    /* ══════════════════════════════════════════════════════════════════
       INPUTS — DARK
       ══════════════════════════════════════════════════════════════════ */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        selection-background-color: {DARK_PRIMARY_CONTAINER};
        selection-color: {DARK_PRIMARY};
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {DARK_PRIMARY};
        padding: {SPACING_SM - 1}px {SPACING_MD - 1}px;
    }}
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_OUTLINE};
    }}

    QSpinBox, QDoubleSpinBox {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
    }}
    QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {DARK_PRIMARY};
    }}
    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        background: transparent;
        border: none;
        width: 20px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {DARK_SURFACE_HIGH};
    }}

    QComboBox {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        min-height: 20px;
    }}
    QComboBox:focus {{
        border: 2px solid {DARK_PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_XS}px;
        selection-background-color: {DARK_SURFACE_HIGH};
        selection-color: {DARK_ON_SURFACE};
        outline: none;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TABLA — DARK
       ══════════════════════════════════════════════════════════════════ */
    QTableWidget, QTableView {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_MD}px;
        gridline-color: {DARK_BORDER};
        selection-background-color: {DARK_PRIMARY_CONTAINER};
        selection-color: {DARK_PRIMARY};
        alternate-background-color: {DARK_SURFACE_LOW};
        font-size: {FONT_SIZE_MD}px;
    }}
    QTableWidget::item, QTableView::item {{
        padding: {SPACING_SM}px {SPACING_MD}px;
        border-bottom: 1px solid {DARK_BORDER};
    }}
    QHeaderView::section {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE_VARIANT};
        border: none;
        border-bottom: 2px solid {DARK_BORDER};
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       GROUPBOX — DARK
       ══════════════════════════════════════════════════════════════════ */
    QGroupBox {{
        background-color: {DARK_SURFACE_CONTAINER};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_MD}px;
        margin-top: 16px;
        padding: {SPACING_MD}px;
        padding-top: 28px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 {SPACING_SM}px;
        color: {DARK_ON_SURFACE_VARIANT};
        font-size: {FONT_SIZE_SM}px;
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       LABELS — DARK
       ══════════════════════════════════════════════════════════════════ */
    QLabel {{
        color: {DARK_ON_SURFACE};
        background: transparent;
    }}
    QLabel[class="headline"] {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
    }}
    QLabel[class="title"] {{
        font-size: {FONT_SIZE_2XL}px;
        font-weight: 700;
    }}
    QLabel[class="subtitle"] {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 600;
    }}
    QLabel[class="body"] {{
        font-size: {FONT_SIZE_MD}px;
        font-weight: 400;
    }}
    QLabel[class="label"] {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 500;
        color: {DARK_ON_SURFACE_VARIANT};
    }}
    QLabel[class="caption"] {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 400;
        color: {DARK_OUTLINE};
    }}
    QLabel[class="hero"] {{
        font-size: {FONT_SIZE_3XL}px;
        font-weight: 700;
    }}

    /* ══════════════════════════════════════════════════════════════════
       SIDEBAR — DARK
       ══════════════════════════════════════════════════════════════════ */
    #sidebar {{
        background-color: {DARK_SURFACE};
        border-right: 1px solid {DARK_BORDER};
        min-width: {SIDEBAR_WIDTH}px;
        max-width: {SIDEBAR_WIDTH}px;
    }}

    #sidebarTitle {{
        font-size: {FONT_SIZE_LG}px;
        font-weight: 700;
        color: {DARK_PRIMARY};
        padding: {SPACING_MD}px;
    }}

    #sidebarNavItem {{
        background-color: transparent;
        color: {DARK_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        text-align: left;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        min-height: 36px;
    }}
    #sidebarNavItem:hover {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE};
    }}
    #sidebarNavItem[active="true"] {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_PRIMARY};
        font-weight: 600;
    }}

    #sidebarSection {{
        font-size: {FONT_SIZE_XS}px;
        font-weight: 600;
        color: {DARK_OUTLINE};
        padding: {SPACING_MD}px {SPACING_MD}px {SPACING_XS}px {SPACING_MD}px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       CARDS — DARK
       ══════════════════════════════════════════════════════════════════ */
    #card {{
        background-color: {DARK_SURFACE_CONTAINER};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_MD}px;
    }}
    #statValue {{
        font-size: {FONT_SIZE_3XL}px;
        font-weight: 700;
        color: {DARK_ON_SURFACE};
    }}
    #statLabel {{
        font-size: {FONT_SIZE_SM}px;
        font-weight: 500;
        color: {DARK_ON_SURFACE_VARIANT};
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOP BAR — DARK
       ══════════════════════════════════════════════════════════════════ */
    #topBar {{
        background-color: {DARK_SURFACE};
        border-bottom: 1px solid {DARK_BORDER};
        min-height: {TOPBAR_HEIGHT}px;
        max-height: {TOPBAR_HEIGHT}px;
        padding: 0 {SPACING_LG}px;
    }}
    #topBarTitle {{
        font-size: {FONT_SIZE_XL}px;
        font-weight: 700;
        color: {DARK_ON_SURFACE};
    }}

    /* ══════════════════════════════════════════════════════════════════
       STATUS BAR — DARK
       ══════════════════════════════════════════════════════════════════ */
    QStatusBar {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE_VARIANT};
        border-top: 1px solid {DARK_BORDER};
        font-size: {FONT_SIZE_XS}px;
        padding: {SPACING_XS}px {SPACING_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       MENU BAR Y MENÚS — DARK
       ══════════════════════════════════════════════════════════════════ */
    QMenuBar {{
        background-color: {DARK_SURFACE};
        color: {DARK_ON_SURFACE};
        border-bottom: 1px solid {DARK_BORDER};
        padding: {SPACING_XS}px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: {SPACING_XS}px {SPACING_SM}px;
        border-radius: {RADIUS_SM}px;
    }}
    QMenuBar::item:selected {{
        background-color: {DARK_SURFACE_HIGH};
    }}
    QMenu {{
        background-color: {DARK_SURFACE_CONTAINER};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_XS}px;
    }}
    QMenu::item {{
        padding: {SPACING_SM}px {SPACING_MD}px;
        border-radius: {RADIUS_SM}px;
    }}
    QMenu::item:selected {{
        background-color: {DARK_SURFACE_HIGH};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {DARK_BORDER};
        margin: {SPACING_XS}px {SPACING_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOOLBAR — DARK
       ══════════════════════════════════════════════════════════════════ */
    QToolBar {{
        background-color: {DARK_SURFACE};
        border-bottom: 1px solid {DARK_BORDER};
        padding: {SPACING_XS}px;
        spacing: {SPACING_XS}px;
    }}
    QToolButton {{
        background: transparent;
        color: {DARK_ON_SURFACE_VARIANT};
        border: none;
        border-radius: {RADIUS_SM}px;
        padding: {SPACING_SM}px;
    }}
    QToolButton:hover {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_ON_SURFACE};
    }}
    QToolButton:pressed {{
        background-color: {DARK_OUTLINE};
    }}
    QToolButton:checked {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_PRIMARY};
    }}

    /* ══════════════════════════════════════════════════════════════════
       PROGRESS BAR — DARK
       ══════════════════════════════════════════════════════════════════ */
    QProgressBar {{
        background-color: {DARK_SURFACE_HIGH};
        border: none;
        border-radius: {RADIUS_SM}px;
        height: 8px;
        text-align: center;
        font-size: 0px;
    }}
    QProgressBar::chunk {{
        background-color: {DARK_PRIMARY};
        border-radius: {RADIUS_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       CHECKBOX Y RADIO BUTTON — DARK
       ══════════════════════════════════════════════════════════════════ */
    QCheckBox {{
        spacing: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
        color: {DARK_ON_SURFACE};
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {DARK_OUTLINE};
        border-radius: {RADIUS_SM}px;
        background-color: {DARK_SURFACE};
    }}
    QCheckBox::indicator:hover {{
        border-color: {DARK_PRIMARY};
    }}
    QCheckBox::indicator:checked {{
        background-color: {DARK_PRIMARY_CONTAINER};
        border-color: {DARK_PRIMARY};
    }}

    QRadioButton {{
        spacing: {SPACING_SM}px;
        font-size: {FONT_SIZE_MD}px;
        color: {DARK_ON_SURFACE};
    }}
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {DARK_OUTLINE};
        border-radius: 9px;
        background-color: {DARK_SURFACE};
    }}
    QRadioButton::indicator:hover {{
        border-color: {DARK_PRIMARY};
    }}
    QRadioButton::indicator:checked {{
        background-color: {DARK_PRIMARY_CONTAINER};
        border-color: {DARK_PRIMARY};
    }}

    /* ══════════════════════════════════════════════════════════════════
       TAB WIDGET — DARK
       ══════════════════════════════════════════════════════════════════ */
    QTabWidget::pane {{
        background-color: {DARK_SURFACE_CONTAINER};
        border: 1px solid {DARK_BORDER};
        border-top: none;
        border-radius: 0 0 {RADIUS_MD}px {RADIUS_MD}px;
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {DARK_ON_SURFACE_VARIANT};
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        min-width: 80px;
    }}
    QTabBar::tab:hover {{
        color: {DARK_ON_SURFACE};
        background-color: {DARK_SURFACE_CONTAINER};
    }}
    QTabBar::tab:selected {{
        color: {DARK_PRIMARY};
        border-bottom: 2px solid {DARK_PRIMARY};
        font-weight: 600;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOOLTIP — DARK
       ══════════════════════════════════════════════════════════════════ */
    QToolTip {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_ON_SURFACE};
        border: 1px solid {DARK_BORDER};
        border-radius: {RADIUS_SM}px;
        padding: {SPACING_XS}px {SPACING_SM}px;
        font-size: {FONT_SIZE_SM}px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       SLIDER — DARK
       ══════════════════════════════════════════════════════════════════ */
    QSlider::groove:horizontal {{
        background: {DARK_SURFACE_HIGH};
        height: 4px;
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {DARK_PRIMARY};
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {DARK_PRIMARY_CONTAINER};
    }}
    QSlider::sub-page:horizontal {{
        background: {DARK_PRIMARY};
        border-radius: 2px;
    }}

    /* ══════════════════════════════════════════════════════════════════
       TOAST — DARK
       ══════════════════════════════════════════════════════════════════ */
    #toast {{
        background-color: {DARK_SURFACE_HIGH};
        color: {DARK_ON_SURFACE};
        border-radius: {RADIUS_DEFAULT}px;
        padding: {SPACING_SM}px {SPACING_MD}px;
        font-size: {FONT_SIZE_MD}px;
        font-weight: 500;
    }}
    """
```

---

## QSS Tips & Gotchas

### 1. Property Selectors

Use `setProperty()` in Python to apply QSS variant selectors:

```python
# En Python
button.setProperty("class", "primary")
button.style().unpolish(button)  # Forzar re-evaluación del estilo
button.style().polish(button)

# En QSS
QPushButton[class="primary"] { ... }
```

### 2. Object Name Selectors

Use `setObjectName()` for unique widget targeting:

```python
# En Python
sidebar.setObjectName("sidebar")

# En QSS — usa # para nombres de objeto
#sidebar { background-color: ...; }
```

### 3. Dynamic Properties for State

```python
# Cambiar estado activo en un item de navegación
nav_item.setProperty("active", "true")
nav_item.style().unpolish(nav_item)
nav_item.style().polish(nav_item)
```

### 4. F-String Escaping

When using Python f-strings for QSS, escape curly braces with double braces:

```python
qss = f"""
QPushButton {{
    background-color: {COLOR_PRIMARY};
    border-radius: {RADIUS_DEFAULT}px;
}}
"""
```

### 5. Force Style Refresh

After changing properties dynamically:

```python
def refresh_style(widget):
    """Fuerza la re-evaluación del QSS en un widget."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
```

### 6. QSS Limitations

- **No native `box-shadow`**: Use `QGraphicsDropShadowEffect` instead
- **No `transition` or `animation`**: Use `QPropertyAnimation`
- **No CSS variables**: Use Python f-string interpolation with tokens
- **No `calc()`**: Compute values in Python before interpolation
- **No pseudo-elements (`::before`, `::after`)**: Use child widgets
- **Limited `border-radius` on some widgets**: May need `border-style: solid`
