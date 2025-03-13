from tkinter import ttk
from typing import Dict, Any
import platform

# Verificar o sistema operacional
IS_WINDOWS = platform.system() == "Windows"

# Fontes seguras para Windows e Mac
if IS_WINDOWS:
    DEFAULT_FONT = "Segoe UI"
    HEADER_FONT = "Segoe UI"
else:
    DEFAULT_FONT = "Inter"
    HEADER_FONT = "Inter"

DESIGN_SYSTEM: Dict[str, Any] = {
    "colors": {
        "primary": "#3B82F6",  # Azul mais vibrante
        "secondary": "#6366F1",  # Indigo
        "background": {
            "default": "#0F172A",  # Azul escuro profundo
            "paper": "#1E293B",  # Azul escuro mais claro
            "card": "#1E293B",  # Fundo dos cards
            "button": "#334155",  # Fundo dos botões (mais escuro)
            "hover": "#475569",  # Cor de hover
        },
        "error": "#EF4444",  # Vermelho
        "success": "#10B981",  # Verde esmeralda
        "warning": "#F59E0B",  # Âmbar
        "border": "#475569",  # Cinza azulado
        "text": {
            "primary": "#F8FAFC",  # Branco com tom azulado
            "secondary": "#94A3B8",  # Cinza azulado claro
            "disabled": "#64748B",  # Cinza azulado médio
        },
    },
    "spacing": {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32},
    "typography": {
        "h1": (HEADER_FONT, 24, "bold"),
        "h2": (HEADER_FONT, 20, "bold"),
        "h3": (HEADER_FONT, 18, "bold"),
        "body1": (DEFAULT_FONT, 14, "normal"),
        "body2": (DEFAULT_FONT, 12, "normal"),
        "button": (DEFAULT_FONT, 14, "bold"),
    },
    "border_radius": {"sm": 4, "md": 8, "lg": 12},
}


