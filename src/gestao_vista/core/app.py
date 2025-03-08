import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Optional, List, Dict, Any, Callable

from ..models.casa_oracao import CasaOracao
from ..services.data_service import DataService
from ..services.graph_service import GraphService
from ..services.casa_oracao_service import CasaOracaoService
from ..services.report_service import ReportService
from ..ui.casa_oracao_ui import CasaOracaoUI
from ..utils.design_system import DESIGN_SYSTEM, setup_styles
from ..utils.constants import is_documento_obrigatorio
from ..ui.components import (
    create_sidebar,
    create_main_content,
    create_controls,
    create_dialog_window,
    create_form_field,
    create_button,
)


class GestaoVistaApp:
    def __init__(self, root: tk.Tk):
        """
        Inicializa a aplicação Gestão à Vista.

        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.setup_window()

        # Configurar tema escuro para o matplotlib
        plt.style.use("dark_background")

        # Inicializar variáveis
        self.df_gestao: Optional[pd.DataFrame] = None
        self.casas: List[CasaOracao] = []
        self.caracteristicas: List[str] = []
        self.export_container: Optional[ttk.Frame] = None
        self.export_button: Optional[tk.Button] = None
        self.caracteristica_combo: Optional[ttk.Combobox] = None
        self.caracteristica_var = tk.StringVar()
        self.coluna_codigo: Optional[str] = None

        # Inicializar serviços
        self.data_service = DataService()
        self.casa_oracao_service = CasaOracaoService(self.data_service)
        self.casa_oracao_ui = CasaOracaoUI(self.casa_oracao_service)
        self.report_service = None  # Será inicializado após carregar os dados
        self.graph_service = GraphService()

        # Carregar dados salvos
        self.load_saved_data()

        # Configurar interface
        self.setup_ui()

        # Atualizar interface com dados carregados
        self.update_ui_with_data()

    def setup_window(self):
        """Configura a janela principal"""
        setup_styles()
        self.root.title("Gestão à Vista - Casas de Oração")
        self.root.geometry("1400x900")
        self.root.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

        # Configurar grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)  # Área principal maior
        self.root.grid_columnconfigure(1, weight=1)  # Sidebar menor

    def load_saved_data(self):
        """Carrega os dados salvos"""
        self.df_gestao = self.data_service.load_gestao()
        self.casas = self.casa_oracao_service.load_casas()

        if self.df_gestao is not None and not self.df_gestao.empty:
            self.caracteristicas = self.df_gestao.columns[1:].tolist()
            self.coluna_codigo = self.df_gestao.columns[0]
        else:
            self.caracteristicas = []
            self.coluna_codigo = None
            # Criar DataFrame vazio com estrutura básica
            self.df_gestao = pd.DataFrame(columns=["codigo"])

        # Inicializar ReportService após carregar os dados
        self.report_service = ReportService(self.df_gestao, self.casas)

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Criar componentes principais
        self.main_frame, self.graph_frame = create_main_content(self.root)

        # Criar controles
        self.controls_frame, self.caracteristica_combo, self.feedback_label = (
            create_controls(
                self.main_frame,
                self.caracteristica_var,
                self.on_caracteristica_selected,
            )
        )

        # Criar sidebar
        self.sidebar, (self.export_container, self.export_button) = create_sidebar(
            self.root,
            self.load_gestao_file,
            self.casa_oracao_service.load_casas_file,
            self.export_faltantes,
            self.clear_gestao,
            self.casa_oracao_service.clear_casas,
            lambda: self.casa_oracao_ui.view_casas(self.root),
        )

    def update_ui_with_data(self):
        """Atualiza a interface com os dados carregados"""
        if self.df_gestao is not None:
            self.caracteristica_combo["values"] = self.caracteristicas
            self.plot_graph()

    def on_caracteristica_selected(self, is_valid: bool):
        """Callback para quando uma característica é selecionada"""
        if self.export_container and self.export_button:
            if is_valid:
                self.export_container.pack(fill=tk.X, padx=10, pady=5)
                self.export_button.configure(state="normal")
            else:
                self.export_container.pack_forget()
                self.export_button.configure(state="disabled")

    def export_graph(self, fig):
        """Exporta o gráfico como imagem"""
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
            ],
            title="Salvar gráfico como",
            initialfile="grafico_gestao_vista.png",
        )

        if file_path:
            try:
                fig.savefig(
                    file_path,
                    facecolor=fig.get_facecolor(),
                    bbox_inches="tight",
                    dpi=300,
                )
                messagebox.showinfo("✅ Sucesso", "Gráfico exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao exportar gráfico: {str(e)}")

    def plot_graph(self):
        """Plota o gráfico com os dados atuais"""
        if self.df_gestao is not None:
            self.graph_service.plot_graph(
                self.graph_frame,
                self.df_gestao,
                self.caracteristicas,
                len(self.df_gestao),
            )

    def load_gestao_file(self):
        """Carrega arquivo de Gestão à Vista"""
        file_path = tk.filedialog.askopenfilename(
            title="Selecione o arquivo de Gestão à Vista",
            filetypes=[
                ("Arquivo Excel", "*.xls"),
                ("Arquivo Excel", "*.xlsx"),
                ("Todos os arquivos", "*.*"),
            ],
            initialdir=".",
        )

        if file_path:
            self.df_gestao = self.data_service.import_gestao_from_excel(file_path)
            if self.df_gestao is not None:
                self.caracteristicas = self.df_gestao.columns[1:].tolist()
                self.coluna_codigo = self.df_gestao.columns[0]
                self.report_service = ReportService(self.df_gestao, self.casas)
                self.update_ui_with_data()
                messagebox.showinfo(
                    "✅ Sucesso", "Arquivo de Gestão à Vista carregado com sucesso!"
                )

    def clear_gestao(self):
        """Limpa os dados de Gestão à Vista"""
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente limpar os dados de Gestão à Vista?"
        ):
            if self.data_service.clear_gestao():
                self.df_gestao = None
                self.caracteristicas = []
                self.caracteristica_combo["values"] = []
                self.caracteristica_var.set("Escolha uma característica...")
                self.report_service = None

                # Limpar gráfico
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()

                messagebox.showinfo(
                    "✅ Sucesso", "Dados de Gestão à Vista limpos com sucesso!"
                )

    def export_faltantes(self):
        """Exporta relatório de casas faltantes"""
        if self.df_gestao is None:
            messagebox.showwarning(
                "⚠️ Aviso", "Carregue primeiro o arquivo de Gestão à Vista!"
            )
            return

        caracteristica = self.caracteristica_var.get()
        if not caracteristica or caracteristica == "Escolha uma característica...":
            messagebox.showwarning(
                "⚠️ Aviso", "Selecione uma característica para exportar!"
            )
            return

        if caracteristica not in self.caracteristicas:
            messagebox.showerror(
                "❌ Erro",
                f"Característica '{caracteristica}' não encontrada na planilha!",
            )
            return

        self.report_service.export_faltantes(caracteristica, self.coluna_codigo)
