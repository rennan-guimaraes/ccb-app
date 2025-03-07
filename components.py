import tkinter as tk
from tkinter import ttk
from styles import DESIGN_SYSTEM


def darken_color(hex_color, factor=0.8):
    """Escurece uma cor hex por um fator"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten_color(hex_color, factor=1.2):
    """Clareia uma cor hex por um fator"""
    hex_color = hex_color.lstrip("#")
    r = min(255, int(int(hex_color[0:2], 16) * factor))
    g = min(255, int(int(hex_color[2:4], 16) * factor))
    b = min(255, int(int(hex_color[4:6], 16) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def create_sidebar(
    root,
    load_gestao_callback,
    load_casas_callback,
    export_callback,
    clear_gestao_callback,
    clear_casas_callback,
    view_casas_callback,
):
    # Frame externo para borda com gradiente
    outer_sidebar = tk.Frame(
        root,
        bg=DESIGN_SYSTEM["colors"]["border"],
        highlightthickness=0,
    )
    outer_sidebar.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(1, 0))
    outer_sidebar.grid_columnconfigure(0, weight=1)

    # Frame interno da sidebar com gradiente
    sidebar = ttk.Frame(outer_sidebar, style="Sidebar.TFrame")
    sidebar.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=1, pady=1)
    sidebar.grid_columnconfigure(0, weight=1)

    # Título da Sidebar com ícone e estilo moderno
    title_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
    title_frame.grid(row=0, column=0, pady=(20, 30), sticky="ew")
    title_frame.grid_columnconfigure(0, weight=1)

    sidebar_title = ttk.Label(
        title_frame,
        text="🎯 Menu Principal",
        style="MenuHeader.TLabel",
        anchor="center",
    )
    sidebar_title.grid(row=0, column=0, sticky="ew")

    # Botões com ícones e descrições
    buttons_data = [
        {
            "icon": "📊",
            "text": "Carregar\nGestão à Vista",
            "description": "Importar dados do arquivo de gestão",
            "command": load_gestao_callback,
            "style": "Primary.TButton",
            "row": 1,
            "enabled": True,
        },
        {
            "icon": "🗑️",
            "text": "Limpar\nGestão à Vista",
            "description": "Limpar dados do arquivo de gestão",
            "command": clear_gestao_callback,
            "style": "Danger.TButton",
            "row": 2,
            "enabled": True,
        },
        {
            "icon": "📁",
            "text": "Carregar\nCasas de Oração",
            "description": "Importar lista de casas",
            "command": load_casas_callback,
            "style": "Info.TButton",
            "row": 3,
            "enabled": True,
        },
        {
            "icon": "🗑️",
            "text": "Limpar\nCasas de Oração",
            "description": "Limpar dados das casas",
            "command": clear_casas_callback,
            "style": "Danger.TButton",
            "row": 4,
            "enabled": True,
        },
        {
            "icon": "👁️",
            "text": "Visualizar\nCasas de Oração",
            "description": "Ver e editar casas cadastradas",
            "command": view_casas_callback,
            "style": "Purple.TButton",
            "row": 5,
            "enabled": True,
        },
    ]

    # Container para o botão de exportar
    export_container = ttk.Frame(sidebar, style="Sidebar.TFrame")
    export_container.grid(row=6, column=0, pady=(20, 20), sticky="ew")
    export_container.grid_columnconfigure(0, weight=1)
    export_container.grid_remove()

    # Botão de exportar com estilo moderno
    export_btn = ttk.Button(
        export_container,
        text="📥 Exportar\nCasas Faltantes",
        command=export_callback,
        style="Warning.TButton",
        cursor="hand2",
    )
    export_btn.grid(row=0, column=0, sticky="ew", padx=10)

    # Criar os outros botões com estilo moderno
    for btn_data in buttons_data:
        # Container para cada botão e sua descrição
        btn_container = ttk.Frame(sidebar, style="Sidebar.TFrame")
        btn_container.grid(row=btn_data["row"], column=0, pady=(0, 15), sticky="ew")
        btn_container.grid_columnconfigure(0, weight=1)

        # Botão principal com efeito de elevação
        btn = ttk.Button(
            btn_container,
            text=f"{btn_data['icon']} {btn_data['text']}",
            command=btn_data["command"],
            style=btn_data["style"],
            cursor="hand2",
        )
        btn.grid(row=0, column=0, sticky="ew", padx=10)

        # Descrição do botão com estilo caption
        desc_label = ttk.Label(
            btn_container,
            text=btn_data["description"],
            style="MenuCaption.TLabel",
            anchor="center",
        )
        desc_label.grid(row=1, column=0, pady=(5, 0), sticky="ew")

    return sidebar, (export_container, export_btn)


def create_main_content(root):
    # Container principal com padding
    main_frame = ttk.Frame(root, style="Background.TFrame")
    main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=20, pady=20)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)

    # Cabeçalho com título e subtítulo
    header_frame = ttk.Frame(main_frame, style="Background.TFrame")
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))

    title_label = ttk.Label(
        header_frame, text="📈 Sistema de Gestão à Vista", style="Header.TLabel"
    )
    title_label.grid(row=0, column=0, sticky="w")

    subtitle_label = ttk.Label(
        header_frame,
        text="Visualize e gerencie as características das casas de oração",
        style="SubHeader.TLabel",
    )
    subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

    # Container do gráfico com elevação - frame externo para borda
    outer_graph_container = tk.Frame(
        main_frame, bg=DESIGN_SYSTEM["colors"]["border"], highlightthickness=0
    )
    outer_graph_container.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    outer_graph_container.grid_columnconfigure(0, weight=1)
    outer_graph_container.grid_rowconfigure(0, weight=1)

    # Frame interno com a cor de fundo correta
    graph_container = ttk.Frame(outer_graph_container, style="Card.TFrame")
    graph_container.grid(
        row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=1, pady=1
    )
    graph_container.grid_columnconfigure(0, weight=1)
    graph_container.grid_rowconfigure(0, weight=1)

    # Frame para o conteúdo do gráfico
    graph_frame = ttk.Frame(graph_container, style="Card.TFrame")
    graph_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=20, pady=20)

    return main_frame, graph_frame


def create_controls(main_frame, caracteristica_var, on_selection_change=None):
    # Frame de controles com espaçamento
    controls_frame = ttk.Frame(main_frame, style="Background.TFrame")
    controls_frame.grid(row=2, column=0, pady=(30, 0), sticky="ew")
    controls_frame.grid_columnconfigure(1, weight=1)

    # Label com ícone
    label_frame = ttk.Frame(controls_frame, style="Background.TFrame")
    label_frame.grid(row=0, column=0, padx=(0, 20))

    icon_label = ttk.Label(label_frame, text="🔍", style="SubHeader.TLabel")
    icon_label.grid(row=0, column=0, padx=(0, 5))

    text_label = ttk.Label(
        label_frame, text="Selecione a característica:", style="SubHeader.TLabel"
    )
    text_label.grid(row=0, column=1)

    # Combobox moderno com estilo dark
    combo = ttk.Combobox(
        controls_frame,
        textvariable=caracteristica_var,
        style="Custom.TCombobox",
        width=50,
        font=("Helvetica", 12),
        state="readonly",
    )
    combo.grid(row=0, column=1, sticky="ew", padx=20)

    # Adicionar placeholder
    combo.set("Escolha uma característica...")

    # Feedback visual
    feedback_label = ttk.Label(
        controls_frame,
        text="",
        style="Caption.TLabel",
    )
    feedback_label.grid(row=1, column=1, sticky="w", padx=20, pady=(5, 0))

    def on_caracteristica_change(*args):
        selected = caracteristica_var.get()
        is_valid = selected and selected != "Escolha uma característica..."

        if is_valid:
            feedback_label.configure(
                text=f"✅ Característica selecionada: {selected}",
                foreground=DESIGN_SYSTEM["colors"]["success"],
            )
        else:
            feedback_label.configure(
                text="❌ Nenhuma característica selecionada",
                foreground=DESIGN_SYSTEM["colors"]["error"],
            )

        if on_selection_change:
            on_selection_change(is_valid)

    def on_combo_select(event):
        selected = combo.get()
        if selected != "Escolha uma característica...":
            caracteristica_var.set(selected)
            feedback_label.configure(
                text=f"✅ Característica selecionada: {selected}",
                foreground=DESIGN_SYSTEM["colors"]["success"],
            )
            if on_selection_change:
                on_selection_change(True)
        else:
            feedback_label.configure(
                text="❌ Nenhuma característica selecionada",
                foreground=DESIGN_SYSTEM["colors"]["error"],
            )
            if on_selection_change:
                on_selection_change(False)

    caracteristica_var.trace_add("write", on_caracteristica_change)
    combo.bind("<<ComboboxSelected>>", on_combo_select)

    return controls_frame, combo, feedback_label
