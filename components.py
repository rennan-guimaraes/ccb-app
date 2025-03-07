import tkinter as tk
from tkinter import ttk
from styles import setup_styles

# Obter o design system
DESIGN_SYSTEM = setup_styles()


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


def create_sidebar(root, load_gestao_callback, load_casas_callback, export_callback):
    # Frame externo para borda
    outer_sidebar = tk.Frame(
        root,
        bg=DESIGN_SYSTEM["colors"]["border"],  # Usar a cor de borda do design system
        highlightthickness=0,
    )
    outer_sidebar.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(1, 0))
    outer_sidebar.grid_columnconfigure(0, weight=1)

    # Frame interno da sidebar
    sidebar = ttk.Frame(outer_sidebar, style="Sidebar.TFrame")
    sidebar.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=1, pady=1)
    sidebar.grid_columnconfigure(0, weight=1)

    # Título da Sidebar com ícone
    sidebar_title = ttk.Label(
        sidebar, text="🎯 Menu Principal", style="SubHeader.TLabel", anchor="center"
    )
    sidebar_title.grid(row=0, column=0, pady=(0, 30), sticky="ew")

    # Botões com ícones e descrições
    buttons_data = [
        {
            "icon": "📊",
            "text": "Carregar\nGestão à Vista",
            "description": "Importar dados do arquivo de gestão",
            "command": load_gestao_callback,
            "color": "#4CAF50",  # primary mais vibrante
            "row": 1,
        },
        {
            "icon": "📁",
            "text": "Carregar\nCasas de Oração",
            "description": "Importar lista de casas",
            "command": load_casas_callback,
            "color": "#4CAF50",  # primary mais vibrante
            "row": 2,
        },
        {
            "icon": "📥",
            "text": "Exportar\nCasas Faltantes",
            "description": "Gerar relatório de pendências",
            "command": export_callback,
            "color": "#2196F3",  # secondary mais vibrante
            "row": 3,
        },
    ]

    for btn_data in buttons_data:
        # Container para cada botão e sua descrição
        btn_container = ttk.Frame(sidebar, style="Sidebar.TFrame")
        btn_container.grid(row=btn_data["row"], column=0, pady=(0, 20), sticky="ew")
        btn_container.grid_columnconfigure(0, weight=1)

        # Calcular cores para diferentes estados
        darker_color = darken_color(
            btn_data["color"], 0.7
        )  # Mais escuro para contraste
        hover_color = lighten_color(btn_data["color"], 1.1)  # Mais claro para hover

        # Botão principal com efeito de elevação
        btn = tk.Button(
            btn_container,
            text=f"{btn_data['icon']}\n{btn_data['text']}",
            command=btn_data["command"],
            font=("Helvetica", 16, "bold"),
            bg=btn_data["color"],
            fg="white",
            height=4,
            width=20,
            relief="flat",
            borderwidth=0,
            activebackground=darker_color,
            activeforeground="white",
            cursor="hand2",
            disabledforeground="white",
        )

        # Efeitos de hover e clique
        def on_enter(e, b=btn, c=hover_color):
            b.configure(bg=c)
            b.configure(relief="solid")

        def on_leave(e, b=btn, c=btn_data["color"]):
            b.configure(bg=c)
            b.configure(relief="flat")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.grid(row=0, column=0, sticky="ew")

        # Descrição do botão com estilo caption
        desc_label = ttk.Label(
            btn_container,
            text=btn_data["description"],
            style="Caption.TLabel",
            anchor="center",
        )
        desc_label.grid(row=1, column=0, pady=(5, 0), sticky="ew")

    return sidebar


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


def create_controls(main_frame, caracteristica_var):
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
        print(f"Mudança de característica detectada: '{selected}'")  # Debug
        if selected and selected != "Escolha uma característica...":
            feedback_label.configure(
                text=f"✅ Característica selecionada: {selected}",
                foreground=DESIGN_SYSTEM["colors"]["success"],
            )
        else:
            feedback_label.configure(
                text="❌ Nenhuma característica selecionada",
                foreground=DESIGN_SYSTEM["colors"]["error"],
            )

    def on_combo_select(event):
        selected = combo.get()
        print(f"Seleção do combo: '{selected}'")  # Debug
        if selected != "Escolha uma característica...":
            caracteristica_var.set(selected)
            feedback_label.configure(
                text=f"✅ Característica selecionada: {selected}",
                foreground=DESIGN_SYSTEM["colors"]["success"],
            )

    caracteristica_var.trace("w", on_caracteristica_change)
    combo.bind("<<ComboboxSelected>>", on_combo_select)

    return controls_frame, combo, feedback_label
