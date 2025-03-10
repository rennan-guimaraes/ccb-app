import tkinter as tk
from tkinter import messagebox
import pandas as pd
from typing import List

from gestao_vista.models.casa_oracao import CasaOracao


class ReportService:
    def __init__(self, df_gestao: pd.DataFrame, casas: List[CasaOracao]):
        self.df_gestao = df_gestao
        self.casas = casas

    def export_faltantes(self, caracteristica: str, coluna_codigo: str):
        """
        Exporta relatório de casas faltantes para uma característica específica.

        Args:
            caracteristica: Característica a ser analisada
            coluna_codigo: Nome da coluna que contém o código das casas
        """
        try:
            # Identificar casas faltantes
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            casas_faltantes = self.df_gestao[~valores.str.upper().str.strip().eq("X")][
                [coluna_codigo, caracteristica]
            ]
            casas_faltantes["Status"] = "Faltante"

            # Preparar dados para exportação
            dados_export = []
            for _, row in casas_faltantes.iterrows():
                codigo = str(row[coluna_codigo])
                casa = next((c for c in self.casas if c.codigo == codigo), None)

                if casa:
                    dados_export.append(
                        {
                            "codigo": codigo,
                            "nome": casa.nome,
                            "endereco": casa.endereco,
                            "tipo_imovel": casa.tipo_imovel,
                            "observacoes": casa.observacoes,
                            "status": casa.status,
                            caracteristica: row[caracteristica],
                            "Status": "Faltante",
                        }
                    )
                else:
                    dados_export.append(
                        {
                            "codigo": codigo,
                            caracteristica: row[caracteristica],
                            "Status": "Faltante",
                        }
                    )

            # Criar DataFrame para exportação
            df_export = pd.DataFrame(dados_export)

            # Salvar arquivo
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title=f"Salvar relatório de casas faltantes - {caracteristica}",
                initialfile=f"casas_faltantes_{caracteristica.lower().replace(' ', '_')}.xlsx",
            )

            if file_path:
                with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                    df_export.to_excel(
                        writer, index=False, sheet_name="Casas Faltantes"
                    )

                    # Ajustar largura das colunas
                    worksheet = writer.sheets["Casas Faltantes"]
                    for idx, col in enumerate(df_export.columns):
                        max_length = max(
                            df_export[col].astype(str).apply(len).max(), len(str(col))
                        )
                        worksheet.column_dimensions[chr(65 + idx)].width = (
                            max_length + 2
                        )

                messagebox.showinfo(
                    "✅ Sucesso",
                    f"Relatório exportado com sucesso!\n"
                    f"Total de casas faltantes: {len(df_export)}",
                )
                return True
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao exportar relatório: {str(e)}")
            return False
