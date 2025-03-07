import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from styles import setup_styles
from components import create_sidebar, create_main_content, create_controls


class GestaoVistaApp:
    def __init__(self, root):
        self.root = root

        # Configurar estilo e obter sistema de design primeiro
        self.design_system = setup_styles()

        # Depois configurar a janela que usa o design system
        self.setup_window()

        self.df_gestao = None
        self.df_casas = None
        self.caracteristicas = []
        self.export_container = None
        self.export_button = None

        self.setup_ui()

    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Gestão à Vista - Casas de Oração")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.design_system["colors"]["background"])

        # Configurar grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)  # Área principal maior
        self.root.grid_columnconfigure(1, weight=1)  # Sidebar menor

    def on_caracteristica_selected(self, is_valid):
        """Callback para quando uma característica é selecionada/deselecionada"""
        if self.export_container and self.export_button:
            if is_valid:
                self.export_container.grid()  # Mostrar o container
                self.export_button.configure(state="normal")
            else:
                self.export_container.grid_remove()  # Esconder o container
                self.export_button.configure(state="disabled")

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Criar componentes principais com novo design system
        self.main_frame, self.graph_frame = create_main_content(self.root)

        # Criar controles
        self.caracteristica_var = tk.StringVar()
        self.controls_frame, self.caracteristica_combo, self.feedback_label = (
            create_controls(
                self.main_frame,
                self.caracteristica_var,
                self.on_caracteristica_selected,
            )
        )

        # Criar sidebar com botão de exportar escondido inicialmente
        self.sidebar, (self.export_container, self.export_button) = create_sidebar(
            self.root, self.load_gestao, self.load_casas, self.export_faltantes
        )

    def plot_graph(self):
        """Plota o gráfico com estilo moderno"""
        if self.df_gestao is None:
            return

        # Limpar frame do gráfico
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Configurar estilo do gráfico
        plt.style.use("dark_background")
        fig, ax = plt.subplots(
            figsize=(12, 7), facecolor=self.design_system["colors"]["background"]
        )
        ax.set_facecolor(self.design_system["colors"]["surface"])

        # Calcular contagem de casas para cada característica
        contagens = []
        for caracteristica in self.caracteristicas:
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            contagem = valores.str.upper().str.strip().eq("X").sum()
            contagens.append(contagem)

        # Criar gráfico de barras com cores do design system
        colors = plt.cm.viridis(np.linspace(0, 1, len(self.caracteristicas)))
        bars = ax.bar(range(len(self.caracteristicas)), contagens, color=colors)

        # Configurar eixos e labels com estilo consistente
        ax.set_xticks(range(len(self.caracteristicas)))
        ax.set_xticklabels(
            self.caracteristicas,
            rotation=45,
            ha="right",
            fontsize=10,
            color=self.design_system["colors"]["text"]["secondary"],
        )
        ax.set_ylabel(
            "Número de Casas de Oração",
            fontsize=12,
            color=self.design_system["colors"]["text"]["primary"],
            labelpad=10,
        )
        ax.set_title(
            "Características das Casas de Oração",
            fontsize=14,
            color=self.design_system["colors"]["text"]["primary"],
            pad=20,
        )

        # Personalizar grid e bordas
        ax.grid(
            True,
            axis="y",
            linestyle="--",
            alpha=0.2,
            color=self.design_system["colors"]["border"],
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(self.design_system["colors"]["border"])
        ax.spines["bottom"].set_color(self.design_system["colors"]["border"])

        # Adicionar valores sobre as barras
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=self.design_system["colors"]["text"]["primary"],
            )

        # Ajustar layout
        plt.tight_layout()

        # Incorporar gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_success_message(self, message):
        """Mostra mensagem de sucesso estilizada"""
        messagebox.showinfo("✅ Sucesso", message)

    def show_error_message(self, message):
        """Mostra mensagem de erro estilizada"""
        messagebox.showerror("❌ Erro", message)

    def show_warning_message(self, message):
        """Mostra mensagem de aviso estilizada"""
        messagebox.showwarning("⚠️ Aviso", message)

    def load_gestao(self):
        """Carrega arquivo de Gestão à Vista"""
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo de Gestão à Vista",
            filetypes=[
                ("Arquivo Excel", "*.xls"),
                ("Arquivo Excel", "*.xlsx"),
                ("Todos os arquivos", "*.*"),
            ],
            initialdir=".",
        )
        if file_path:
            try:
                if file_path.endswith(".xls"):
                    self.df_gestao = pd.read_excel(file_path, header=14, engine="xlrd")
                else:
                    self.df_gestao = pd.read_excel(
                        file_path, header=14, engine="openpyxl"
                    )

                # Limpar e preparar o DataFrame
                self.df_gestao = self.df_gestao.loc[
                    :, ~self.df_gestao.columns.str.contains("^Unnamed")
                ]
                self.df_gestao = self.df_gestao.dropna(axis=1, how="all")
                self.coluna_codigo = self.df_gestao.columns[0]
                self.caracteristicas = self.df_gestao.columns[1:].tolist()
                self.caracteristica_combo["values"] = self.caracteristicas

                self.plot_graph()
                self.show_success_message(
                    "Arquivo de Gestão à Vista carregado com sucesso!"
                )
            except Exception as e:
                self.show_error_message(f"Erro ao carregar arquivo: {str(e)}")

    def load_casas(self):
        """Carrega arquivo de Casas de Oração"""
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo de Casas de Oração",
            filetypes=[
                ("Arquivo Excel", "*.xlsx"),
                ("Arquivo Excel", "*.xls"),
                ("Todos os arquivos", "*.*"),
            ],
            initialdir=".",
        )
        if file_path:
            try:
                if file_path.endswith(".xls"):
                    self.df_casas = pd.read_excel(file_path, engine="xlrd")
                else:
                    self.df_casas = pd.read_excel(file_path, engine="openpyxl")

                self.show_success_message(
                    "Arquivo de Casas de Oração carregado com sucesso!"
                )
            except Exception as e:
                self.show_error_message(f"Erro ao carregar arquivo: {str(e)}")

    def export_faltantes(self):
        """Exporta relatório de casas faltantes"""
        if self.df_gestao is None:
            self.show_warning_message("Carregue primeiro o arquivo de Gestão à Vista!")
            return

        caracteristica = self.caracteristica_var.get()
        if not caracteristica or caracteristica == "Escolha uma característica...":
            self.show_warning_message("Selecione uma característica para exportar!")
            return

        if caracteristica not in self.caracteristicas:
            self.show_error_message(
                f"Característica '{caracteristica}' não encontrada na planilha!"
            )
            return

        try:
            # Identificar casas faltantes
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            casas_faltantes = self.df_gestao[~valores.str.upper().str.strip().eq("X")][
                [self.coluna_codigo, caracteristica]
            ]
            casas_faltantes["Status"] = "Faltante"

            # Merge com dados das casas se disponível
            if self.df_casas is not None:
                # Mapeamento de colunas para padronização
                mapeamento_colunas = {
                    "codigo": ["codigo", "Código", "CODIGO", "CÓDIGO"],
                    "nome": ["nome", "Nome", "NOME"],
                    "endereco": [
                        "endereco",
                        "Endereco",
                        "ENDERECO",
                        "endereço",
                        "Endereço",
                        "ENDEREÇO",
                    ],
                    "bairro": ["bairro", "Bairro", "BAIRRO"],
                    "cidade": ["cidade", "Cidade", "CIDADE"],
                    "responsavel": [
                        "responsavel",
                        "Responsavel",
                        "RESPONSAVEL",
                        "responsável",
                        "Responsável",
                        "RESPONSÁVEL",
                    ],
                    "telefone": ["telefone", "Telefone", "TELEFONE"],
                }

                # Encontrar e padronizar colunas no df_casas
                colunas_encontradas = {}
                df_casas_padronizado = self.df_casas.copy()

                for coluna_padrao, variantes in mapeamento_colunas.items():
                    for variante in variantes:
                        if variante in self.df_casas.columns:
                            colunas_encontradas[coluna_padrao] = variante
                            if variante != coluna_padrao:
                                df_casas_padronizado = df_casas_padronizado.rename(
                                    columns={variante: coluna_padrao}
                                )
                            break

                if "codigo" not in colunas_encontradas:
                    self.show_warning_message(
                        "Não foi possível encontrar a coluna de código no arquivo de casas.\n"
                        "Exportando apenas os dados básicos."
                    )
                    resultado = casas_faltantes
                else:
                    # Selecionar apenas as colunas encontradas e fazer o merge
                    colunas_para_merge = ["codigo"] + [
                        col for col in colunas_encontradas.keys() if col != "codigo"
                    ]
                    colunas_df_casas = [
                        col
                        for col in colunas_para_merge
                        if col in df_casas_padronizado.columns
                    ]

                    resultado = pd.merge(
                        casas_faltantes,
                        df_casas_padronizado[colunas_df_casas],
                        left_on=self.coluna_codigo,
                        right_on="codigo",
                        how="left",
                    )

                    # Remover coluna de código duplicada se necessário
                    if (
                        "codigo" in resultado.columns
                        and resultado.columns[0] != "codigo"
                    ):
                        resultado = resultado.drop(columns=["codigo"])
            else:
                resultado = casas_faltantes

            # Salvar resultado
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title=f"Salvar relatório de casas faltantes - {caracteristica}",
                initialfile=f"casas_faltantes_{caracteristica.lower().replace(' ', '_')}.xlsx",
            )

            if file_path:
                # Definir ordem das colunas
                colunas_ordem = [
                    self.coluna_codigo,  # Código sempre primeiro
                    "nome",
                    "endereco",
                    "bairro",
                    "cidade",
                    "responsavel",
                    "telefone",
                    caracteristica,
                    "Status",
                ]

                # Filtrar apenas as colunas que existem
                colunas_ordem = [
                    col for col in colunas_ordem if col in resultado.columns
                ]
                resultado = resultado[colunas_ordem]

                # Formatar e salvar o Excel
                with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                    resultado.to_excel(
                        writer, index=False, sheet_name="Casas Faltantes"
                    )
                    # Ajustar largura das colunas
                    worksheet = writer.sheets["Casas Faltantes"]
                    for idx, col in enumerate(resultado.columns):
                        max_length = max(
                            resultado[col].astype(str).apply(len).max(), len(str(col))
                        )
                        worksheet.column_dimensions[chr(65 + idx)].width = (
                            max_length + 2
                        )

                self.show_success_message(
                    f"Relatório exportado com sucesso!\n"
                    f"Total de casas faltantes: {len(resultado)}"
                )
        except Exception as e:
            print(f"Erro detalhado: {str(e)}")  # Debug detalhado
            self.show_error_message(f"Erro ao exportar relatório: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GestaoVistaApp(root)
    root.mainloop()
