import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from ..utils.design_system import DESIGN_SYSTEM
from ..utils.constants import is_documento_obrigatorio
from ..ui.components import create_button


class GraphService:
    @staticmethod
    def plot_graph(
        graph_frame: ttk.Frame,
        df_gestao: pd.DataFrame,
        caracteristicas: list,
        total_casas: int,
    ):
        """Plota o gráfico com os dados atuais"""
        if df_gestao is None or df_gestao.empty or not caracteristicas:
            # Limpar frame do gráfico
            for widget in graph_frame.winfo_children():
                widget.destroy()

            # Mostrar mensagem quando não há dados
            ttk.Label(
                graph_frame,
                text="Nenhum dado disponível.\nImporte um arquivo de Gestão à Vista para visualizar o gráfico.",
                style="SubHeader.TLabel",
                justify=tk.CENTER,
            ).pack(expand=True)
            return

        # Limpar frame do gráfico
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Criar frame para o gráfico e controles
        controls_frame = ttk.Frame(graph_frame, style="Card.TFrame")
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        graph_container = ttk.Frame(graph_frame, style="Card.TFrame")
        graph_container.pack(fill=tk.BOTH, expand=True)

        # Configurar gráfico
        fig, ax = plt.subplots(
            figsize=(12, 7), facecolor=DESIGN_SYSTEM["colors"]["background"]["default"]
        )
        ax.set_facecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])

        # Separar características em obrigatórias e opcionais
        caracteristicas_obrigatorias = []
        caracteristicas_opcionais = []
        contagens_obrigatorias = []
        contagens_opcionais = []
        cores_obrigatorias = []
        cores_opcionais = []

        # Classificar características
        for caracteristica in caracteristicas:
            valores = df_gestao[caracteristica].fillna("").astype(str)
            contagem = valores.str.upper().str.strip().eq("X").sum()

            if is_documento_obrigatorio(caracteristica):
                caracteristicas_obrigatorias.append(caracteristica)
                contagens_obrigatorias.append(contagem)
                cores_obrigatorias.append(DESIGN_SYSTEM["colors"]["error"])
            else:
                caracteristicas_opcionais.append(caracteristica)
                contagens_opcionais.append(contagem)
                cores_opcionais.append(DESIGN_SYSTEM["colors"]["primary"])

        # Ordenar obrigatórios por contagem (maior para menor)
        indices_ordenados_obrig = np.argsort(contagens_obrigatorias)[::-1]
        caracteristicas_obrigatorias = [
            caracteristicas_obrigatorias[i] for i in indices_ordenados_obrig
        ]
        contagens_obrigatorias = [
            contagens_obrigatorias[i] for i in indices_ordenados_obrig
        ]
        cores_obrigatorias = [cores_obrigatorias[i] for i in indices_ordenados_obrig]

        # Ordenar opcionais por contagem (maior para menor)
        indices_ordenados_opc = np.argsort(contagens_opcionais)[::-1]
        caracteristicas_opcionais = [
            caracteristicas_opcionais[i] for i in indices_ordenados_opc
        ]
        contagens_opcionais = [contagens_opcionais[i] for i in indices_ordenados_opc]
        cores_opcionais = [cores_opcionais[i] for i in indices_ordenados_opc]

        # Combinar listas mantendo a ordem (obrigatórios à esquerda, opcionais à direita)
        todas_caracteristicas = caracteristicas_obrigatorias + caracteristicas_opcionais
        todas_contagens = contagens_obrigatorias + contagens_opcionais
        todas_cores = cores_obrigatorias + cores_opcionais

        # Criar gráfico
        bars = ax.bar(
            range(len(todas_caracteristicas)), todas_contagens, color=todas_cores
        )

        # Configurar eixos e labels
        ax.set_xticks(range(len(todas_caracteristicas)))
        ax.set_xticklabels(
            todas_caracteristicas,
            rotation=45,
            ha="right",
            fontsize=10,
            color=DESIGN_SYSTEM["colors"]["text"]["secondary"],
        )

        ax.set_ylabel(
            "Número de Casas de Oração",
            fontsize=12,
            color=DESIGN_SYSTEM["colors"]["text"]["primary"],
            labelpad=10,
        )

        ax.set_title(
            "Características das Casas de Oração\n(Documentos obrigatórios em vermelho à esquerda, ordenados de maior para menor)",
            fontsize=14,
            color=DESIGN_SYSTEM["colors"]["text"]["primary"],
            pad=20,
        )

        # Personalizar grid e bordas
        ax.grid(
            True,
            axis="y",
            linestyle="--",
            alpha=0.2,
            color=DESIGN_SYSTEM["colors"]["border"],
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(DESIGN_SYSTEM["colors"]["border"])
        ax.spines["bottom"].set_color(DESIGN_SYSTEM["colors"]["border"])

        # Adicionar valores e porcentagens sobre as barras
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total_casas) * 100
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}\n({percentage:.1f}%)",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=DESIGN_SYSTEM["colors"]["text"]["primary"],
            )

        # Ajustar layout
        plt.tight_layout()

        # Adicionar botão de exportação
        export_btn = create_button(
            controls_frame,
            "📸 Exportar Gráfico",
            lambda: GraphService.export_graph(fig),
            "primary",
        )
        export_btn.pack(side=tk.RIGHT, padx=5)

        # Criar canvas e exibir
        canvas = FigureCanvasTkAgg(fig, master=graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    @staticmethod
    def export_graph(fig):
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
