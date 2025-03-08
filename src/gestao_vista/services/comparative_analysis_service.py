import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from tkinter import messagebox, filedialog
import os
from datetime import datetime

from ..utils.constants import is_documento_obrigatorio
from ..utils.design_system import DESIGN_SYSTEM


class ComparativeAnalysisService:
    def __init__(self):
        """Inicializa o serviço de análise comparativa."""
        self.current_data = None
        self.comparison_data = None
        self.comparison_label = None

    def set_current_data(self, df: pd.DataFrame):
        """Define os dados atuais para comparação."""
        self.current_data = df

    def set_comparison_data(self, df: pd.DataFrame, label: str):
        """Define os dados para comparação e seu rótulo."""
        self.comparison_data = df
        self.comparison_label = label

    def generate_comparative_analysis(self) -> bool:
        """
        Gera uma análise comparativa entre dois períodos.

        Returns:
            bool: True se a análise foi gerada com sucesso, False caso contrário.
        """
        if self.current_data is None or self.comparison_data is None:
            messagebox.showerror(
                "❌ Erro", "Dados insuficientes para gerar análise comparativa."
            )
            return False

        try:
            # Preparar dados para análise
            current_counts = self._count_documents(self.current_data)
            comparison_counts = self._count_documents(self.comparison_data)

            # Calcular diferenças
            differences = {}
            for doc in set(current_counts.keys()) | set(comparison_counts.keys()):
                current = current_counts.get(doc, 0)
                previous = comparison_counts.get(doc, 0)
                differences[doc] = current - previous

            # Ordenar por magnitude da diferença
            sorted_differences = sorted(
                differences.items(), key=lambda x: abs(x[1]), reverse=True
            )

            # Criar figura
            plt.style.use("dark_background")
            fig, (ax1, ax2) = plt.subplots(
                2,
                1,
                figsize=(15, 12),
                gridspec_kw={"height_ratios": [2, 1]},
                facecolor=DESIGN_SYSTEM["colors"]["background"]["default"],
            )

            # Gráfico de barras comparativo
            docs = [item[0] for item in sorted_differences]
            current_values = [current_counts.get(doc, 0) for doc in docs]
            comparison_values = [comparison_counts.get(doc, 0) for doc in docs]

            x = np.arange(len(docs))
            width = 0.35

            ax1.bar(
                x - width / 2,
                comparison_values,
                width,
                label=self.comparison_label,
                color=DESIGN_SYSTEM["colors"]["primary"],
            )
            ax1.bar(
                x + width / 2,
                current_values,
                width,
                label="Atual",
                color=DESIGN_SYSTEM["colors"]["secondary"],
            )

            # Configurar primeiro gráfico
            ax1.set_ylabel("Quantidade de Casas", fontsize=12)
            ax1.set_title("Comparação por Documento", fontsize=14, pad=20)
            ax1.set_xticks(x)
            ax1.set_xticklabels(docs, rotation=45, ha="right")
            ax1.legend()
            ax1.grid(True, alpha=0.2)

            # Gráfico de diferenças
            differences_values = [item[1] for item in sorted_differences]
            colors = ["#2ecc71" if d > 0 else "#e74c3c" for d in differences_values]

            ax2.bar(x, differences_values, color=colors)
            ax2.set_ylabel("Diferença (Atual - Anterior)", fontsize=12)
            ax2.set_title("Diferença entre Períodos", fontsize=14, pad=20)
            ax2.set_xticks(x)
            ax2.set_xticklabels(docs, rotation=45, ha="right")
            ax2.grid(True, alpha=0.2)

            # Adicionar valores nas barras do gráfico de diferenças
            for i, v in enumerate(differences_values):
                color = "white"
                ax2.text(
                    i,
                    v + (0.5 if v >= 0 else -0.5),
                    str(v),
                    ha="center",
                    va="bottom" if v >= 0 else "top",
                    color=color,
                    fontweight="bold",
                )

            # Ajustar layout
            plt.tight_layout()

            # Abrir diálogo para salvar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("PDF files", "*.pdf"),
                ],
                title="Salvar análise comparativa como",
                initialfile=f"analise_comparativa_{self.comparison_label.replace('/', '_')}.png",
            )

            if file_path:
                # Salvar figura
                fig.savefig(
                    file_path,
                    facecolor=fig.get_facecolor(),
                    bbox_inches="tight",
                    dpi=300,
                )

                plt.close(fig)

                messagebox.showinfo(
                    "✅ Sucesso", "Análise comparativa gerada com sucesso!"
                )
                return True

            plt.close(fig)
            return False

        except Exception as e:
            messagebox.showerror(
                "❌ Erro", f"Erro ao gerar análise comparativa: {str(e)}"
            )
            return False

    def _count_documents(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Conta a quantidade de documentos marcados com 'X' para cada característica.

        Args:
            df: DataFrame com os dados do Gestão à Vista

        Returns:
            Dict[str, int]: Dicionário com as contagens de cada documento
        """
        counts = {}
        for col in df.columns[1:]:  # Ignora a primeira coluna (código)
            count = df[col].fillna("").astype(str).str.upper().str.strip().eq("X").sum()
            counts[col] = count
        return counts
