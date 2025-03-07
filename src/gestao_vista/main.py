import tkinter as tk
from tkinter import ttk

from .ui.components import create_sidebar, create_controls
from .ui.styles import setup_styles, DESIGN_SYSTEM
from .services.data_service import DataService
from .services.excel_service import ExcelService


def main():
    """Função principal da aplicação."""
    # Criar janela principal
    root = tk.Tk()
    root.title("Gestão Vista")
    root.geometry("800x600")

    # Configurar estilos TTK
    setup_styles(root)

    # Configurar grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=1)

    # Criar serviços
    data_service = DataService()
    excel_service = ExcelService(data_service)

    # Criar variáveis de controle
    caracteristica_var = tk.StringVar()

    # Criar frame principal
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

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
        lambda: excel_service.load_gestao(combo),
        lambda: excel_service.load_casas(),
        lambda: excel_service.export_faltantes(caracteristica_var.get()),
        lambda: data_service.clear_gestao(),
        lambda: data_service.clear_casas(),
        lambda: excel_service.view_casas(),
    )

    # Iniciar loop principal
    root.mainloop()