def setup_styles() -> None:
    """Configura os estilos do ttk com base no design system."""
    style = ttk.Style()

    # Configurar tema escuro
    style.configure(
        "Card.TFrame",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    # Configurar estilo do separador
    style.configure(
        "Separator.TFrame",
        background=DESIGN_SYSTEM["colors"]["border"],
    )

    # Configurar estilo dos labels
    style.configure(
        "Header.TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["h1"],
    )

    style.configure(
        "SubHeader.TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["h2"],
    )

    style.configure(
        "Default.TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["body1"],
    )

    # Configurar estilo dos botões
    style.configure(
        "Primary.TButton",
        background=DESIGN_SYSTEM["colors"]["primary"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["button"],
    )

    style.configure(
        "Secondary.TButton",
        background=DESIGN_SYSTEM["colors"]["secondary"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["button"],
    )

    style.configure(
        "Error.TButton",
        background=DESIGN_SYSTEM["colors"]["error"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["button"],
    )

    # Configurar estilo geral
    style.configure(
        ".",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["body1"],
        borderwidth=0,
    )

    # Estilo para frames
    style.configure(
        "Card.TFrame",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        borderwidth=0,
        relief="flat",
    )

    # Estilo para labels
    style.configure(
        "TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["body1"],
    )

    # Estilo para combobox
    style.configure(
        "TCombobox",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        borderwidth=1,
        relief="solid",
        arrowcolor=DESIGN_SYSTEM["colors"]["primary"],
    )

    # Mapear estados do combobox
    style.map(
        "TCombobox",
        fieldbackground=[
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["paper"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["default"]),
        ],
        foreground=[
            ("readonly", DESIGN_SYSTEM["colors"]["text"]["primary"]),
            ("disabled", DESIGN_SYSTEM["colors"]["text"]["disabled"]),
        ],
    )

    # Estilo para entry
    style.configure(
        "TEntry",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        selectbackground=DESIGN_SYSTEM["colors"]["primary"],
        selectforeground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        borderwidth=1,
        relief="solid",
    )

    # Mapear estados do entry
    style.map(
        "TEntry",
        background=[
            ("active", DESIGN_SYSTEM["colors"]["background"]["paper"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["default"]),
        ],
        fieldbackground=[
            ("active", DESIGN_SYSTEM["colors"]["background"]["paper"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["default"]),
        ],
        foreground=[
            ("disabled", DESIGN_SYSTEM["colors"]["text"]["disabled"]),
        ],
    )

    # Estilo para treeview
    style.configure(
        "Treeview",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        font=DESIGN_SYSTEM["typography"]["body1"],
        borderwidth=0,
        rowheight=30,  # Altura das linhas
    )

    style.configure(
        "Treeview.Heading",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["button"],
        relief="flat",
        borderwidth=0,
        padding=5,
    )

    # Mapear estados do treeview
    style.map(
        "Treeview",
        background=[
            ("selected", DESIGN_SYSTEM["colors"]["primary"]),
            ("alternate", DESIGN_SYSTEM["colors"]["background"]["default"]),
        ],
        foreground=[
            ("selected", DESIGN_SYSTEM["colors"]["text"]["primary"]),
        ],
    )

    style.map(
        "Treeview.Heading",
        background=[
            ("active", DESIGN_SYSTEM["colors"]["primary"]),
            ("pressed", DESIGN_SYSTEM["colors"]["primary"]),
        ],
        foreground=[
            ("active", DESIGN_SYSTEM["colors"]["text"]["primary"]),
            ("pressed", DESIGN_SYSTEM["colors"]["text"]["primary"]),
        ],
    )

    # Configurar estilo do campo de busca
    style.configure(
        "Search.TEntry",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        borderwidth=1,
        relief="solid",
        padding=8,
    )

    style.map(
        "Search.TEntry",
        fieldbackground=[
            ("focus", DESIGN_SYSTEM["colors"]["background"]["paper"]),
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["paper"]),
        ],
        foreground=[
            ("focus", DESIGN_SYSTEM["colors"]["text"]["primary"]),
        ],
    )

    # Estilo para Scrollbar
    style.configure(
        "TScrollbar",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        troughcolor=DESIGN_SYSTEM["colors"]["background"]["paper"],
        borderwidth=0,
        relief="flat",
        arrowcolor=DESIGN_SYSTEM["colors"]["text"]["primary"],
    )

    # Estilo para Notebook (abas)
    style.configure(
        "TNotebook",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        borderwidth=0,
    )

    style.configure(
        "TNotebook.Tab",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        padding=[10, 5],
        borderwidth=0,
    )

    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", DESIGN_SYSTEM["colors"]["primary"]),
            ("active", DESIGN_SYSTEM["colors"]["background"]["hover"]),
        ],
        foreground=[
            ("selected", DESIGN_SYSTEM["colors"]["text"]["primary"]),
            ("active", DESIGN_SYSTEM["colors"]["text"]["primary"]),
        ],
    )


def get_button_style(variant: str = "primary") -> Dict[str, Any]:
    """
    Retorna o estilo para botões baseado na variante.

    Args:
        variant: Tipo do botão ('primary', 'secondary', 'error', 'success')
    """
    colors = {
        "primary": {
            "default": DESIGN_SYSTEM["colors"]["primary"],
            "hover": "#2563EB",  # Azul mais escuro
            "text": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "secondary": {
            "default": DESIGN_SYSTEM["colors"]["secondary"],
            "hover": "#4F46E5",  # Indigo mais escuro
            "text": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "error": {
            "default": DESIGN_SYSTEM["colors"]["error"],
            "hover": "#DC2626",  # Vermelho mais escuro
            "text": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "success": {
            "default": DESIGN_SYSTEM["colors"]["success"],
            "hover": "#059669",  # Verde mais escuro
            "text": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "warning": {
            "default": DESIGN_SYSTEM["colors"]["warning"],
            "hover": "#D97706",  # Âmbar mais escuro
            "text": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "text": {
            "default": "transparent",
            "hover": DESIGN_SYSTEM["colors"]["background"]["hover"],
            "text": DESIGN_SYSTEM["colors"]["primary"],
        },
    }

    return colors.get(variant, colors["primary"])
