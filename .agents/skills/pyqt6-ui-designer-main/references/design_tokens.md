# Design Tokens — PyQt6 Modern Enterprise Design System

> Canonical reference for all design token values. Every color, spacing, font, radius,
> and shadow value used across the system is defined here. **Never hard-code values in
> QSS or Python — always import or reference these tokens.**

---

## Color Palette — Light Mode

### Surfaces

```python
# ── Superficies (Light Mode) ──────────────────────────────────────────────
COLOR_SURFACE              = "#faf9ff"   # Fondo principal de la aplicación
COLOR_SURFACE_DIM          = "#ccdaff"   # Superficie atenuada (fondos secundarios)
COLOR_SURFACE_BRIGHT       = "#faf9ff"   # Superficie más brillante
COLOR_SURFACE_LOWEST       = "#ffffff"   # Superficie base (tarjetas, diálogos)
COLOR_SURFACE_LOW          = "#f1f3ff"   # Superficie baja (filas alternas en tablas)
COLOR_SURFACE_HIGH         = "#e1e8ff"   # Superficie elevada (hover sobre superficies)
COLOR_SURFACE_HIGHEST      = "#d8e2ff"   # Superficie más elevada (estados activos)
COLOR_BACKGROUND           = "#faf9ff"   # Fondo de la ventana principal
COLOR_SURFACE_VARIANT      = "#d8e2ff"   # Variante de superficie (chips, badges)
```

### Content / On-Surface

```python
# ── Contenido sobre superficies ───────────────────────────────────────────
COLOR_ON_SURFACE           = "#051a3e"   # Texto principal (alto contraste)
COLOR_ON_SURFACE_VARIANT   = "#434654"   # Texto secundario (subtítulos, captions)
COLOR_OUTLINE              = "#737685"   # Bordes de inputs, separadores
COLOR_OUTLINE_VARIANT      = "#c3c6d6"   # Bordes sutiles (dividers, table borders)
```

### Primary Brand (Corporate Blue)

```python
# ── Color primario (Azul corporativo) ─────────────────────────────────────
COLOR_PRIMARY              = "#003d9b"   # Botones primarios, enlaces, iconos activos
COLOR_ON_PRIMARY           = "#ffffff"   # Texto sobre fondo primario
COLOR_PRIMARY_CONTAINER    = "#0052cc"   # Contenedor primario (badges, selección)
COLOR_ON_PRIMARY_CONTAINER = "#c4d2ff"   # Texto sobre contenedor primario
COLOR_INVERSE_PRIMARY      = "#b2c5ff"   # Color primario en modo inverso
COLOR_SURFACE_TINT         = "#0c56d0"   # Tinte de superficie (hover/focus rings)
```

### Secondary

```python
# ── Color secundario ─────────────────────────────────────────────────────
COLOR_SECONDARY            = "#535f73"   # Botones secundarios, texto auxiliar
COLOR_ON_SECONDARY         = "#ffffff"   # Texto sobre fondo secundario
COLOR_SECONDARY_CONTAINER  = "#d4e0f8"   # Contenedor secundario (tags, filtros)
```

### Tertiary (Warm Accent)

```python
# ── Color terciario (Acento cálido) ──────────────────────────────────────
COLOR_TERTIARY             = "#7b2600"   # Acento cálido para énfasis
COLOR_ON_TERTIARY          = "#ffffff"   # Texto sobre fondo terciario
COLOR_TERTIARY_CONTAINER   = "#a33500"   # Contenedor terciario
```

### Error

```python
# ── Color de error ────────────────────────────────────────────────────────
COLOR_ERROR                = "#ba1a1a"   # Borde de error, iconos de alerta
COLOR_ON_ERROR             = "#ffffff"   # Texto sobre fondo de error
COLOR_ERROR_CONTAINER      = "#ffdad6"   # Fondo de banner de error
COLOR_ON_ERROR_CONTAINER   = "#93000a"   # Texto dentro de contenedor de error
```

### Inverse

