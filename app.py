import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class GestaoVistaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão à Vista - Casas de Oração")
        self.root.geometry("1200x800")

        self.df_gestao = None
        self.df_casas = None
        self.caracteristicas = []

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Botões para carregar arquivos
        ttk.Button(
            main_frame, text="Carregar Gestão à Vista", command=self.load_gestao
        ).grid(row=0, column=0, pady=5)
        ttk.Button(
            main_frame, text="Carregar Casas de Oração", command=self.load_casas
        ).grid(row=0, column=1, pady=5)

        # Frame para o gráfico
        self.graph_frame = ttk.Frame(main_frame)
        self.graph_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Combobox para selecionar característica
        ttk.Label(main_frame, text="Selecione a característica:").grid(
            row=2, column=0, pady=5
        )
        self.caracteristica_var = tk.StringVar()
        self.caracteristica_combo = ttk.Combobox(
            main_frame, textvariable=self.caracteristica_var
        )
        self.caracteristica_combo.grid(row=2, column=1, pady=5)

        # Botão para exportar faltantes
        ttk.Button(
            main_frame, text="Exportar Casas Faltantes", command=self.export_faltantes
        ).grid(row=3, column=0, columnspan=2, pady=5)

    def load_gestao(self):
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
                # Remover colunas sem nome ou com nome 'Unnamed'
                self.df_gestao = self.df_gestao.loc[
                    :, ~self.df_gestao.columns.str.contains("^Unnamed")
                ]

                # Remover colunas que são totalmente vazias
                self.df_gestao = self.df_gestao.dropna(axis=1, how="all")

                # Pegar a primeira coluna como código da casa de oração
                self.coluna_codigo = self.df_gestao.columns[0]

                # Pegar as características (todas as colunas exceto a primeira)
                self.caracteristicas = self.df_gestao.columns[1:].tolist()
                self.caracteristica_combo["values"] = self.caracteristicas

                self.plot_graph()
                messagebox.showinfo(
                    "Sucesso", "Arquivo de Gestão à Vista carregado com sucesso!"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def load_casas(self):
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

                messagebox.showinfo(
                    "Sucesso", "Arquivo de Casas de Oração carregado com sucesso!"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def plot_graph(self):
        if self.df_gestao is None:
            return

        # Limpar frame do gráfico
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Criar novo gráfico
        fig, ax = plt.subplots(figsize=(10, 6))

        # Calcular contagem de casas para cada característica
        contagens = []
        for caracteristica in self.caracteristicas:
            # Converte para string e trata valores nulos
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            # Conta valores 'X' (case insensitive)
            contagem = valores.str.upper().str.strip().eq("X").sum()
            contagens.append(contagem)

        # Criar gráfico de barras
        bars = ax.bar(range(len(self.caracteristicas)), contagens)
        ax.set_xticks(range(len(self.caracteristicas)))
        ax.set_xticklabels(self.caracteristicas, rotation=45, ha="right")
        ax.set_ylabel("Número de Casas de Oração")
        ax.set_title("Características das Casas de Oração")

        # Adicionar valores sobre as barras
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

        # Ajustar layout
        plt.tight_layout()

        # Incorporar gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_faltantes(self):
        if self.df_gestao is None:
            messagebox.showwarning(
                "Aviso", "Carregue primeiro o arquivo de Gestão à Vista!"
            )
            return

        caracteristica = self.caracteristica_var.get()
        if not caracteristica:
            messagebox.showwarning("Aviso", "Selecione uma característica!")
            return

        # Identificar casas faltantes (valores diferentes de 'X')
        valores = self.df_gestao[caracteristica].fillna("").astype(str)
        casas_faltantes = self.df_gestao[~valores.str.upper().str.strip().eq("X")][
            self.coluna_codigo
        ]

        # Se tiver o arquivo de nomes das casas, fazer o merge
        if self.df_casas is not None:
            resultado = pd.merge(
                casas_faltantes.to_frame(),
                self.df_casas,
                left_on=self.coluna_codigo,
                right_on="codigo",
                how="left",
            )
        else:
            resultado = casas_faltantes.to_frame()

        # Salvar resultado
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
        )

        if file_path:
            resultado.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    app = GestaoVistaApp(root)
    root.mainloop()
