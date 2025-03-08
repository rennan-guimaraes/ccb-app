import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Optional, List
from tkmacosx import Button as MacButton

from ..utils.design_system import DESIGN_SYSTEM, get_button_style


def create_label(parent: tk.Widget, text: str, variant: str = "body1") -> tk.Label:
    """Cria um label estilizado"""
    styles = {
        "h1": DESIGN_SYSTEM["typography"]["h1"],
        "h2": DESIGN_SYSTEM["typography"]["h2"],
        "h3": DESIGN_SYSTEM["typography"]["h3"],
        "body1": DESIGN_SYSTEM["typography"]["body1"],
        "body2": DESIGN_SYSTEM["typography"]["body2"],
    }

    font = styles.get(variant, DESIGN_SYSTEM["typography"]["body1"])
    fg_color = DESIGN_SYSTEM["colors"]["text"]["primary"]
    bg_color = DESIGN_SYSTEM["colors"]["background"]["paper"]

    return tk.Label(
        parent,
        text=text,
        font=font,
        fg=fg_color,
        bg=bg_color,
        anchor="w",
    )


def create_button(
    parent: ttk.Frame, text: str, command: Callable, variant: str
) -> MacButton:
    """Cria um botão estilizado usando tkmacosx.Button"""
    style = get_button_style(variant)
    bg_color = style["default"]
    hover_color = style["hover"]
    fg_color = style["text"]
    font = DESIGN_SYSTEM["typography"]["button"]

    btn = MacButton(
        parent,
        text=text,
        command=command,
        font=font,
        fg=fg_color,
        bg=bg_color,
        activebackground=hover_color,
        activeforeground=fg_color,
        disabledforeground=DESIGN_SYSTEM["colors"]["text"]["disabled"],
        borderless=1,
        focuscolor="",
        height=35,
        padx=12,
        overrelief="flat",
        borderwidth=0,
        highlightthickness=0,
        overbackground=hover_color,
    )
    btn.pack(fill=tk.X, padx=10, pady=5)

    def on_disable():
        btn.configure(
            bg=DESIGN_SYSTEM["colors"]["background"]["button"],
            fg=DESIGN_SYSTEM["colors"]["text"]["disabled"],
        )

    # Configurar estado inicial
    if str(btn["state"]) == "disabled":
        on_disable()

    # Sobrescrever o método configure para manter as cores corretas
    original_configure = btn.configure

    def new_configure(**kwargs):
        if "state" in kwargs:
            if kwargs["state"] == "disabled":
                on_disable()
            elif kwargs["state"] == "normal":
                btn.configure(bg=bg_color, fg=fg_color)
        original_configure(**kwargs)

    btn.configure = new_configure

    return btn


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
    # Frame principal da sidebar com fundo escuro
    sidebar = ttk.Frame(root, style="Card.TFrame")
    sidebar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Frame para conteúdo com padding interno
    content_frame = ttk.Frame(sidebar, style="Card.TFrame")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Título da sidebar
    title_label = create_label(content_frame, "Controles", "h1")
    title_label.pack(pady=(10, 20), padx=10)

    # Botões principais com espaçamento consistente
    buttons = [
        ("📊 Carregar Gestão", on_load_gestao, "primary"),
        ("🏠 Carregar Casas", on_load_casas, "primary"),
        ("👁️ Ver Casas", on_view_casas, "secondary"),
        ("🗑️ Limpar Gestão", on_clear_gestao, "error"),
        ("🗑️ Limpar Casas", on_clear_casas, "error"),
    ]

    for text, command, style in buttons:
        btn = create_button(content_frame, text, command, style)

    # Container para exportação (inicialmente escondido)
    export_container = ttk.Frame(content_frame, style="Card.TFrame")
    export_container.pack(fill=tk.X, padx=10, pady=5)
    export_container.pack_forget()

    # Botão de exportação
    export_button = create_button(
        export_container, "📥 Exportar Faltantes", on_export, "success"
    )
    export_button.configure(state="disabled")

    return sidebar, (export_container, export_button)


def create_main_content(root: tk.Tk) -> Tuple[ttk.Frame, ttk.Frame, ttk.Frame]:
    """
    Cria o conteúdo principal da aplicação.

    Args:
        root: Janela principal

    Returns:
        Tuple contendo o frame principal, frame do gráfico e frame da tabela
    """
    main_frame = ttk.Frame(root, style="Card.TFrame")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Frame para o gráfico (inicialmente visível)
    graph_frame = ttk.Frame(main_frame, style="Card.TFrame")
    graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame para a tabela (inicialmente escondido)
    table_frame = ttk.Frame(main_frame, style="Card.TFrame")

    return main_frame, graph_frame, table_frame


