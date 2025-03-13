import tkinter as tk
from tkinter import ttk
import platform
import os
import sys


def apply_windows_specific_fixes(root: tk.Tk) -> None:
    """
    Aplica correções específicas para Windows para melhorar a aparência da aplicação.

    Args:
        root: A janela principal da aplicação
    """
    if platform.system() != "Windows":
        return

    # Ajustar DPI para evitar problemas de escala
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    # Melhorar a aparência dos botões no Windows
    def fix_button_appearance(widget):
        """Recursivamente melhora a aparência dos botões no Windows"""
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                # Adicionar padding extra para botões no Windows
                current_padx = child.cget("padx")
                current_pady = child.cget("pady")
                if isinstance(current_padx, int) and current_padx < 15:
                    child.configure(padx=15)
                if isinstance(current_pady, int) and current_pady < 8:
                    child.configure(pady=8)

                # Garantir que o botão tenha bordas arredondadas
                child.configure(relief="flat", overrelief="flat")

            # Corrigir comboboxes
            if isinstance(child, ttk.Combobox):
                # Garantir que o combobox tenha cores adequadas
                child.configure(
                    foreground="#0F172A",  # Texto escuro
                    background="#F8FAFC",  # Fundo claro
                )

                # Aplicar estilo específico para Windows
                style = ttk.Style()
                style.map(
                    "TCombobox",
                    fieldbackground=[
                        ("readonly", "#F8FAFC"),  # Fundo claro para o campo
                        ("active", "#F8FAFC"),
                        ("disabled", "#E2E8F0"),
                    ],
                    foreground=[
                        ("readonly", "#0F172A"),  # Texto escuro
                        ("active", "#0F172A"),
                        ("disabled", "#64748B"),
                    ],
                    selectbackground=[
                        ("readonly", "#3B82F6"),  # Cor de seleção azul
                    ],
                    selectforeground=[
                        ("readonly", "#FFFFFF"),  # Texto branco na seleção
                    ],
                )

            # Corrigir Treeview (tabelas)
            if isinstance(child, ttk.Treeview):
                # Aplicar estilo específico para Windows
                style = ttk.Style()
                style.configure(
                    "Treeview",
                    background="#F8FAFC",  # Fundo claro
                    foreground="#0F172A",  # Texto escuro
                    fieldbackground="#F8FAFC",
                    borderwidth=1,
                    relief="solid",
                )

                style.configure(
                    "Treeview.Heading",
                    background="#E2E8F0",  # Fundo cinza claro para cabeçalhos
                    foreground="#0F172A",  # Texto escuro
                    relief="solid",
                    borderwidth=1,
                )

                style.map(
                    "Treeview",
                    background=[
                        ("selected", "#3B82F6"),  # Azul para linhas selecionadas
                    ],
                    foreground=[
                        (
                            "selected",
                            "#FFFFFF",
                        ),  # Texto branco para linhas selecionadas
                    ],
                )

            # Processar recursivamente
            fix_button_appearance(child)

    # Aplicar correções após um curto delay para garantir que todos os widgets estejam criados
    root.after(100, lambda: fix_button_appearance(root))

    # Configurar o tema visual do Windows
    style = ttk.Style()
    available_themes = style.theme_names()

    # Tentar usar temas que funcionam bem no Windows
    preferred_themes = ["vista", "winnative", "xpnative", "clam"]
    for theme in preferred_themes:
        if theme in available_themes:
            style.theme_use(theme)
            break

    # Corrigir estilos específicos para Windows
    fix_windows_styles(style)