```python
# ── Colores inversos (tooltips, snackbars) ────────────────────────────────
COLOR_INVERSE_SURFACE      = "#1d3054"   # Fondo de tooltips / snackbars
COLOR_INVERSE_ON_SURFACE   = "#edf0ff"   # Texto en superficies inversas
```

---

## Color Palette — Dark Mode

```python
# ══════════════════════════════════════════════════════════════════════════
# MODO OSCURO
# ══════════════════════════════════════════════════════════════════════════

DARK_BACKGROUND            = "#0B121F"   # Fondo principal (ventana)
DARK_SURFACE               = "#161C27"   # Superficie base (similar a surface)
DARK_SURFACE_CONTAINER     = "#1E2738"   # Contenedores (tarjetas, sidebar)
DARK_SURFACE_HIGH          = "#252D3D"   # Superficie elevada (hover, selección)
DARK_BORDER                = "#252D3D"   # Bordes generales
DARK_ON_SURFACE            = "#edf0ff"   # Texto principal
DARK_ON_SURFACE_VARIANT    = "#9ca3b8"   # Texto secundario
DARK_OUTLINE               = "#3d4560"   # Bordes de inputs, separadores
DARK_PRIMARY               = "#b2c5ff"   # Color primario (texto/iconos primarios)
DARK_PRIMARY_CONTAINER     = "#0040a2"   # Contenedores primarios (botón primario)
```

### Dark Mode — Extended Tokens (Derived)

```python
# ── Tokens derivados para modo oscuro ─────────────────────────────────────
DARK_SURFACE_LOW           = "#131924"   # Filas alternas en tablas
DARK_SURFACE_LOWEST        = "#0E1520"   # Diálogos, modales
DARK_ERROR                 = "#ffb4ab"   # Texto/icono de error en dark
DARK_ERROR_CONTAINER       = "#93000a"   # Fondo de contenedor de error en dark
DARK_ON_ERROR              = "#690005"   # Texto sobre error container dark
DARK_SUCCESS               = "#6dd58c"   # Texto/icono de éxito en dark
DARK_WARNING               = "#fbbf24"   # Texto/icono de advertencia en dark
DARK_INFO                  = "#93b4ff"   # Texto/icono informativo en dark
```

---

## Semantic Colors

```python
# ══════════════════════════════════════════════════════════════════════════
# COLORES SEMÁNTICOS (ambos modos comparten las mismas bases light)
# ══════════════════════════════════════════════════════════════════════════

COLOR_SUCCESS              = "#1a7d37"   # Éxito — texto, iconos, bordes
COLOR_SUCCESS_CONTAINER    = "#d4edda"   # Éxito — fondo de contenedor
COLOR_WARNING              = "#b45309"   # Advertencia — texto, iconos, bordes
COLOR_WARNING_CONTAINER    = "#fff3cd"   # Advertencia — fondo de contenedor
COLOR_INFO                 = "#0c56d0"   # Información — texto, iconos, bordes
COLOR_INFO_CONTAINER       = "#cce5ff"   # Información — fondo de contenedor
```

---

## Spacing System (4px Grid)

All spacing values are multiples of 4px for consistent visual rhythm.

```python
# ══════════════════════════════════════════════════════════════════════════
# ESPACIADO (Sistema de 4px)
# ══════════════════════════════════════════════════════════════════════════

SPACING_2XS = 2    # Micro gaps (solo para bordes o ajustes de 1-2px)
SPACING_XS  = 4    # Gaps ajustados, padding de iconos
SPACING_SM  = 8    # Padding interno por defecto, gap entre elementos inline
SPACING_MD  = 16   # Padding de secciones, márgenes de tarjetas
SPACING_LG  = 24   # Márgenes de página, gaps grandes
SPACING_XL  = 32   # Secciones hero, separaciones amplias
SPACING_2XL = 48   # Divisiones principales del layout
```

### Usage Guidelines

