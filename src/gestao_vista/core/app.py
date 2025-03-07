import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Optional, List, Dict, Any, Callable

from ..models.casa_oracao import CasaOracao
from ..services.data_service import DataService
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
        self.casas = self.data_service.load_casas()

        if self.df_gestao is not None and not self.df_gestao.empty:
            self.caracteristicas = self.df_gestao.columns[1:].tolist()
            self.coluna_codigo = self.df_gestao.columns[0]
        else:
            self.caracteristicas = []
            self.coluna_codigo = None
            # Criar DataFrame vazio com estrutura básica
            self.df_gestao = pd.DataFrame(columns=["codigo"])

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
            self.load_casas_file,
            self.export_faltantes,
            self.clear_gestao,
            self.clear_casas,
            self.view_casas,
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

    def plot_graph(self):
        """Plota o gráfico com os dados atuais"""
        if self.df_gestao is None or self.df_gestao.empty or not self.caracteristicas:
            # Limpar frame do gráfico
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            # Mostrar mensagem quando não há dados
            ttk.Label(
                self.graph_frame,
                text="Nenhum dado disponível.\nImporte um arquivo de Gestão à Vista para visualizar o gráfico.",
                style="SubHeader.TLabel",
                justify=tk.CENTER,
            ).pack(expand=True)
            return

        # Limpar frame do gráfico
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Configurar gráfico
        fig, ax = plt.subplots(
            figsize=(12, 7), facecolor=DESIGN_SYSTEM["colors"]["background"]["default"]
        )
        ax.set_facecolor(DESIGN_SYSTEM["colors"]["background"]["paper"])

        # Calcular dados e definir cores
        contagens = []
        cores = []
        total_casas = len(self.df_gestao)

        for caracteristica in self.caracteristicas:
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            contagem = valores.str.upper().str.strip().eq("X").sum()
            contagens.append(contagem)

            # Definir cor baseada se é documento obrigatório
            if is_documento_obrigatorio(caracteristica):
                cores.append(
                    DESIGN_SYSTEM["colors"]["error"]
                )  # Vermelho para obrigatórios
            else:
                cores.append(
                    DESIGN_SYSTEM["colors"]["primary"]
                )  # Cor padrão para os demais

        # Criar gráfico
        bars = ax.bar(range(len(self.caracteristicas)), contagens, color=cores)

        # Adicionar linha de 100% para documentos obrigatórios
        ax.axhline(
            y=total_casas, color="red", linestyle="--", alpha=0.3, label="Meta (100%)"
        )

        # Configurar eixos e labels
        ax.set_xticks(range(len(self.caracteristicas)))
        ax.set_xticklabels(
            self.caracteristicas,
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
            "Características das Casas de Oração\n(Documentos obrigatórios em vermelho)",
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

        # Adicionar legenda
        ax.legend()

        # Ajustar layout e exibir
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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
                self.update_ui_with_data()
                messagebox.showinfo(
                    "✅ Sucesso", "Arquivo de Gestão à Vista carregado com sucesso!"
                )

    def load_casas_file(self):
        """Carrega arquivo de Casas de Oração"""
        file_path = tk.filedialog.askopenfilename(
            title="Selecione o arquivo de Casas de Oração",
            filetypes=[
                ("Arquivo Excel", "*.xlsx"),
                ("Arquivo Excel", "*.xls"),
                ("Todos os arquivos", "*.*"),
            ],
            initialdir=".",
        )

        if file_path:
            self.casas = self.data_service.import_casas_from_excel(file_path)
            if self.casas:
                messagebox.showinfo(
                    "✅ Sucesso", "Arquivo de Casas de Oração carregado com sucesso!"
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

                # Limpar gráfico
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()

                messagebox.showinfo(
                    "✅ Sucesso", "Dados de Gestão à Vista limpos com sucesso!"
                )

    def clear_casas(self):
        """Limpa os dados das Casas de Oração"""
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente limpar os dados das Casas de Oração?"
        ):
            if self.data_service.clear_casas():
                self.casas = []
                messagebox.showinfo(
                    "✅ Sucesso", "Dados das Casas de Oração limpos com sucesso!"
                )

    def view_casas(self):
        """Abre janela para visualizar e editar casas de oração"""
        dialog = create_dialog_window(
            self.root, "Casas de Oração", width=1000, height=700
        )

        # Frame principal
        main_frame = ttk.Frame(dialog, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para botões de ação
        action_frame = ttk.Frame(main_frame, style="Card.TFrame")
        action_frame.pack(fill=tk.X, padx=5, pady=(0, 10))

        # Botão Adicionar
        add_btn = create_button(
            action_frame,
            "➕ Adicionar Casa",
            lambda: self.add_edit_casa(dialog),
            "success",
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        # Frame para a tabela
        table_frame = ttk.Frame(main_frame, style="Card.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Criar Treeview
        columns = [
            "codigo",
            "nome",
            "tipo_imovel",
            "endereco",
            "observacoes",
            "status",
        ]
        tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        # Configurar colunas e cabeçalhos
        headers = {
            "codigo": "Código",
            "nome": "Nome",
            "tipo_imovel": "Tipo",
            "endereco": "Endereço",
            "observacoes": "Observações",
            "status": "Status",
        }

        # Configurar cada coluna individualmente
        column_widths = {
            "codigo": 100,
            "nome": 200,
            "tipo_imovel": 150,
            "endereco": 250,
            "observacoes": 200,
            "status": 100,
        }

        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=column_widths[col], stretch=True)

        # Limpar dados existentes
        for item in tree.get_children():
            tree.delete(item)

        # Adicionar scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        x_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=tree.xview
        )
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)

        # Preencher dados
        for casa in self.casas:
            values = []
            for col in columns:
                value = getattr(casa, col, "")
                values.append(value if value is not None else "")
            tree.insert("", tk.END, values=values)

        # Adicionar menu de contexto
        def show_context_menu(event):
            item = tree.selection()
            if item:
                menu = tk.Menu(dialog, tearoff=0)
                menu.add_command(
                    label="✏️ Editar",
                    command=lambda: self.add_edit_casa(
                        dialog,
                        CasaOracao(**dict(zip(columns, tree.item(item[0])["values"]))),
                    ),
                )
                menu.add_command(
                    label="🗑️ Excluir", command=lambda: self.delete_casa(tree, item[0])
                )
                menu.post(event.x_root, event.y_root)

        tree.bind("<Button-3>", show_context_menu)
        tree.bind(
            "<Double-1>",
            lambda e: self.add_edit_casa(
                dialog,
                (
                    CasaOracao(
                        **dict(zip(columns, tree.item(tree.selection()[0])["values"]))
                    )
                    if tree.selection()
                    else None
                ),
            ),
        )

    def add_edit_casa(self, parent: tk.Toplevel, casa: Optional[CasaOracao] = None):
        """
        Abre janela para adicionar ou editar casa de oração.

        Args:
            parent: Janela pai
            casa: Casa de oração a ser editada (None para adicionar nova)
        """
        dialog = create_dialog_window(
            parent, "Editar Casa" if casa else "Adicionar Casa", width=500, height=600
        )

        # Frame principal
        main_frame = ttk.Frame(dialog, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Campos do formulário
        fields = {
            "codigo": ("Código", True),
            "nome": ("Nome", True),
            "tipo_imovel": ("Tipo", False),
            "endereco": ("Endereço", False),
            "observacoes": ("Observações", False),
            "status": ("Status", False),
        }

        entries = {}
        for field, (label, required) in fields.items():
            _, entry = create_form_field(
                main_frame, label, getattr(casa, field, "") if casa else "", required
            )
            entries[field] = entry

        # Frame para botões
        button_frame = ttk.Frame(main_frame, style="Card.TFrame")
        button_frame.pack(fill=tk.X, padx=10, pady=20)

        # Botões
        save_btn = create_button(
            button_frame,
            "💾 Salvar",
            lambda: self.save_casa(dialog, entries, casa),
            "success",
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = create_button(button_frame, "❌ Cancelar", dialog.destroy, "error")
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def save_casa(
        self,
        dialog: tk.Toplevel,
        entries: Dict[str, ttk.Entry],
        old_casa: Optional[CasaOracao] = None,
    ):
        """
        Salva os dados da casa de oração.

        Args:
            dialog: Janela de diálogo
            entries: Dicionário com os campos do formulário
            old_casa: Casa de oração sendo editada (None para nova casa)
        """
        # Coletar dados dos campos
        data = {field: entry.get().strip() for field, entry in entries.items()}

        # Validar campos obrigatórios
        required_fields = ["codigo", "nome"]
        missing_fields = [field for field in required_fields if not data[field]]

        if missing_fields:
            messagebox.showwarning(
                "⚠️ Aviso",
                f"Os seguintes campos são obrigatórios:\n{', '.join(missing_fields)}",
            )
            return

        try:
            # Criar nova casa
            nova_casa = CasaOracao(**data)

            # Se estiver editando, remover a casa antiga
            if old_casa:
                self.casas = [
                    casa for casa in self.casas if casa.codigo != old_casa.codigo
                ]

            # Adicionar nova casa
            self.casas.append(nova_casa)

            # Salvar no arquivo
            self.data_service.save_casas(self.casas)

            # Fechar janela e atualizar visualização
            dialog.destroy()
            self.view_casas()

            messagebox.showinfo("✅ Sucesso", "Casa de oração salva com sucesso!")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar casa de oração: {str(e)}")

    def delete_casa(self, tree: ttk.Treeview, item: str):
        """
        Exclui uma casa de oração.

        Args:
            tree: Treeview com as casas
            item: Item selecionado na árvore
        """
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir esta casa de oração?"
        ):
            values = tree.item(item)["values"]
            codigo = str(values[0])

            try:
                # Remover do DataFrame
                self.casas = [casa for casa in self.casas if casa.codigo != codigo]

                # Salvar no arquivo
                self.data_service.save_casas(self.casas)

                # Remover da árvore
                tree.delete(item)

                messagebox.showinfo(
                    "✅ Sucesso", "Casa de oração excluída com sucesso!"
                )
            except Exception as e:
                messagebox.showerror(
                    "❌ Erro", f"Erro ao excluir casa de oração: {str(e)}"
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

        try:
            # Identificar casas faltantes
            valores = self.df_gestao[caracteristica].fillna("").astype(str)
            casas_faltantes = self.df_gestao[~valores.str.upper().str.strip().eq("X")][
                [self.coluna_codigo, caracteristica]
            ]
            casas_faltantes["Status"] = "Faltante"

            # Preparar dados para exportação
            dados_export = []
            for _, row in casas_faltantes.iterrows():
                codigo = str(row[self.coluna_codigo])
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
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao exportar relatório: {str(e)}")
