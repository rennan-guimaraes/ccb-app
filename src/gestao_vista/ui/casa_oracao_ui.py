import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional, Tuple
import platform

from gestao_vista.models.casa_oracao import CasaOracao
from gestao_vista.services.data_service import DataService
from gestao_vista.utils.design_system import DESIGN_SYSTEM
from gestao_vista.ui.components import (
    create_dialog_window,
    create_button,
    create_form_field,
    create_label,
    create_searchable_combobox,
)
from gestao_vista.ui.windows_fixes import fix_treeview_header_for_windows


class CasaOracaoUI:
    def __init__(self, data_service: DataService):
        self.data_service = data_service
        self.window = None
        self.casas = []
        self.casa_var = tk.StringVar()
        self.casas_dict = {}
        self.edit_btn = None
        self.selected_casa = None

    def view_casas(self, parent: tk.Tk):
        """Abre janela para visualizar e editar casas de oração"""
        if self.window is not None:
            self.window.lift()
            return

        self.window = tk.Toplevel(parent)
        self.window.title("Casas de Oração")
        self.window.geometry("1000x700")
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Verificar se estamos no Windows
        is_windows = platform.system() == "Windows"

        # Configurar cores de fundo
        if is_windows:
            bg_color = "#F8FAFC"  # Fundo claro para Windows
            self.window.configure(bg=bg_color)
        else:
            bg_color = DESIGN_SYSTEM["colors"]["background"]["default"]
            self.window.configure(bg=bg_color)

        # Container principal
        container = ttk.Frame(self.window, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para título e botão de adicionar
        header_frame = ttk.Frame(container, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Título
        title_label = create_label(header_frame, "Casas de Oração", "h1")
        title_label.pack(side=tk.LEFT)

        # Botões de ação
        action_frame = ttk.Frame(header_frame, style="Card.TFrame")
        action_frame.pack(side=tk.RIGHT)

        # Botão Importar
        import_btn = create_button(
            action_frame, "📥 Importar", lambda: self._import_casas(), "primary"
        )
        import_btn.pack(side=tk.RIGHT, padx=5)

        # Botão Limpar
        clear_btn = create_button(
            action_frame, "🗑️ Limpar Todas", lambda: self._clear_casas(), "error"
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

        # Botão Editar (inicialmente oculto)
        self.edit_btn = create_button(
            action_frame, "✏️ Editar Casa", lambda: self._edit_selected_casa(), "primary"
        )
        # Não fazer pack do botão aqui, ele será mostrado apenas quando uma linha for selecionada

        # Botão Adicionar
        add_btn = create_button(
            action_frame, "➕ Nova Casa", lambda: self.add_edit_casa(), "success"
        )
        add_btn.pack(side=tk.RIGHT, padx=5)

        # Frame para pesquisa
        search_frame = ttk.Frame(container, style="Card.TFrame")
        search_frame.pack(fill=tk.X, pady=(0, 10))

        # Label de pesquisa
        search_label = create_label(search_frame, "Pesquisar casa:", "h3")
        search_label.pack(anchor=tk.W, pady=(0, 5))

        # Campo de pesquisa
        self.casa_var = tk.StringVar()
        self.casa_var.trace("w", lambda *args: self._on_casa_selected(None))

        # Carregar todas as casas
        self._carregar_casas()

        # Campo de busca de casas
        self.search_frame, _, _ = create_searchable_combobox(
            search_frame,
            self.casa_var,
            self.casas_dict,
            "Digite o nome ou código da casa...",
        )
        self.search_frame.pack(fill=tk.X, pady=(0, 15))

        # Frame para a tabela
        self.table_frame = ttk.Frame(container, style="Card.TFrame")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Criar tabela
        self._create_table()

    def _carregar_casas(self):
        """Carrega todas as casas"""
        self.casas = self.data_service.load_casas()
        self.casas_dict = {
            f"{casa.nome} (Cód: {casa.codigo})": casa for casa in self.casas
        }

    def _on_casa_selected(self, event):
        """Manipula a seleção de casa na pesquisa"""
        casa_key = self.casa_var.get()

        # Se não houver seleção, mostrar todas as casas
        if not casa_key:
            self._create_table(self.casas)
            return

        # Se uma casa específica foi selecionada
        if casa_key in self.casas_dict:
            casa_selecionada = self.casas_dict[casa_key]
            self._create_table([casa_selecionada])
        else:
            # Filtrar casas baseado no texto de pesquisa
            texto_pesquisa = casa_key.lower()
            casas_filtradas = [
                casa
                for casa in self.casas
                if texto_pesquisa in casa.nome.lower()
                or texto_pesquisa in casa.codigo.lower()
            ]
            self._create_table(casas_filtradas)

        # Esconder botão de edição quando pesquisar
        if self.edit_btn:
            self.edit_btn.pack_forget()
        self.selected_casa = None

    def _create_table(self, casas_para_exibir: Optional[List[CasaOracao]] = None):
        """Cria e configura a tabela de casas"""
        # Limpar frame da tabela
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Se não foi especificada uma lista de casas, usar todas
        if casas_para_exibir is None:
            casas_para_exibir = self.casas

        if not casas_para_exibir:
            no_data_label = create_label(
                self.table_frame, "Nenhuma casa de oração encontrada.", "body1"
            )
            no_data_label.pack(pady=20)
            # Esconder botão de edição
            if self.edit_btn:
                self.edit_btn.pack_forget()
            self.selected_casa = None
            return

        # Verificar se estamos no Windows
        is_windows = platform.system() == "Windows"

        # Criar Treeview
        columns = ["codigo", "nome", "tipo_imovel", "endereco", "status"]
        tree = ttk.Treeview(
            self.table_frame, columns=columns, show="headings", style="Treeview"
        )

        # Configurar colunas
        tree.heading("codigo", text="Código")
        tree.heading("nome", text="Nome")
        tree.heading("tipo_imovel", text="Tipo do Imóvel")
        tree.heading("endereco", text="Endereço")
        tree.heading("status", text="Status")

        tree.column("codigo", width=100, minwidth=80)
        tree.column("nome", width=200, minwidth=150)
        tree.column("tipo_imovel", width=150, minwidth=100)
        tree.column("endereco", width=300, minwidth=200)
        tree.column("status", width=100, minwidth=80)

        # Adicionar scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar elementos
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Configurar grid
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Esconder botão de edição ao recriar a tabela
        if self.edit_btn:
            self.edit_btn.pack_forget()
        self.selected_casa = None

        # Preencher dados
        for casa in casas_para_exibir:
            tree.insert(
                "",
                "end",
                values=(
                    casa.codigo,
                    casa.nome,
                    casa.tipo_imovel or "",
                    casa.endereco or "",
                    casa.status or "",
                ),
            )

        # Configurações específicas para Windows
        if is_windows:
            # Aplicar correções específicas para o cabeçalho da tabela no Windows
            fix_treeview_header_for_windows(tree)

        # Adicionar menu de contexto
        def show_context_menu(event):
            item = tree.selection()
            if item:
                menu = tk.Menu(self.window, tearoff=0)
                menu.add_command(
                    label="✏️ Editar", command=lambda: self._handle_edit(tree, item[0])
                )
                menu.add_command(
                    label="🗑️ Excluir",
                    command=lambda: self._handle_delete(tree, item[0]),
                )
                menu.post(event.x_root, event.y_root)

        # Configurar eventos
        tree.bind("<Button-3>", show_context_menu)  # Menu de contexto
        tree.bind("<Double-1>", lambda e: self._edit_selected_casa())  # Duplo clique
        tree.bind(
            "<<TreeviewSelect>>", lambda e: self._on_tree_select(e, tree)
        )  # Seleção

    def add_edit_casa(self, casa: Optional[CasaOracao] = None):
        """Abre janela para adicionar ou editar uma casa de oração"""
        # Verificar se estamos no Windows
        is_windows = platform.system() == "Windows"

        # Criar janela de diálogo
        dialog = create_dialog_window(
            self.window, "Adicionar Casa" if casa is None else "Editar Casa", 500, 600
        )

        # Configurar cores de fundo para Windows
        if is_windows:
            dialog.configure(bg="#F8FAFC")  # Fundo claro para Windows

        # Container principal
        container = ttk.Frame(dialog, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_text = (
            "Adicionar Nova Casa" if casa is None else f"Editar Casa: {casa.nome}"
        )
        title = create_label(container, title_text, "h2")
        title.pack(pady=(0, 20))

        # Frame para os campos
        fields_frame = ttk.Frame(container, style="Card.TFrame")
        fields_frame.pack(fill=tk.BOTH, expand=True)

        # Campos do formulário
        entries = {}

        # Definir cores para os campos de entrada
        entry_fg = (
            "#0F172A" if is_windows else DESIGN_SYSTEM["colors"]["text"]["primary"]
        )
        entry_bg = (
            "#F8FAFC" if is_windows else DESIGN_SYSTEM["colors"]["background"]["paper"]
        )

        # Código
        codigo_frame, codigo_entry = create_form_field(
            fields_frame, "Código", casa.codigo if casa else "", True
        )
        entries["codigo"] = codigo_entry
        if is_windows:
            codigo_entry.configure(fg=entry_fg, bg=entry_bg)

        # Nome
        nome_frame, nome_entry = create_form_field(
            fields_frame, "Nome", casa.nome if casa else "", True
        )
        entries["nome"] = nome_entry
        if is_windows:
            nome_entry.configure(fg=entry_fg, bg=entry_bg)

        # Tipo de Imóvel
        tipo_frame, tipo_entry = create_form_field(
            fields_frame, "Tipo de Imóvel", casa.tipo_imovel if casa else ""
        )
        entries["tipo_imovel"] = tipo_entry
        if is_windows:
            tipo_entry.configure(fg=entry_fg, bg=entry_bg)

        # Endereço
        endereco_frame, endereco_entry = create_form_field(
            fields_frame, "Endereço", casa.endereco if casa else ""
        )
        entries["endereco"] = endereco_entry
        if is_windows:
            endereco_entry.configure(fg=entry_fg, bg=entry_bg)

        # Status
        status_frame, status_entry = create_form_field(
            fields_frame, "Status", casa.status if casa else ""
        )
        entries["status"] = status_entry
        if is_windows:
            status_entry.configure(fg=entry_fg, bg=entry_bg)

        # Observações
        observacoes_frame, observacoes_entry = create_form_field(
            fields_frame, "Observações", casa.observacoes if casa else ""
        )
        entries["observacoes"] = observacoes_entry
        if is_windows:
            observacoes_entry.configure(fg=entry_fg, bg=entry_bg)

        # Frame para botões
        buttons_frame = ttk.Frame(container, style="Card.TFrame")
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        # Botão Cancelar
        cancel_btn = create_button(
            buttons_frame, "❌ Cancelar", lambda: dialog.destroy(), "error"
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Botão Salvar
        save_btn = create_button(
            buttons_frame,
            "💾 Salvar",
            lambda: self._handle_save(dialog, entries, casa),
            "success",
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

    def _handle_save(
        self,
        dialog: tk.Toplevel,
        entries: Dict[str, ttk.Entry],
        old_casa: Optional[CasaOracao] = None,
    ):
        """Manipula o salvamento de uma casa"""
        if self.data_service.save_casa(dialog, entries, old_casa):
            self._carregar_casas()
            self._create_table()

    def _handle_edit(self, tree: ttk.Treeview, item: str):
        """Manipula a edição de uma casa"""
        values = tree.item(item)["values"]
        casa = CasaOracao(
            codigo=values[0],
            nome=values[1],
            tipo_imovel=values[2],
            endereco=values[3],
            status=values[4],
        )
        self.add_edit_casa(casa)

    def _handle_delete(self, tree: ttk.Treeview, item: str):
        """Manipula a exclusão de uma casa"""
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir esta casa de oração?"
        ):
            values = tree.item(item)["values"]
            codigo = str(values[0])
            if self.data_service.delete_casa(codigo):
                self._carregar_casas()
                self._create_table()

    def _show_error_dialog(self, title: str, message: str, is_unexpected: bool = False):
        """Mostra um diálogo de erro padronizado"""
        dialog = create_dialog_window(
            self.window,
            "Erro Inesperado" if is_unexpected else "Erro",
            width=500,
            height=300,
        )

        container = ttk.Frame(dialog, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        error_title = create_label(
            container,
            "❌ " + title,
            "h2",
        )
        error_title.pack(pady=(0, 10))

        error_msg = create_label(
            container,
            message,
            "body1",
        )
        error_msg.pack(pady=(0, 20))

        ok_btn = create_button(container, "OK", dialog.destroy, "primary")
        ok_btn.pack()

    def _show_success_dialog(self, message: str):
        """Mostra um diálogo de sucesso padronizado"""
        dialog = create_dialog_window(self.window, "Sucesso", width=400, height=200)

        container = ttk.Frame(dialog, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        message_label = create_label(container, "✅ " + message, "body1")
        message_label.pack(pady=(0, 20))

        ok_btn = create_button(container, "OK", dialog.destroy, "primary")
        ok_btn.pack()

    def _import_casas(self):
        """Importa casas de oração de um arquivo Excel."""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo Excel",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("Excel files", ".xls"),
                ("All files", "*.*"),
            ],
            initialdir=".",
            defaultextension=".xlsx",
        )

        if not file_path:
            return

        try:
            # Importar casas
            novas_casas = self.data_service.import_casas_from_excel(file_path)

            if not novas_casas:
                self._show_error_dialog(
                    "Erro ao importar arquivo",
                    "Nenhuma casa de oração válida encontrada no arquivo.\n\nCertifique-se que o arquivo está no formato correto e tente novamente.",
                )
                return

            # Atualizar dados
            self._carregar_casas()
            self._create_table()

            # Mostrar mensagem de sucesso
            self._show_success_dialog(
                f"{len(novas_casas)} casas de oração importadas com sucesso!"
            )

        except ValueError as e:
            self._show_error_dialog(
                "Erro ao importar arquivo",
                f"{str(e)}\n\nCertifique-se que o arquivo está no formato correto e tente novamente.",
            )

        except Exception as e:
            self._show_error_dialog(
                "Erro Inesperado",
                f"{str(e)}\n\nPor favor, contate o suporte técnico.",
                is_unexpected=True,
            )

    def _clear_casas(self):
        """Limpa todas as casas de oração"""
        if self.data_service.clear_casas():
            self._carregar_casas()
            self._create_table()

    def _edit_selected_casa(self):
        """Abre o formulário de edição para a casa selecionada"""
        if self.selected_casa:
            self.add_edit_casa(self.selected_casa)

    def _on_tree_select(self, event, tree: ttk.Treeview):
        """Manipula a seleção de uma linha na tabela"""
        selected_items = tree.selection()
        if selected_items:
            # Obter dados da casa selecionada
            values = tree.item(selected_items[0])["values"]
            self.selected_casa = CasaOracao(
                codigo=values[0],
                nome=values[1],
                tipo_imovel=values[2],
                endereco=values[3],
                status=values[4],
            )
            # Mostrar botão de edição
            self.edit_btn.pack(side=tk.RIGHT, padx=5)
        else:
            # Esconder botão de edição
            self.edit_btn.pack_forget()
            self.selected_casa = None

    def _on_close(self):
        """Manipula o fechamento da janela"""
        self.window.destroy()
        self.window = None
        self.edit_btn = None
        self.selected_casa = None