| Token        | Use for                                              |
|--------------|------------------------------------------------------|
| `SPACING_XS` | Icon-to-text gap, compact list item padding          |
| `SPACING_SM` | Default inner padding, form field gaps               |
| `SPACING_MD` | Card padding, section vertical spacing               |
| `SPACING_LG` | Page margins, content area padding                   |
| `SPACING_XL` | Hero section padding, major content gaps             |
| `SPACING_2XL`| Layout division gaps (sidebar ↔ content)             |

---

## Typography

```python
# ══════════════════════════════════════════════════════════════════════════
# TIPOGRAFÍA
# ══════════════════════════════════════════════════════════════════════════

# Familias de fuentes
FONT_BODY     = "Inter"            # Fuente principal para todo el texto
FONT_FALLBACK = "Segoe UI"        # Fallback para Windows
FONT_MONO     = "JetBrains Mono"  # Código, datos tabulares monoespaciados

# Pila de fuentes completa para QSS
FONT_STACK      = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_MONO_STACK = '"JetBrains Mono", "Cascadia Code", "Consolas", monospace'

# Tamaños de fuente (px)
FONT_SIZE_XS  = 11   # Captions, badges, micro texto
FONT_SIZE_SM  = 12   # Labels de formularios, texto auxiliar
FONT_SIZE_MD  = 14   # Cuerpo del texto (tamaño por defecto)
FONT_SIZE_LG  = 16   # Subtítulos, texto destacado
FONT_SIZE_XL  = 20   # Títulos de sección
FONT_SIZE_2XL = 24   # Títulos de página
FONT_SIZE_3XL = 32   # Encabezados hero / dashboard

# Pesos de fuente
FONT_WEIGHT_REGULAR  = 400   # Texto normal
FONT_WEIGHT_MEDIUM   = 500   # Labels, navegación
FONT_WEIGHT_SEMIBOLD = 600   # Subtítulos, botones
FONT_WEIGHT_BOLD     = 700   # Títulos, énfasis fuerte

# Altura de línea (multiplicador)
LINE_HEIGHT_TIGHT    = 1.2    # Títulos, encabezados
LINE_HEIGHT_NORMAL   = 1.5    # Texto body
LINE_HEIGHT_RELAXED  = 1.75   # Párrafos extensos
```

### Typography Scale Quick Reference

| Style       | Size   | Weight   | Use                           |
|-------------|--------|----------|-------------------------------|
| `caption`   | 11px   | 400      | Metadata, timestamps, badges  |
| `label`     | 12px   | 500      | Form labels, nav items        |
| `body`      | 14px   | 400      | Default text                  |
| `subtitle`  | 16px   | 600      | Card titles, subsections      |
| `headline`  | 20px   | 700      | Section titles                |
| `title`     | 24px   | 700      | Page titles                   |
| `hero`      | 32px   | 700      | Dashboard hero values         |

---

## Border Radius

```python
# ══════════════════════════════════════════════════════════════════════════
# BORDES REDONDEADOS
# ══════════════════════════════════════════════════════════════════════════

RADIUS_SM      = 4      # Botones pequeños, badges, chips
RADIUS_DEFAULT = 8      # Inputs, botones estándar, dropdowns
RADIUS_MD      = 12     # Tarjetas, contenedores
RADIUS_LG      = 16     # Modales, diálogos, tarjetas grandes
RADIUS_FULL    = 9999   # Píldora (pill), avatares circulares
```

---

## Shadows

Shadows are applied via `QGraphicsDropShadowEffect` in Python. QSS does not
support native `box-shadow`, so shadows must be set programmatically.

