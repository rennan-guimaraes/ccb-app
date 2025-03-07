from tkinter import ttk
from typing import Dict, Any

DESIGN_SYSTEM: Dict[str, Any] = {
    "colors": {
        "primary": "#1976D2",
        "secondary": "#424242",
        "background": {
            "default": "#121212",  # Fundo escuro principal
            "paper": "#1E1E1E",  # Superfícies e cards
        },
        "error": "#CF6679",
        "success": "#4CAF50",
        "warning": "#FB8C00",
        "border": "#323232",
        "text": {
            "primary": "#FFFFFF",  # Texto principal branco
            "secondary": "#B3B3B3",  # Texto secundário cinza claro
            "disabled": "#666666",  # Texto desabilitado
        },
    },
    "spacing": {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32},
    "typography": {
        "h1": ("Helvetica", 24, "bold"),
        "h2": ("Helvetica", 20, "bold"),
        "h3": ("Helvetica", 18, "bold"),
        "body1": ("Helvetica", 14, "normal"),
        "body2": ("Helvetica", 12, "normal"),
        "button": ("Helvetica", 14, "bold"),
    },
    "border_radius": {"sm": 4, "md": 8, "lg": 12},
}


def setup_styles() -> None:
    """Configura os estilos do ttk com base no design system."""
    style = ttk.Style()

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
        borderwidth=1,
        relief="solid",
    )

    # Estilo para labels
    style.configure(
        "TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        font=DESIGN_SYSTEM["typography"]["body1"],
    )

    # Estilo para headers
    style.configure(
        "Header.TLabel",
        font=DESIGN_SYSTEM["typography"]["h1"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    # Estilo para sub-headers
    style.configure(
        "SubHeader.TLabel",
        font=DESIGN_SYSTEM["typography"]["h2"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["secondary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
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


def get_button_style(variant: str = "primary") -> Dict[str, Any]:
    """
    Retorna o estilo para botões baseado na variante.

    Args:
        variant: Tipo do botão ('primary', 'secondary', 'error', 'success')
    """
    styles = {
        "primary": {
            "bg": DESIGN_SYSTEM["colors"]["primary"],
            "fg": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "secondary": {
            "bg": DESIGN_SYSTEM["colors"]["secondary"],
            "fg": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "error": {
            "bg": DESIGN_SYSTEM["colors"]["error"],
            "fg": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
        "success": {
            "bg": DESIGN_SYSTEM["colors"]["success"],
            "fg": DESIGN_SYSTEM["colors"]["text"]["primary"],
        },
    }

    return styles.get(variant, styles["primary"])
