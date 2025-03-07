import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Optional

from ..utils.design_system import DESIGN_SYSTEM, get_button_style


def create_sidebar(
    root: tk.Tk,
    on_load_gestao: Callable,
    on_load_casas: Callable,
    on_export: Callable,
    on_clear_gestao: Callable,
    on_clear_casas: Callable,
    on_view_casas: Callable,
) -> Tuple[ttk.Frame, Tuple[ttk.Frame, tk.Button]]:
    """
    Cria a sidebar com os controles principais.

    Args:
        root: Janela principal
        on_load_gestao: Callback para carregar dados de gestão
        on_load_casas: Callback para carregar dados das casas
        on_export: Callback para exportar dados
        on_clear_gestao: Callback para limpar dados de gestão
        on_clear_casas: Callback para limpar dados das casas
        on_view_casas: Callback para visualizar casas
    """
    sidebar = ttk.Frame(root, style="Card.TFrame")
    sidebar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Título da sidebar
    ttk.Label(sidebar, text="Controles", style="Header.TLabel").pack(pady=10, padx=10)

    # Botões principais
    buttons = [
        ("📊 Carregar Gestão", on_load_gestao, "primary"),
        ("🏠 Carregar Casas", on_load_casas, "primary"),
        ("👁️ Ver Casas", on_view_casas, "secondary"),
        ("🗑️ Limpar Gestão", on_clear_gestao, "error"),
        ("🗑️ Limpar Casas", on_clear_casas, "error"),
    ]

    for text, command, variant in buttons:
        style = get_button_style(variant)
        btn = tk.Button(
            sidebar,
            text=text,
            command=command,
            font=DESIGN_SYSTEM["typography"]["button"],
            bg=style["bg"],
            fg=style["fg"],
            relief="flat",
            cursor="hand2",
        )
        btn.pack(fill=tk.X, padx=10, pady=5)

    # Container para exportação (inicialmente escondido)
    export_container = ttk.Frame(sidebar, style="Card.TFrame")
    export_container.pack(fill=tk.X, padx=10, pady=5)
    export_container.pack_forget()

    # Botão de exportação
    export_style = get_button_style("success")
    export_button = tk.Button(
        export_container,
        text="📥 Exportar Faltantes",
        command=on_export,
        font=DESIGN_SYSTEM["typography"]["button"],
        bg=export_style["bg"],
        fg=export_style["fg"],
        relief="flat",
        cursor="hand2",
        state="disabled",
    )
    export_button.pack(fill=tk.X)

    return sidebar, (export_container, export_button)


def create_main_content(root: tk.Tk) -> Tuple[ttk.Frame, ttk.Frame]:
    """
    Cria o conteúdo principal da aplicação.

    Args:
        root: Janela principal
    """
    main_frame = ttk.Frame(root, style="Card.TFrame")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Frame para o gráfico
    graph_frame = ttk.Frame(main_frame, style="Card.TFrame")
    graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    return main_frame, graph_frame


def create_controls(
    parent: ttk.Frame,
    caracteristica_var: tk.StringVar,
    on_caracteristica_selected: Callable[[bool], None],
) -> Tuple[ttk.Frame, ttk.Combobox, ttk.Label]:
    """
    Cria os controles para seleção de características.

    Args:
        parent: Frame pai
        caracteristica_var: Variável para armazenar a característica selecionada
        on_caracteristica_selected: Callback para quando uma característica é selecionada
    """
    controls_frame = ttk.Frame(parent, style="Card.TFrame")
    controls_frame.pack(fill=tk.X, padx=10, pady=5)

    # Label para o combobox
    ttk.Label(
        controls_frame, text="Selecione uma característica:", style="SubHeader.TLabel"
    ).pack(side=tk.LEFT, padx=5)

    # Combobox para seleção
    combo = ttk.Combobox(
        controls_frame,
        textvariable=caracteristica_var,
        state="readonly",
        font=DESIGN_SYSTEM["typography"]["body1"],
    )
    combo.pack(side=tk.LEFT, padx=5)
    combo.set("Escolha uma característica...")

    # Label para feedback
    feedback_label = ttk.Label(controls_frame, text="", style="TLabel")
    feedback_label.pack(side=tk.LEFT, padx=5)

    def on_combo_selected(event):
        """Callback para quando o combobox é alterado"""
        selected = caracteristica_var.get()
        is_valid = selected != "Escolha uma característica..."
        on_caracteristica_selected(is_valid)

        if is_valid:
            feedback_label.configure(
                text=f"✅ {selected} selecionada",
                foreground=DESIGN_SYSTEM["colors"]["success"],
            )
        else:
            feedback_label.configure(
                text="", foreground=DESIGN_SYSTEM["colors"]["text"]["primary"]
            )

    combo.bind("<<ComboboxSelected>>", on_combo_selected)

    return controls_frame, combo, feedback_label


def create_dialog_window(
    parent: tk.Tk, title: str, width: int = 400, height: int = 300
) -> tk.Toplevel:
    """
    Cria uma janela de diálogo modal.

    Args:
        parent: Janela pai
        title: Título da janela
        width: Largura da janela
        height: Altura da janela
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry(f"{width}x{height}")
    dialog.configure(bg=DESIGN_SYSTEM["colors"]["background"])
    dialog.transient(parent)
    dialog.grab_set()

    return dialog


def create_form_field(
    parent: ttk.Frame, label: str, initial_value: str = "", required: bool = False
) -> Tuple[ttk.Frame, ttk.Entry]:
    """
    Cria um campo de formulário com label.

    Args:
        parent: Frame pai
        label: Label do campo
        initial_value: Valor inicial
        required: Se o campo é obrigatório
    """
    field_frame = ttk.Frame(parent, style="Card.TFrame")
    field_frame.pack(fill=tk.X, padx=10, pady=5)

    # Label com indicador de obrigatório
    label_text = f"{label}{'*' if required else ''}"
    ttk.Label(field_frame, text=label_text, style="SubHeader.TLabel").pack(anchor=tk.W)

    # Entry
    entry = ttk.Entry(field_frame, font=DESIGN_SYSTEM["typography"]["body1"])
    entry.pack(fill=tk.X, pady=(5, 0))
    entry.insert(0, initial_value)

    return field_frame, entry