```python
# ══════════════════════════════════════════════════════════════════════════
# SOMBRAS (parámetros para QGraphicsDropShadowEffect)
# ══════════════════════════════════════════════════════════════════════════

# Cada tupla contiene: (blur_radius, x_offset, y_offset, color_rgba)
SHADOW_SM = {
    "blur_radius": 4,
    "x_offset":    0,
    "y_offset":    2,
    "color":       (0, 0, 0, 25),   # rgba — alpha 25/255 ≈ 10% opacidad
}

SHADOW_MD = {
    "blur_radius": 12,
    "x_offset":    0,
    "y_offset":    4,
    "color":       (0, 0, 0, 40),   # rgba — alpha 40/255 ≈ 16% opacidad
}

SHADOW_LG = {
    "blur_radius": 24,
    "x_offset":    0,
    "y_offset":    8,
    "color":       (0, 0, 0, 60),   # rgba — alpha 60/255 ≈ 24% opacidad
}

SHADOW_XL = {
    "blur_radius": 40,
    "x_offset":    0,
    "y_offset":    16,
    "color":       (0, 0, 0, 80),   # rgba — alpha 80/255 ≈ 31% opacidad
}
```

### Shadow Helper Function

```python
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

def apply_shadow(widget, shadow_def):
    """Aplica una sombra a un widget usando los tokens definidos."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(shadow_def["blur_radius"])
    effect.setXOffset(shadow_def["x_offset"])
    effect.setYOffset(shadow_def["y_offset"])
    r, g, b, a = shadow_def["color"]
    effect.setColor(QColor(r, g, b, a))
    widget.setGraphicsEffect(effect)
```

---

## Layout Dimensions

```python
# ══════════════════════════════════════════════════════════════════════════
# DIMENSIONES DE LAYOUT
# ══════════════════════════════════════════════════════════════════════════

SIDEBAR_WIDTH       = 240   # Ancho fijo del sidebar
SIDEBAR_COLLAPSED   = 64    # Ancho del sidebar colapsado (solo iconos)
TOPBAR_HEIGHT       = 64    # Altura de la barra superior
STATUSBAR_HEIGHT    = 28    # Altura de la barra de estado
MIN_WINDOW_WIDTH    = 1024  # Ancho mínimo de la ventana
MIN_WINDOW_HEIGHT   = 640   # Alto mínimo de la ventana
CARD_MIN_WIDTH      = 200   # Ancho mínimo de tarjetas
TABLE_ROW_HEIGHT    = 44    # Altura de filas en tablas
ICON_SIZE_SM        = 16    # Iconos pequeños (inline, badges)
ICON_SIZE_MD        = 20    # Iconos estándar (navegación, botones)
ICON_SIZE_LG        = 24    # Iconos grandes (sidebar, acciones principales)
ICON_SIZE_XL        = 32    # Iconos hero, ilustraciones pequeñas
```

---

## Z-Index Layers

```python
# ══════════════════════════════════════════════════════════════════════════
# CAPAS Z-INDEX (para QWidget.raise_() y stacking order)
# ══════════════════════════════════════════════════════════════════════════

Z_BASE       = 0      # Contenido principal
Z_STICKY     = 10     # Headers fijos, barras superiores
Z_DROPDOWN   = 100    # Menús desplegables, combobox popups
Z_MODAL      = 200    # Diálogos modales, overlays
Z_TOAST      = 300    # Notificaciones toast
Z_TOOLTIP    = 400    # Tooltips
```

---

## Transition / Animation Durations

```python
# ══════════════════════════════════════════════════════════════════════════
# DURACIONES DE ANIMACIÓN (ms)
# ══════════════════════════════════════════════════════════════════════════

DURATION_FAST    = 100   # Hovers, cambios de estado rápidos
DURATION_NORMAL  = 200   # Transiciones estándar (sidebar, expansiones)
DURATION_SLOW    = 350   # Modales, overlays, animaciones complejas
DURATION_TOAST   = 3000  # Duración visible de notificaciones toast
```

---

## Complete Token Export

Copy this block into any generated Python file as the canonical token source:

