import tkinter as tk
from tkinter import ttk
import platform
import os

from gestao_vista.ui.components import create_sidebar, create_controls
from gestao_vista.ui.styles import setup_styles, DESIGN_SYSTEM
from gestao_vista.services.data_service import DataService
from gestao_vista.ui.observacao_ui import ObservacaoUI
from gestao_vista.ui.windows_fixes import apply_windows_specific_fixes, get_asset_path


def main():
    """Função principal da aplicação."""
    # Verificar o sistema operacional
    is_windows = platform.system() == "Windows"

    # Criar janela principal
    root = tk.Tk()
    root.title("Gestão Vista - Casas de Oração")

    # Aplicar correções específicas para Windows
    if is_windows:
        apply_windows_specific_fixes(root)

    # Configurar tamanho da janela (maior para Windows)
    if is_windows:
        root.geometry("1000x700")
    else:
        root.geometry("800x600")

    # Configurar ícone da aplicação (se disponível)
    try:
        if is_windows:
            icon_path = get_asset_path("icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:
            icon_path = get_asset_path("icon.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                root.iconphoto(True, icon)
    except Exception as e:
        print(f"Erro ao carregar ícone: {e}")
        # Ignorar erros se o ícone não estiver disponível
        pass

    # Configurar tema escuro
    root.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

    # Configurar estilos TTK
    setup_styles(root)

    # Configurar grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=1)

    # Criar serviços
    data_service = DataService()

    # Criar variáveis de controle
    caracteristica_var = tk.StringVar()

    # Criar frame principal com tema escuro
    main_frame = ttk.Frame(root, style="Card.TFrame")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Criar interface de observações
    observacao_ui = ObservacaoUI(root)

    # Criar controles
    def on_caracteristica_selected(is_valid: bool):
        """Callback para quando uma característica é selecionada."""
        if is_valid and export_container:
            export_container.pack(fill=tk.X, padx=10, pady=5)
            export_button.configure(state="normal")
        else:
            export_container.pack_forget()
            export_button.configure(state="disabled")

    controls_frame, combo, feedback = create_controls(
        main_frame, caracteristica_var, on_caracteristica_selected
    )

    # Criar sidebar
    sidebar, (export_container, export_button) = create_sidebar(
        root,
        lambda: data_service.import_gestao_from_excel(combo),
        lambda: data_service.import_casas_from_excel(),
        lambda: data_service.export_faltantes(caracteristica_var.get()),
        lambda: data_service.clear_gestao(),
        lambda: data_service.clear_casas(),
        lambda: data_service.view_casas(),
        lambda: observacao_ui.show(),
    )

    # Configurar o redimensionamento da janela
    def on_resize(event):
        # Ajustar o tamanho dos componentes quando a janela for redimensionada
        width = event.width
        height = event.height

        # Ajustar o tamanho do sidebar e do conteúdo principal
        if width > 800:
            root.grid_columnconfigure(0, weight=3)
            root.grid_columnconfigure(1, weight=1)
        else:
            root.grid_columnconfigure(0, weight=2)
            root.grid_columnconfigure(1, weight=1)

    # Vincular o evento de redimensionamento
    root.bind("<Configure>", on_resize)

    # Iniciar loop principal
    root.mainloop()
