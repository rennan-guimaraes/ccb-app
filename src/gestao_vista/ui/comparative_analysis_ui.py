import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from ..services.comparative_analysis_service import ComparativeAnalysisService
from ..services.data_service import DataService
from ..utils.design_system import DESIGN_SYSTEM
from ..ui.components import create_button


class ComparativeAnalysisUI:
    def __init__(self, data_service: DataService):
        """
        Inicializa a interface de análise comparativa.

        Args:
            data_service: Serviço de dados para carregar arquivos
        """
        self.data_service = data_service
        self.comparative_service = ComparativeAnalysisService()

    def show_dialog(self, current_data: pd.DataFrame):
        """
        Mostra o diálogo de análise comparativa.

        Args:
            current_data: DataFrame com os dados atuais
        """
        # Configurar serviço com dados atuais
        self.comparative_service.set_current_data(current_data)

        # Criar janela de diálogo
        dialog = tk.Toplevel()
        dialog.title("Análise Comparativa")
        dialog.geometry("500x300")
        dialog.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

        # Tornar a janela modal
        dialog.transient(dialog.master)
        dialog.grab_set()

        # Frame principal
        main_frame = ttk.Frame(dialog, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Label de título
        ttk.Label(
            main_frame,
            text="Análise Comparativa de Gestão à Vista",
            style="Header.TLabel",
        ).pack(pady=(0, 20))

        # Frame para entrada do nome
        name_frame = ttk.Frame(main_frame, style="Card.TFrame")
        name_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            name_frame,
            text="Nome para o período de comparação:",
            style="Default.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 10))

        name_entry = ttk.Entry(name_frame)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        name_entry.insert(0, "Período Anterior")

        # Frame para o arquivo
        file_frame = ttk.Frame(main_frame, style="Card.TFrame")
        file_frame.pack(fill=tk.X, pady=(0, 20))

        self.file_label = ttk.Label(
            file_frame, text="Nenhum arquivo selecionado", style="Default.TLabel"
        )
        self.file_label.pack(side=tk.LEFT, padx=(0, 10))

        def select_file():
            file_path = filedialog.askopenfilename(
                title="Selecione o arquivo de Gestão à Vista para comparação",
                filetypes=[
                    ("Arquivo Excel", "*.xls"),
                    ("Arquivo Excel", "*.xlsx"),
                    ("Todos os arquivos", "*.*"),
                ],
            )

            if file_path:
                try:
                    comparison_data = self.data_service.import_gestao_from_excel(
                        file_path,
                        should_save=False,  # Não salvar os dados de comparação
                    )
                    if comparison_data is not None:
                        self.comparative_service.set_comparison_data(
                            comparison_data,
                            name_entry.get().strip() or "Período Anterior",
                        )
                        self.file_label.config(
                            text=f"Arquivo selecionado: {file_path.split('/')[-1]}"
                        )
                        generate_btn.configure(state="normal")
                except Exception as e:
                    messagebox.showerror(
                        "❌ Erro", f"Erro ao carregar arquivo: {str(e)}"
                    )

        select_btn = create_button(
            file_frame, "Selecionar Arquivo", select_file, "primary"
        )
        select_btn.pack(side=tk.RIGHT)

        # Botão de gerar análise
        generate_btn = create_button(
            main_frame,
            "Gerar Análise",
            lambda: self._generate_analysis(name_entry.get().strip(), dialog),
            "primary",
        )
        generate_btn.configure(state="disabled")
        generate_btn.pack(pady=20)

        # Centralizar janela
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def _generate_analysis(self, comparison_name: str, dialog: tk.Toplevel):
        """
        Gera a análise comparativa.

        Args:
            comparison_name: Nome do período de comparação
            dialog: Janela de diálogo para fechar após gerar
        """
        # Atualizar nome do período de comparação
        self.comparative_service.comparison_label = (
            comparison_name or "Período Anterior"
        )

        # Gerar análise
        if self.comparative_service.generate_comparative_analysis():
            dialog.destroy()
