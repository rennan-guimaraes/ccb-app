import tkinter as tk
from tkinter import ttk
import platform
from typing import Dict, Any
from gestao_vista.utils.design_system import (
    DESIGN_SYSTEM,
    setup_styles as setup_styles_base,
)

# Verificar o sistema operacional
IS_WINDOWS = platform.system() == "Windows"


def setup_styles(root: tk.Tk):
    """Configura os estilos TTK para a aplicação."""
    # Configurar estilos base
    setup_styles_base()

    # Configurações adicionais específicas da UI
    style = ttk.Style(root)

    # No Windows, usar o tema 'vista' ou 'winnative' para melhor compatibilidade
    if IS_WINDOWS:
        try:
            style.theme_use("vista")
        except tk.TclError:
            try:
                style.theme_use("winnative")
            except tk.TclError:
                style.theme_use("clam")  # Fallback para clam
    else:
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
    if IS_WINDOWS:
        # Configurações específicas para Windows
        style.configure(
            "TCombobox",
            background="#F8FAFC",
            fieldbackground="#F8FAFC",
            foreground="#0F172A",
            arrowcolor=DESIGN_SYSTEM["colors"]["primary"],
            relief="solid",
            borderwidth=1,
        )

        # Configurar variante customizada do Combobox
        style.configure(
            "Custom.TCombobox",
            background="#F8FAFC",
            fieldbackground="#F8FAFC",
            foreground="#0F172A",
            selectbackground=DESIGN_SYSTEM["colors"]["primary"],
            selectforeground="#FFFFFF",
            relief="solid",
            borderwidth=1,
        )

        # Configurar estado do Combobox
        style.map(
            "TCombobox",
            background=[
                ("readonly", "#F8FAFC"),
                ("active", "#F8FAFC"),
                ("disabled", "#E2E8F0"),
            ],
            fieldbackground=[
                ("readonly", "#F8FAFC"),
                ("active", "#F8FAFC"),
                ("disabled", "#E2E8F0"),
            ],
            foreground=[
                ("readonly", "#0F172A"),
                ("active", "#0F172A"),
                ("disabled", "#64748B"),
            ],
            selectbackground=[("readonly", DESIGN_SYSTEM["colors"]["primary"])],
            selectforeground=[("readonly", "#FFFFFF")],
            relief=[("readonly", "solid"), ("active", "solid"), ("disabled", "solid")],
            borderwidth=[("readonly", 1), ("active", 1), ("disabled", 1)],
        )
    else:
        # Configurações para Mac e outros sistemas
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

    # Estilo para Entry
    style.configure(
        "TEntry",
        padding=5,
        relief="flat",
        borderwidth=1,
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        insertcolor=DESIGN_SYSTEM["colors"]["text"]["primary"],  # Cor do cursor
        selectbackground=DESIGN_SYSTEM["colors"]["primary"],
        selectforeground=DESIGN_SYSTEM["colors"]["text"]["primary"],
    )

    # Estilo para Treeview (tabelas)
    if IS_WINDOWS:
        # Configurações específicas para Windows
        style.configure(
            "Treeview",
            background="#F8FAFC",  # Fundo claro
            foreground="#0F172A",  # Texto escuro
            fieldbackground="#F8FAFC",
            borderwidth=1,
            relief="solid",
            rowheight=30,  # Altura das linhas
        )

        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",  # Fundo cinza claro para cabeçalhos
            foreground="#0F172A",  # Texto escuro
            relief="solid",
            borderwidth=1,
            font=(DESIGN_SYSTEM["typography"]["button"][0], 10, "bold"),
        )

        # Garantir que o cabeçalho seja visível no Windows
        style.layout(
            "Treeview.Heading",
            [
                (
                    "Treeheading.cell",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "Treeheading.border",
                                {
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "Treeheading.padding",
                                            {
                                                "sticky": "nswe",
                                                "children": [
                                                    (
                                                        "Treeheading.image",
                                                        {"side": "right", "sticky": ""},
                                                    ),
                                                    (
                                                        "Treeheading.text",
                                                        {"sticky": "we"},
                                                    ),
                                                ],
                                            },
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    DESIGN_SYSTEM["colors"]["primary"],
                ),  # Azul para linhas selecionadas
            ],
            foreground=[
                ("selected", "#FFFFFF"),  # Texto branco para linhas selecionadas
            ],
        )

        # Mapear estados do cabeçalho do Treeview
        style.map(
            "Treeview.Heading",
            background=[
                ("active", "#CBD5E1"),  # Cor quando o mouse passa por cima
                ("pressed", "#94A3B8"),  # Cor quando pressionado
            ],
            relief=[
                ("active", "solid"),
                ("pressed", "solid"),
            ],
        )
    else:
        # Configurações para Mac e outros sistemas
        style.configure(
            "Treeview",
            background=DESIGN_SYSTEM["colors"]["background"]["paper"],
            foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
            fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
            borderwidth=0,
            relief="flat",
            rowheight=30,  # Altura das linhas
        )

        style.configure(
            "Treeview.Heading",
            background=DESIGN_SYSTEM["colors"]["background"]["default"],
            foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
            relief="flat",
            borderwidth=0,
            font=DESIGN_SYSTEM["typography"]["button"],
        )

        style.map(
            "Treeview",
            background=[
                ("selected", DESIGN_SYSTEM["colors"]["primary"]),
            ],
            foreground=[
                ("selected", DESIGN_SYSTEM["colors"]["text"]["primary"]),
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
