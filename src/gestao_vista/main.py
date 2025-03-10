import tkinter as tk
from tkinter import ttk

from gestao_vista.ui.components import create_sidebar, create_controls
from gestao_vista.ui.styles import setup_styles, DESIGN_SYSTEM
from gestao_vista.services.data_service import DataService
from gestao_vista.ui.observacao_ui import ObservacaoUI


def main():
    """Função principal da aplicação."""
    # Criar janela principal
    root = tk.Tk()
    root.title("Gestão Vista")
    root.geometry("800x600")

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

    # Iniciar loop principal
    root.mainloop()
