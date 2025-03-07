from tkinter import ttk


def setup_styles():
    style = ttk.Style()

    # Sistema de Design - Tema Escuro
    DESIGN_SYSTEM = {
        "colors": {
            # Cores principais
            "primary": "#4CAF50",  # Verde mais vibrante
            "primary_light": "#81C784",
            "primary_dark": "#388E3C",
            "secondary": "#2196F3",  # Azul mais vibrante
            "secondary_light": "#64B5F6",
            "secondary_dark": "#1976D2",
            # Cores de background
            "background": "#121212",  # Fundo principal mais escuro
            "surface": "#1E1E1E",  # Superfícies (cards, sidebars)
            "surface_light": "#2C2C2C",  # Superfícies mais claras
            "surface_dark": "#171717",  # Superfícies mais escuras
            # Texto e ícones
            "text": {
                "primary": "#FFFFFF",  # Texto principal
                "secondary": "#B3B3B3",  # Texto secundário
                "disabled": "#757575",  # Texto desabilitado
                "hint": "#9E9E9E",  # Texto de dica
            },
            # Borda
            "border": "#2D2D2D",
            # Estados
            "states": {"hover": "#3C3C3C", "active": "#323232", "selected": "#0A84FF"},
            # Feedback
            "error": "#CF6679",  # Vermelho menos agressivo
            "warning": "#FFB74D",  # Laranja suave
            "success": "#81C784",  # Verde suave
            "info": "#64B5F6",  # Azul suave
        },
        "typography": {
            "h1": ("Helvetica", 32, "bold"),
            "h2": ("Helvetica", 24, "bold"),
            "h3": ("Helvetica", 20, "bold"),
            "subtitle1": ("Helvetica", 16, "bold"),
            "subtitle2": ("Helvetica", 14, "bold"),
            "body1": ("Helvetica", 14, "normal"),
            "body2": ("Helvetica", 12, "normal"),
            "button": ("Helvetica", 16, "bold"),
            "caption": ("Helvetica", 11, "normal"),
            "overline": ("Helvetica", 10, "normal"),
        },
        "spacing": {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32, "xxl": 48},
        "elevation": {
            "0": "flat",
            "1": "solid",
            "2": "raised",
            "3": "sunken",
            "4": "ridge",
        },
    }

    # Configuração do tema geral
    style.configure(".", background=DESIGN_SYSTEM["colors"]["background"])

    # Estilos de texto
    style.configure(
        "Header.TLabel",
        font=DESIGN_SYSTEM["typography"]["h1"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        background=DESIGN_SYSTEM["colors"]["background"],
        padding=DESIGN_SYSTEM["spacing"]["lg"],
    )

    style.configure(
        "SubHeader.TLabel",
        font=DESIGN_SYSTEM["typography"]["subtitle1"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["secondary"],
        background=DESIGN_SYSTEM["colors"]["background"],
        padding=DESIGN_SYSTEM["spacing"]["md"],
    )

    style.configure(
        "Caption.TLabel",
        font=DESIGN_SYSTEM["typography"]["caption"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["hint"],
        background=DESIGN_SYSTEM["colors"]["surface"],
        padding=DESIGN_SYSTEM["spacing"]["xs"],
    )

    # Frames
    style.configure(
        "Card.TFrame",
        background=DESIGN_SYSTEM["colors"]["surface"],
        relief="flat",
        borderwidth=0,
    )

    style.configure(
        "Background.TFrame",
        background=DESIGN_SYSTEM["colors"]["background"],
        relief="flat",
    )

    style.configure(
        "Sidebar.TFrame",
        background=DESIGN_SYSTEM["colors"]["surface_dark"],
        relief="flat",
        borderwidth=0,
    )

    # Combobox com borda personalizada
    style.configure(
        "Custom.TCombobox",
        background=DESIGN_SYSTEM["colors"]["surface"],
        fieldbackground=DESIGN_SYSTEM["colors"]["surface"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        arrowcolor=DESIGN_SYSTEM["colors"]["text"]["primary"],
        relief="flat",
        borderwidth=0,
        padding=DESIGN_SYSTEM["spacing"]["sm"],
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[
            ("readonly", DESIGN_SYSTEM["colors"]["surface"]),
            ("active", DESIGN_SYSTEM["colors"]["surface_light"]),
        ],
        selectbackground=[("readonly", DESIGN_SYSTEM["colors"]["states"]["selected"])],
        selectforeground=[("readonly", DESIGN_SYSTEM["colors"]["text"]["primary"])],
    )

    return DESIGN_SYSTEM