def fix_windows_styles(style):
    """
    Aplica correções específicas aos estilos do ttk para Windows.

    Args:
        style: Objeto ttk.Style
    """
    # Corrigir combobox
    style.configure(
        "TCombobox",
        foreground="#0F172A",  # Texto escuro
        fieldbackground="#F8FAFC",  # Fundo claro
        background="#F8FAFC",
        arrowcolor="#3B82F6",  # Seta azul
        relief="solid",
        borderwidth=1,
    )

    # Mapear estados do combobox
    style.map(
        "TCombobox",
        fieldbackground=[
            ("readonly", "#F8FAFC"),  # Fundo claro para o campo
            ("active", "#F8FAFC"),
            ("disabled", "#E2E8F0"),
        ],
        foreground=[
            ("readonly", "#0F172A"),  # Texto escuro
            ("active", "#0F172A"),
            ("disabled", "#64748B"),
        ],
        selectbackground=[
            ("readonly", "#3B82F6"),  # Cor de seleção azul
        ],
        selectforeground=[
            ("readonly", "#FFFFFF"),  # Texto branco na seleção
        ],
    )

    # Corrigir variante customizada do combobox
    style.configure(
        "Custom.TCombobox",
        foreground="#0F172A",  # Texto escuro
        fieldbackground="#F8FAFC",  # Fundo claro
        background="#F8FAFC",
        arrowcolor="#3B82F6",  # Seta azul
        relief="solid",
        borderwidth=1,
    )

    # Mapear estados da variante customizada
    style.map(
        "Custom.TCombobox",
        fieldbackground=[
            ("readonly", "#F8FAFC"),  # Fundo claro para o campo
            ("active", "#F8FAFC"),
            ("disabled", "#E2E8F0"),
        ],
        foreground=[
            ("readonly", "#0F172A"),  # Texto escuro
            ("active", "#0F172A"),
            ("disabled", "#64748B"),
        ],
        selectbackground=[
            ("readonly", "#3B82F6"),  # Cor de seleção azul
        ],
        selectforeground=[
            ("readonly", "#FFFFFF"),  # Texto branco na seleção
        ],
    )

    # Corrigir Treeview (tabelas)
    style.configure(
        "Treeview",
        background="#F8FAFC",  # Fundo claro
        foreground="#0F172A",  # Texto escuro
        fieldbackground="#F8FAFC",
        borderwidth=1,
        relief="solid",
        rowheight=30,  # Altura das linhas
    )

    # Corrigir cabeçalho do Treeview - problema com cabeçalho invisível no Windows
    style.configure(
        "Treeview.Heading",
        background="#E2E8F0",  # Fundo cinza claro para cabeçalhos
        foreground="#0F172A",  # Texto escuro
        relief="solid",
        borderwidth=1,
        font=("Segoe UI", 10, "bold"),
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
                                                ("Treeheading.text", {"sticky": "we"}),
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

    # Mapear estados do Treeview
    style.map(
        "Treeview",
        background=[
            ("selected", "#3B82F6"),  # Azul para linhas selecionadas
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


def get_asset_path(filename: str) -> str:
    """
    Retorna o caminho completo para um arquivo na pasta assets.

    Args:
        filename: Nome do arquivo na pasta assets

    Returns:
        Caminho completo para o arquivo
    """
    # Determinar o diretório base da aplicação
    if getattr(sys, "frozen", False):
        # Se estiver executando como um executável empacotado
        base_dir = os.path.dirname(sys.executable)
    else:
        # Se estiver executando como script Python
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

    # Construir o caminho para o arquivo de assets
    return os.path.join(base_dir, "assets", filename)


def fix_treeview_header_for_windows(tree: ttk.Treeview) -> None:
    """
    Aplica correções específicas para o cabeçalho da tabela no Windows.

    Args:
        tree: Objeto ttk.Treeview
    """
    if platform.system() != "Windows":
        return

    # Aplicar estilo específico para o cabeçalho
    style = ttk.Style()
    style.configure(
        "Treeview.Heading",
        background="#E2E8F0",  # Fundo cinza claro para cabeçalhos
        foreground="#0F172A",  # Texto escuro
        relief="solid",
        borderwidth=1,
        font=("Segoe UI", 10, "bold"),
    )

    # Aplicar layout específico para o cabeçalho
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
                                                ("Treeheading.text", {"sticky": "we"}),
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

    # Mapear estados do cabeçalho
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

    # Configurar colunas para garantir que sejam visíveis
    for col in tree["columns"]:
        current_width = tree.column(col, "width")
        tree.column(col, width=current_width, minwidth=max(80, current_width // 2))
