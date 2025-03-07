import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

DESIGN_SYSTEM = {
    "colors": {
        "primary": "#2196F3",
        "secondary": "#757575",
        "error": "#F44336",
        "success": "#4CAF50",
        "background": {
            "default": "#FFFFFF",
            "paper": "#F5F5F5",
        },
        "text": {
            "primary": "#212121",
            "secondary": "#757575",
        },
    },
    "typography": {
        "h1": ("Helvetica", 24, "bold"),
        "h2": ("Helvetica", 20, "bold"),
        "h3": ("Helvetica", 18, "bold"),
        "body1": ("Helvetica", 14),
        "body2": ("Helvetica", 12),
        "button": ("Helvetica", 12, "bold"),
    },
    "spacing": {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
    },
}


def setup_styles(root: tk.Tk):
    """Configura os estilos TTK para a aplicação."""
    style = ttk.Style(root)

    # Configuração base
    style.configure(
        "TFrame", background=DESIGN_SYSTEM["colors"]["background"]["default"]
    )

    # Estilo para cards
    style.configure(
        "Card.TFrame",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        relief="raised",
        borderwidth=1,
    )

    # Estilos de texto
    style.configure(
        "Header.TLabel",
        font=DESIGN_SYSTEM["typography"]["h2"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "SubHeader.TLabel",
        font=DESIGN_SYSTEM["typography"]["h3"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "Body.TLabel",
        font=DESIGN_SYSTEM["typography"]["body1"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "Feedback.TLabel",
        font=DESIGN_SYSTEM["typography"]["body2"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["secondary"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "Success.TLabel",
        font=DESIGN_SYSTEM["typography"]["body2"],
        foreground=DESIGN_SYSTEM["colors"]["success"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    # Estilos de botões
    button_base = {
        "font": DESIGN_SYSTEM["typography"]["button"],
        "relief": "flat",
        "borderwidth": 1,
        "padding": (10, 5),
    }

    style.configure(
        "Primary.TButton",
        **button_base,
        background=DESIGN_SYSTEM["colors"]["primary"],
        foreground="white",
    )

    style.configure(
        "Secondary.TButton",
        **button_base,
        background=DESIGN_SYSTEM["colors"]["secondary"],
        foreground="white",
    )

    style.configure(
        "Error.TButton",
        **button_base,
        background=DESIGN_SYSTEM["colors"]["error"],
        foreground="white",
    )

    style.configure(
        "Success.TButton",
        **button_base,
        background=DESIGN_SYSTEM["colors"]["success"],
        foreground="white",
    )

    # Estilo para Combobox
    style.configure(
        "Custom.TCombobox",
        font=DESIGN_SYSTEM["typography"]["body1"],
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        arrowcolor=DESIGN_SYSTEM["colors"]["primary"],
        padding=5,
    )

    # Configurar estados dos botões
    for btn_style in ["Primary", "Secondary", "Error", "Success"]:
        style.map(
            f"{btn_style}.TButton",
            background=[
                ("active", DESIGN_SYSTEM["colors"]["primary"]),
                ("disabled", DESIGN_SYSTEM["colors"]["text"]["secondary"]),
            ],
            foreground=[("disabled", "white")],
        )

    # Configurar estado do Combobox
    style.map(
        "Custom.TCombobox",
        fieldbackground=[
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["paper"]),
        ],
        selectbackground=[("readonly", DESIGN_SYSTEM["colors"]["primary"])],
        selectforeground=[("readonly", "white")],
    )
