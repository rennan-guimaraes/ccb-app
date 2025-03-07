import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
from ..utils.design_system import DESIGN_SYSTEM, setup_styles as setup_styles_base


def setup_styles(root: tk.Tk):
    """Configura os estilos TTK para a aplicação."""
    # Configurar estilos base
    setup_styles_base()

    # Configurações adicionais específicas da UI
    style = ttk.Style(root)
    style.theme_use("clam")

    # Configuração base
    style.configure(
        ".",  # Estilo base para todos os widgets
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        troughcolor=DESIGN_SYSTEM["colors"]["background"]["paper"],
        font=DESIGN_SYSTEM["typography"]["body1"],
    )

    # Configuração base para frames
    style.configure(
        "TFrame", background=DESIGN_SYSTEM["colors"]["background"]["default"]
    )

    # Estilo para cards
    style.configure(
        "Card.TFrame", background=DESIGN_SYSTEM["colors"]["background"]["paper"]
    )

    # Configuração base para labels
    style.configure(
        "TLabel",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
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

    # Configurar variantes de labels
    style.configure(
        "Success.TLabel",
        font=DESIGN_SYSTEM["typography"]["body2"],
        foreground=DESIGN_SYSTEM["colors"]["success"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "Error.TLabel",
        font=DESIGN_SYSTEM["typography"]["body2"],
        foreground=DESIGN_SYSTEM["colors"]["error"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    style.configure(
        "Warning.TLabel",
        font=DESIGN_SYSTEM["typography"]["body2"],
        foreground=DESIGN_SYSTEM["colors"]["warning"],
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
    )

    # Estilo para Combobox
    style.configure(
        "TCombobox",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        arrowcolor=DESIGN_SYSTEM["colors"]["primary"],
        relief="flat",
        borderwidth=0,
    )

    # Configurar variante customizada do Combobox
    style.configure(
        "Custom.TCombobox",
        background=DESIGN_SYSTEM["colors"]["background"]["default"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["default"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        selectbackground=DESIGN_SYSTEM["colors"]["primary"],
        selectforeground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        relief="flat",
        borderwidth=0,
    )

    # Configurar estado do Combobox
    style.map(
        "TCombobox",
        background=[
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("active", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["paper"]),
        ],
        fieldbackground=[
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("active", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["paper"]),
        ],
        selectbackground=[("readonly", DESIGN_SYSTEM["colors"]["primary"])],
        selectforeground=[("readonly", "white")],
        relief=[("readonly", "flat"), ("active", "flat"), ("disabled", "flat")],
        borderwidth=[("readonly", 0), ("active", 0), ("disabled", 0)],
    )