def create_combobox(
    parent: tk.Widget,
    textvariable: tk.StringVar,
    values: List[str] = None,
) -> ttk.Combobox:
    """Cria um combobox estilizado"""
    combo = ttk.Combobox(
        parent,
        textvariable=textvariable,
        values=values,
        state="readonly",
        font=DESIGN_SYSTEM["typography"]["body1"],
        style="Custom.TCombobox",
    )

    # Configurar estilo da seta
    style = ttk.Style()
    style.configure(
        "Custom.TCombobox",
        background=DESIGN_SYSTEM["colors"]["background"]["paper"],
        fieldbackground=DESIGN_SYSTEM["colors"]["background"]["paper"],
        foreground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        arrowcolor=DESIGN_SYSTEM["colors"]["primary"],
        borderwidth=2,
        relief="solid",
        padding=5,
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[
            ("readonly", DESIGN_SYSTEM["colors"]["background"]["paper"]),
            ("disabled", DESIGN_SYSTEM["colors"]["background"]["default"]),
            ("active", DESIGN_SYSTEM["colors"]["primary"]),
        ],
        foreground=[
            ("readonly", DESIGN_SYSTEM["colors"]["text"]["primary"]),
            ("disabled", DESIGN_SYSTEM["colors"]["text"]["disabled"]),
            ("active", DESIGN_SYSTEM["colors"]["text"]["primary"]),
        ],
        bordercolor=[
            ("focus", DESIGN_SYSTEM["colors"]["primary"]),
            ("active", DESIGN_SYSTEM["colors"]["primary"]),
        ],
    )

    return combo


def create_controls(
    parent: ttk.Frame,
    caracteristica_var: tk.StringVar,
    on_caracteristica_selected: Callable[[bool], None],
) -> Tuple[ttk.Frame, ttk.Combobox, tk.Label]:
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
    label = create_label(controls_frame, "Selecione uma característica:", "h3")
    label.pack(side=tk.LEFT, padx=5)

    # Combobox para seleção
    combo = create_combobox(controls_frame, caracteristica_var)
    combo.pack(side=tk.LEFT, padx=5)
    combo.set("Escolha uma característica...")

    # Label para feedback
    feedback_label = create_label(controls_frame, "", "body2")
    feedback_label.pack(side=tk.LEFT, padx=5)

    def on_combo_selected(event):
        """Callback para quando o combobox é alterado"""
        selected = caracteristica_var.get()
        is_valid = selected != "Escolha uma característica..."
        on_caracteristica_selected(is_valid)

        if is_valid:
            feedback_label.configure(
                text=f"✅ {selected} selecionada",
                fg=DESIGN_SYSTEM["colors"]["success"],
            )
        else:
            feedback_label.configure(
                text="",
                fg=DESIGN_SYSTEM["colors"]["text"]["secondary"],
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
    dialog.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])
    dialog.transient(parent)
    dialog.grab_set()

    return dialog


def create_entry(parent: tk.Widget, initial_value: str = "") -> tk.Entry:
    """Cria um entry estilizado"""
    entry = tk.Entry(
        parent,
        font=DESIGN_SYSTEM["typography"]["body1"],
        fg=DESIGN_SYSTEM["colors"]["text"]["primary"],
        bg=DESIGN_SYSTEM["colors"]["background"]["paper"],
        insertbackground=DESIGN_SYSTEM["colors"]["text"]["primary"],  # Cursor color
        selectbackground=DESIGN_SYSTEM["colors"]["primary"],
        selectforeground=DESIGN_SYSTEM["colors"]["text"]["primary"],
        relief="flat",
        bd=1,
    )

    entry.insert(0, initial_value)

    # Criar borda personalizada
    def on_focus_in(e):
        entry.configure(
            bd=2,
            highlightthickness=1,
            highlightcolor=DESIGN_SYSTEM["colors"]["primary"],
            highlightbackground=DESIGN_SYSTEM["colors"]["border"],
        )

    def on_focus_out(e):
        entry.configure(
            bd=1,
            highlightthickness=0,
        )

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry


def create_form_field(
    parent: ttk.Frame, label: str, initial_value: str = "", required: bool = False
) -> Tuple[ttk.Frame, tk.Entry]:
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
    label = create_label(field_frame, label_text, "h3")
    label.pack(anchor=tk.W)

    # Entry
    entry = create_entry(field_frame, initial_value)
    entry.pack(fill=tk.X, pady=(5, 0))

    return field_frame, entry