```python
# ══════════════════════════════════════════════════════════════════════════
# DESIGN TOKENS — PyQt6 Modern Enterprise Design System
# Copiar este bloque completo al inicio de cada archivo de UI generado.
# ══════════════════════════════════════════════════════════════════════════

# ── Light Mode Surfaces ──
COLOR_SURFACE              = "#faf9ff"
COLOR_SURFACE_DIM          = "#ccdaff"
COLOR_SURFACE_BRIGHT       = "#faf9ff"
COLOR_SURFACE_LOWEST       = "#ffffff"
COLOR_SURFACE_LOW          = "#f1f3ff"
COLOR_SURFACE_HIGH         = "#e1e8ff"
COLOR_SURFACE_HIGHEST      = "#d8e2ff"
COLOR_BACKGROUND           = "#faf9ff"
COLOR_SURFACE_VARIANT      = "#d8e2ff"

# ── Content ──
COLOR_ON_SURFACE           = "#051a3e"
COLOR_ON_SURFACE_VARIANT   = "#434654"
COLOR_OUTLINE              = "#737685"
COLOR_OUTLINE_VARIANT      = "#c3c6d6"

# ── Primary ──
COLOR_PRIMARY              = "#003d9b"
COLOR_ON_PRIMARY           = "#ffffff"
COLOR_PRIMARY_CONTAINER    = "#0052cc"
COLOR_ON_PRIMARY_CONTAINER = "#c4d2ff"
COLOR_INVERSE_PRIMARY      = "#b2c5ff"
COLOR_SURFACE_TINT         = "#0c56d0"

# ── Secondary ──
COLOR_SECONDARY            = "#535f73"
COLOR_ON_SECONDARY         = "#ffffff"
COLOR_SECONDARY_CONTAINER  = "#d4e0f8"

# ── Tertiary ──
COLOR_TERTIARY             = "#7b2600"
COLOR_ON_TERTIARY          = "#ffffff"
COLOR_TERTIARY_CONTAINER   = "#a33500"

# ── Error ──
COLOR_ERROR                = "#ba1a1a"
COLOR_ON_ERROR             = "#ffffff"
COLOR_ERROR_CONTAINER      = "#ffdad6"
COLOR_ON_ERROR_CONTAINER   = "#93000a"

# ── Inverse ──
COLOR_INVERSE_SURFACE      = "#1d3054"
COLOR_INVERSE_ON_SURFACE   = "#edf0ff"

# ── Dark Mode ──
DARK_BACKGROUND            = "#0B121F"
DARK_SURFACE               = "#161C27"
DARK_SURFACE_CONTAINER     = "#1E2738"
DARK_SURFACE_HIGH          = "#252D3D"
DARK_BORDER                = "#252D3D"
DARK_ON_SURFACE            = "#edf0ff"
DARK_ON_SURFACE_VARIANT    = "#9ca3b8"
DARK_OUTLINE               = "#3d4560"
DARK_PRIMARY               = "#b2c5ff"
DARK_PRIMARY_CONTAINER     = "#0040a2"
DARK_SURFACE_LOW           = "#131924"
DARK_SURFACE_LOWEST        = "#0E1520"

# ── Semantic ──
COLOR_SUCCESS              = "#1a7d37"
COLOR_SUCCESS_CONTAINER    = "#d4edda"
COLOR_WARNING              = "#b45309"
COLOR_WARNING_CONTAINER    = "#fff3cd"
COLOR_INFO                 = "#0c56d0"
COLOR_INFO_CONTAINER       = "#cce5ff"

# ── Spacing (4px grid) ──
SPACING_XS  = 4
SPACING_SM  = 8
SPACING_MD  = 16
SPACING_LG  = 24
SPACING_XL  = 32
SPACING_2XL = 48

# ── Typography ──
FONT_BODY     = "Inter"
FONT_MONO     = "JetBrains Mono"
FONT_STACK    = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_SIZE_XS  = 11
FONT_SIZE_SM  = 12
FONT_SIZE_MD  = 14
FONT_SIZE_LG  = 16
FONT_SIZE_XL  = 20
FONT_SIZE_2XL = 24
FONT_SIZE_3XL = 32

# ── Radius ──
RADIUS_SM      = 4
RADIUS_DEFAULT = 8
RADIUS_MD      = 12
RADIUS_LG      = 16
RADIUS_FULL    = 9999

# ── Layout ──
SIDEBAR_WIDTH    = 240
TOPBAR_HEIGHT    = 64
TABLE_ROW_HEIGHT = 44
```
