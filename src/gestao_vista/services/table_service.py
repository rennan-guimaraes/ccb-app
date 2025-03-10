import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from typing import List, Optional
import matplotlib

matplotlib.use("Agg")  # Usar backend não-interativo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from gestao_vista.utils.design_system import DESIGN_SYSTEM
from gestao_vista.models.casa_oracao import CasaOracao
from gestao_vista.ui.components import create_button
from gestao_vista.utils.constants import is_documento_obrigatorio
from gestao_vista.services.observacao_service import ObservacaoService


class TableService:
    def __init__(self):
        self.observacao_service = ObservacaoService()

    @staticmethod
    def plot_table(
        table_frame: ttk.Frame,
        df_gestao: pd.DataFrame,
        casas: List[CasaOracao],
        caracteristicas: list,
    ):
        """Plota a tabela com os dados atuais"""
        if df_gestao is None or df_gestao.empty or not caracteristicas:
            # Limpar frame da tabela
            for widget in table_frame.winfo_children():
                widget.destroy()

            # Mostrar mensagem quando não há dados
            ttk.Label(
                table_frame,
                text="Nenhum dado disponível.\nImporte um arquivo de Gestão à Vista para visualizar a tabela.",
                style="SubHeader.TLabel",
                justify=tk.CENTER,
            ).pack(expand=True)
            return

        # Limpar frame da tabela
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Criar frame para a tabela e controles
        controls_frame = ttk.Frame(table_frame, style="Card.TFrame")
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Botão de exportação
        export_btn = create_button(
            controls_frame,
            "📸 Exportar Tabela",
            lambda: TableService.export_table(fig),
            "primary",
        )
        export_btn.pack(side=tk.RIGHT, padx=5)

        # Frame para conter o canvas com scroll
        canvas_frame = ttk.Frame(table_frame, style="Card.TFrame")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar canvas para scroll
        canvas = tk.Canvas(
            canvas_frame,
            bg=DESIGN_SYSTEM["colors"]["background"]["paper"],
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(
            canvas_frame, orient="horizontal", command=canvas.xview
        )

        # Frame dentro do canvas que vai conter a tabela
        table_container = ttk.Frame(canvas, style="Card.TFrame")

        # Configurar scroll
        canvas.configure(
            yscrollcommand=scrollbar.set,
            xscrollcommand=scrollbar_x.set,
        )

        # Posicionar elementos
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Criar janela no canvas
        canvas.create_window((0, 0), window=table_container, anchor="nw")

        # Configurar figura com tamanho ajustado
        fig, ax = plt.subplots(
            figsize=(16, len(casas) * 0.3),
            facecolor=DESIGN_SYSTEM["colors"]["background"]["default"],
        )
        ax.set_facecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])

        # Preparar dados para a tabela
        nomes_casas = []
        dados_tabela = []

        for casa in casas:
            nomes_casas.append(casa.nome)
            linha = []
            for caracteristica in caracteristicas:
                valor = df_gestao[df_gestao.iloc[:, 0] == casa.codigo][
                    caracteristica
                ].iloc[0]
                tem_documento = str(valor).strip().upper() == "X"
                linha.append(1 if tem_documento else 0)
            dados_tabela.append(linha)

        # Criar tabela
        table = ax.table(
            cellText=[[" " for _ in caracteristicas] for _ in nomes_casas],
            rowLabels=nomes_casas,
            colLabels=caracteristicas,
            cellColours=[
                [
                    (
                        DESIGN_SYSTEM["colors"]["success"]
                        if valor
                        else DESIGN_SYSTEM["colors"]["error"]
                    )
                    for valor in linha
                ]
                for linha in dados_tabela
            ],
            loc="center",
            cellLoc="center",
            colWidths=[0.1] * (len(caracteristicas) + 1),  # +1 para a coluna de nomes
        )

        # Configurar aparência da tabela
        table.auto_set_font_size(False)
        table.set_fontsize(12)  # Aumentado o tamanho base da fonte

        # Ajustar cores e estilos das células
        for pos, cell in table._cells.items():
            if pos[1] == -1:  # Células da primeira coluna (nomes das casas)
                cell.set_text_props(
                    color=DESIGN_SYSTEM["colors"]["text"]["primary"], weight="bold"
                )
                cell.set_facecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])
            elif pos[0] == 0:  # Cabeçalhos das colunas
                cell.set_text_props(
                    color=DESIGN_SYSTEM["colors"]["text"]["primary"], weight="bold"
                )
                cell.set_facecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])
            else:
                cell.set_text_props(color=DESIGN_SYSTEM["colors"]["text"]["primary"])

            # Remover bordas entre células
            cell.set_edgecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])

        # Ajustar layout
        ax.axis("off")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remover margens

        # Criar canvas matplotlib e exibir
        canvas_plot = FigureCanvasTkAgg(fig, master=table_container)
        canvas_plot.draw()
        canvas_widget = canvas_plot.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Configurar scroll após a tabela ser criada
        table_container.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Configurar eventos do mouse para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    @staticmethod
    def export_table(fig):
        """Exporta a tabela como imagem"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
            ],
            title="Salvar tabela como",
            initialfile="tabela_gestao_vista.png",
        )

        if file_path:
            try:
                fig.savefig(
                    file_path,
                    facecolor=fig.get_facecolor(),
                    bbox_inches="tight",
                    dpi=300,
                )
                messagebox.showinfo("✅ Sucesso", "Tabela exportada com sucesso!")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao exportar tabela: {str(e)}")

    @staticmethod
    def export_table_view(
        df_gestao: pd.DataFrame,
        casas: List[CasaOracao],
        caracteristicas: list,
    ):
        """Exporta a visualização em tabela diretamente"""
        if df_gestao is None or df_gestao.empty or not caracteristicas:
            messagebox.showwarning(
                "⚠️ Aviso",
                "Nenhum dado disponível.\nImporte um arquivo de Gestão à Vista primeiro.",
            )
            return

        try:
            # Inicializar ObservacaoService
            observacao_service = ObservacaoService()

            # Separar características em obrigatórias e opcionais
            caracteristicas_obrigatorias = []
            caracteristicas_opcionais = []

            for caracteristica in caracteristicas:
                if is_documento_obrigatorio(caracteristica):
                    caracteristicas_obrigatorias.append(caracteristica)
                else:
                    caracteristicas_opcionais.append(caracteristica)

            # Preparar dados para a tabela
            nomes_casas = []
            dados_obrigatorios = []
            dados_opcionais = []
            percentuais_obrigatorios = []
            percentuais_opcionais = []

            for casa in casas:
                # Carregar observações para esta casa
                observacoes = observacao_service.listar_observacoes_por_casa(
                    casa.codigo
                )
                documentos_com_observacao = {obs.documento for obs in observacoes}

                nomes_casas.append(casa.nome)

                # Processar documentos obrigatórios
                linha_obrig = []
                total_obrig = 0
                for caracteristica in caracteristicas_obrigatorias:
                    valor = df_gestao[df_gestao.iloc[:, 0] == casa.codigo][
                        caracteristica
                    ].iloc[0]
                    tem_documento = str(valor).strip().upper() == "X"
                    linha_obrig.append(1 if tem_documento else 0)
                    if tem_documento:
                        total_obrig += 1
                dados_obrigatorios.append(linha_obrig)

                # Calcular percentual obrigatórios
                perc_obrig = (
                    (total_obrig / len(caracteristicas_obrigatorias) * 100)
                    if caracteristicas_obrigatorias
                    else 0
                )
                percentuais_obrigatorios.append(f"{perc_obrig:.1f}%")

                # Processar documentos opcionais
                linha_opc = []
                total_opc = 0
                for caracteristica in caracteristicas_opcionais:
                    valor = df_gestao[df_gestao.iloc[:, 0] == casa.codigo][
                        caracteristica
                    ].iloc[0]
                    tem_documento = str(valor).strip().upper() == "X"
                    linha_opc.append(1 if tem_documento else 0)
                    if tem_documento:
                        total_opc += 1
                dados_opcionais.append(linha_opc)

                # Calcular percentual opcionais
                perc_opc = (
                    (total_opc / len(caracteristicas_opcionais) * 100)
                    if caracteristicas_opcionais
                    else 0
                )
                percentuais_opcionais.append(f"{perc_opc:.1f}%")

            # Configurar figura com tamanho ajustado
            fig_width = max(
                32,  # Largura mínima aumentada para dar mais espaço entre as tabelas
                (len(caracteristicas_obrigatorias) + len(caracteristicas_opcionais))
                * 0.8,  # Aumentado para dar mais espaço
            )
            fig_height = (
                len(casas) // 2 + len(casas) % 2
            ) * 0.3 + 2  # Aumentada altura por linha e margem

            # Criar figura com mais espaço entre os subplots
            fig, (ax1, ax2) = plt.subplots(
                1,
                2,  # 1 linha, 2 colunas
                figsize=(fig_width, fig_height),
                facecolor="white",  # Fundo branco
                gridspec_kw={"wspace": 0.2},  # Reduzir espaço entre as tabelas
            )

            # Dividir os dados em duas partes
            metade = len(casas) // 2 + len(casas) % 2
            nomes_casas_1 = nomes_casas[:metade]
            nomes_casas_2 = nomes_casas[metade:]
            dados_obrigatorios_1 = dados_obrigatorios[:metade]
            dados_obrigatorios_2 = dados_obrigatorios[metade:]
            dados_opcionais_1 = dados_opcionais[:metade]
            dados_opcionais_2 = dados_opcionais[metade:]
            percentuais_obrigatorios_1 = percentuais_obrigatorios[:metade]
            percentuais_obrigatorios_2 = percentuais_obrigatorios[metade:]
            percentuais_opcionais_1 = percentuais_opcionais[:metade]
            percentuais_opcionais_2 = percentuais_opcionais[metade:]

            # Preparar cabeçalhos
            headers = ["Casa de Oração"]
            headers.extend(caracteristicas_obrigatorias)
            headers.append("% Obrig.")
            headers.append("")  # Coluna de espaço
            headers.extend(caracteristicas_opcionais)
            headers.append("% Opc.")

            # Função auxiliar para criar tabela
            def criar_tabela(
                ax, nomes, dados_obrig, dados_opc, perc_obrig, perc_opc, casas_indices
            ):
                # Calcular largura ideal para coluna de nomes
                nome_mais_longo = max(nomes, key=len)
                largura_nome = max(
                    0.15, len(nome_mais_longo) * 0.01
                )  # Reduzido ainda mais o fator de multiplicação e largura mínima

                # Calcular número total de colunas
                n_cols = (
                    1  # Casa de Oração
                    + len(caracteristicas_obrigatorias)  # Docs obrigatórios
                    + 1  # % Obrig
                    + 1  # Espaço
                    + len(caracteristicas_opcionais)  # Docs opcionais
                    + 1  # % Opc
                )

                # Definir larguras das colunas
                col_widths = []
                col_widths.append(largura_nome)  # Coluna de nomes ajustada
                col_widths.extend(
                    [0.05] * len(caracteristicas_obrigatorias)
                )  # Reduzido para 0.05
                col_widths.append(0.08)  # Percentual obrigatórios
                col_widths.append(0.03)  # Espaço entre grupos
                col_widths.extend(
                    [0.05] * len(caracteristicas_opcionais)
                )  # Reduzido para 0.05
                col_widths.append(0.08)  # Percentual opcionais

                # Preparar cores das células
                cell_colors = []
                for i, casa_idx in enumerate(casas_indices):
                    casa = casas[casa_idx]
                    observacoes = observacao_service.listar_observacoes_por_casa(
                        casa.codigo
                    )
                    documentos_com_observacao = {obs.documento for obs in observacoes}

                    row_colors = [DESIGN_SYSTEM["colors"]["background"]["paper"]]

                    # Cores para documentos obrigatórios
                    for j, valor in enumerate(dados_obrig[i]):
                        doc = caracteristicas_obrigatorias[j]
                        if valor:  # Tem o documento
                            row_colors.append(DESIGN_SYSTEM["colors"]["success"])
                        else:  # Não tem o documento
                            if doc in documentos_com_observacao:
                                row_colors.append(
                                    "#FFA726"
                                )  # Laranja para documentos com observação
                            else:
                                row_colors.append(DESIGN_SYSTEM["colors"]["error"])

                    row_colors.append(DESIGN_SYSTEM["colors"]["background"]["paper"])
                    row_colors.append(DESIGN_SYSTEM["colors"]["background"]["default"])

                    # Cores para documentos opcionais
                    for j, valor in enumerate(dados_opc[i]):
                        doc = caracteristicas_opcionais[j]
                        if valor:  # Tem o documento
                            row_colors.append(DESIGN_SYSTEM["colors"]["success"])
                        else:  # Não tem o documento
                            if doc in documentos_com_observacao:
                                row_colors.append(
                                    "#FFA726"
                                )  # Laranja para documentos com observação
                            else:
                                row_colors.append(DESIGN_SYSTEM["colors"]["error"])

                    row_colors.append(DESIGN_SYSTEM["colors"]["background"]["paper"])
                    cell_colors.append(row_colors)

                # Preparar textos das células
                cell_text = []
                for i in range(len(nomes)):
                    row_text = [nomes[i]]
                    row_text.extend([" " for _ in dados_obrig[i]])
                    row_text.append(perc_obrig[i])
                    row_text.append("")
                    row_text.extend([" " for _ in dados_opc[i]])
                    row_text.append(perc_opc[i])
                    cell_text.append(row_text)

                # Criar tabela
                table = ax.table(
                    cellText=cell_text,
                    cellColours=cell_colors,
                    colLabels=headers,
                    loc="center",
                    cellLoc="center",
                    colWidths=col_widths,
                )

                # Configurar aparência da tabela
                table.auto_set_font_size(False)
                table.set_fontsize(12)  # Aumentado o tamanho base da fonte

                # Ajustar cores e estilos das células
                for pos, cell in table._cells.items():
                    if pos[0] == 0:  # Cabeçalhos
                        if pos[1] == 0:  # Cabeçalho "Casa de Oração"
                            cell.set_text_props(
                                color="black",
                                weight="bold",
                                size=15,  # Aumentado ainda mais
                            )
                        else:  # Outros cabeçalhos
                            cell.set_text_props(
                                color="black",
                                weight="bold",
                                rotation=90,
                                size=14,  # Aumentado ainda mais
                            )
                            if pos[1] > 0:
                                cell.set_height(
                                    0.3
                                )  # Aumentado para acomodar fonte maior
                        cell.set_facecolor("white")
                    else:
                        is_perc_col = pos[1] in [
                            len(caracteristicas_obrigatorias) + 1,
                            n_cols - 1,
                        ]
                        is_space_col = pos[1] == len(caracteristicas_obrigatorias) + 2

                        if is_space_col:
                            cell.set_facecolor("white")
                        elif pos[1] == 0:  # Nome da casa
                            cell.set_text_props(
                                color="black",
                                weight="bold",
                                size=14,  # Aumentado ainda mais
                            )
                            cell.set_facecolor("white")
                        elif is_perc_col:  # Coluna de percentual
                            cell.set_text_props(
                                color="black",
                                weight="bold",  # Adicionado negrito
                                size=13,  # Aumentado ainda mais
                            )
                            cell.set_facecolor("white")
                        else:
                            cell.set_text_props(
                                color="black",
                                weight="bold",  # Adicionado negrito
                                size=12,  # Aumentado ainda mais
                            )

                        # Ajustar altura das linhas para acomodar fonte maior
                        cell.set_height(0.06)  # Aumentado para acomodar fonte maior

                    cell.set_edgecolor("black")  # Mudando a cor da borda para preto
                    cell.set_linewidth(0.5)  # Definindo a espessura da linha

                return table

            # Criar as duas tabelas com índices das casas
            indices_primeira_metade = list(range(metade))
            indices_segunda_metade = list(range(metade, len(casas)))

            table1 = criar_tabela(
                ax1,
                nomes_casas_1,
                dados_obrigatorios_1,
                dados_opcionais_1,
                percentuais_obrigatorios_1,
                percentuais_opcionais_1,
                indices_primeira_metade,
            )

            if len(nomes_casas_2) > 0:  # Só criar segunda tabela se houver dados
                table2 = criar_tabela(
                    ax2,
                    nomes_casas_2,
                    dados_obrigatorios_2,
                    dados_opcionais_2,
                    percentuais_obrigatorios_2,
                    percentuais_opcionais_2,
                    indices_segunda_metade,
                )
            else:
                ax2.axis("off")

            # Ajustar layout
            ax1.axis("off")
            ax2.axis("off")
            plt.subplots_adjust(
                left=0.02,
                right=0.98,
                top=0.95,
                bottom=0.05,
                wspace=0.2,  # Reduzir espaço entre as tabelas
            )

            # Salvar tabela
            root = tk.Tk()
            root.withdraw()  # Esconder a janela principal
            file_path = filedialog.asksaveasfilename(
                parent=root,
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("PDF files", "*.pdf"),
                ],
                title="Salvar tabela como",
                initialfile="tabela_gestao_vista.png",
            )
            root.destroy()  # Destruir a janela após o diálogo

            if file_path:
                # Salvar a figura diretamente
                fig.savefig(
                    file_path,
                    facecolor="white",  # Fundo branco
                    bbox_inches="tight",
                    dpi=300,
                    format=file_path.split(".")[-1].lower(),
                )
                messagebox.showinfo("✅ Sucesso", "Tabela exportada com sucesso!")

        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao exportar tabela: {str(e)}")
        finally:
            # Limpar recursos do matplotlib
            plt.close("all")
