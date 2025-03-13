import tkinter as tk
from tkinter import ttk, messagebox
from gestao_vista.services.observacao_service import ObservacaoService
from gestao_vista.services.casa_oracao_service import CasaOracaoService
from gestao_vista.models.observacao import Observacao
from gestao_vista.ui.styles import *
from gestao_vista.services.data_service import DataService
from gestao_vista.ui.components import (
    create_label,
    create_button,
    create_combobox,
    create_searchable_combobox,
)
import platform


class ObservacaoUI:
    def __init__(
        self, root, casa_oracao_service: CasaOracaoService, data_service: DataService
    ):
        self.root = root
        self.observacao_service = ObservacaoService()
        self.casa_oracao_service = casa_oracao_service
        self.data_service = data_service

        self.window = None
        self.casa_var = tk.StringVar()
        self.documento_var = tk.StringVar()

    def show(self):
        """Abre janela para visualizar observações existentes"""
        if self.window is not None:
            self.window.lift()
            return

        self.window = tk.Toplevel(self.root)
        self.window.title("Observações")
        self.window.geometry("800x600")
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

        # Container principal
        container = ttk.Frame(self.window, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para título e botão de adicionar
        header_frame = ttk.Frame(container, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Título
        title_label = create_label(header_frame, "Observações", "h1")
        title_label.pack(side=tk.LEFT)

        # Botão Adicionar
        add_btn = create_button(
            header_frame, "➕ Nova Observação", self._show_add_form, "success"
        )
        add_btn.pack(side=tk.RIGHT)

        # Seleção da Casa de Oração
        casa_label = create_label(container, "Casa de Oração:", "h3")
        casa_label.pack(anchor=tk.W, pady=(0, 5))

        self.casa_var = tk.StringVar()
        self.casa_var.trace("w", lambda *args: self._on_casa_selected_view(None))

        # Carregar casas que têm observações
        self._carregar_casas_com_observacoes()

        # Campo de busca de casas
        self.search_frame, _, _ = create_searchable_combobox(
            container,
            self.casa_var,
            self.casas_dict,
            "Digite o nome ou código da casa...",
        )
        self.search_frame.pack(fill=tk.X, pady=(0, 15))

        # Frame para conter o canvas e scrollbar
        scroll_container = ttk.Frame(container, style="Card.TFrame")
        scroll_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)

        # Criar canvas para scroll
        canvas = tk.Canvas(
            scroll_container,
            bg=DESIGN_SYSTEM["colors"]["background"]["paper"],
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            scroll_container, orient="vertical", command=canvas.yview
        )

        # Frame para lista de observações dentro do canvas
        self.observacoes_frame = ttk.Frame(canvas, style="Card.TFrame")
        self.observacoes_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Configurar canvas
        canvas.create_window(
            (0, 0),
            window=self.observacoes_frame,
            anchor="nw",
            width=canvas.winfo_reqwidth(),
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        # Posicionar elementos usando grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar scroll com mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Ajustar tamanho do canvas quando a janela for redimensionada
        def _on_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)

        canvas.bind("<Configure>", _on_configure)

    def _carregar_casas_com_observacoes(self):
        """Carrega apenas as casas que têm observações cadastradas"""
        casas = self.casa_oracao_service.load_casas()
        casas_com_observacoes = []

        for casa in casas:
            observacoes = self.observacao_service.listar_observacoes_por_casa(
                casa.codigo
            )
            if observacoes:
                casas_com_observacoes.append(casa)

        self.casas_dict = {
            f"{casa.nome} (Cód: {casa.codigo})": casa for casa in casas_com_observacoes
        }

        if not self.casas_dict:
            no_data_label = create_label(
                self.observacoes_frame,
                "Nenhuma casa possui observações cadastradas.",
                "body1",
            )
            no_data_label.pack(pady=20)

    def _show_add_form(self):
        """Abre o formulário para adicionar nova observação"""
        if self.window:
            self.window.destroy()
            self.window = None

        # Resetar as variáveis
        self.casa_var.set("")
        self.documento_var.set("")

        self.window = tk.Toplevel(self.root)
        self.window.title("Nova Observação")
        self.window.geometry("800x600")
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

        # Container principal
        container = ttk.Frame(self.window, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configurar o grid do container
        container.grid_rowconfigure(0, weight=1)  # Conteúdo expande
        container.grid_rowconfigure(1, weight=0)  # Botões não expandem
        container.grid_columnconfigure(0, weight=1)

        # Frame para o conteúdo
        content_frame = ttk.Frame(container, style="Card.TFrame", padding="20")
        content_frame.grid(row=0, column=0, sticky="nsew")

        # Título
        title_label = create_label(content_frame, "Nova Observação", "h1")
        title_label.pack(pady=(0, 20))

        # Seleção da Casa de Oração
        casa_label = create_label(content_frame, "Casa de Oração:", "h3")
        casa_label.pack(anchor=tk.W, pady=(0, 5))

        # Carregar todas as casas
        casas = self.casa_oracao_service.load_casas()
        self.casas_dict = {f"{casa.nome} (Cód: {casa.codigo})": casa for casa in casas}

        # Campo de busca de casas
        self.search_frame, _, _ = create_searchable_combobox(
            content_frame,
            self.casa_var,
            self.casas_dict,
            "Digite o nome ou código da casa...",
        )
        self.search_frame.pack(fill=tk.X, pady=(0, 15))

        # Bind para atualizar documentos quando uma casa for selecionada
        self.casa_var.trace("w", lambda *args: self._on_casa_selected(None))

        # Lista de Documentos Faltantes
        doc_label = create_label(content_frame, "Documento:", "h3")
        doc_label.pack(anchor=tk.W, pady=(0, 5))

        self.doc_combo = create_combobox(content_frame, self.documento_var)
        self.doc_combo.pack(fill=tk.X, pady=(0, 15))

        # Campo de Comentário
        comentario_label = create_label(content_frame, "Comentário:", "h3")
        comentario_label.pack(anchor=tk.W, pady=(0, 5))

        # Frame para o Text com fundo escuro
        text_frame = ttk.Frame(content_frame, style="Card.TFrame")
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Verificar se estamos no Windows
        is_windows = platform.system() == "Windows"

        # Configurar cores para o campo de texto
        if is_windows:
            text_fg = "#0F172A"  # Texto escuro para Windows
            text_bg = "#F8FAFC"  # Fundo branco para Windows
            insert_color = "#0F172A"  # Cursor escuro para Windows
        else:
            text_fg = DESIGN_SYSTEM["colors"]["text"]["primary"]
            text_bg = DESIGN_SYSTEM["colors"]["background"]["paper"]
            insert_color = DESIGN_SYSTEM["colors"]["text"]["primary"]

        self.comentario_text = tk.Text(
            text_frame,
            height=10,
            font=DESIGN_SYSTEM["typography"]["body1"],
            fg=text_fg,
            bg=text_bg,
            insertbackground=insert_color,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.comentario_text.pack(fill=tk.BOTH, expand=True)

        # Frame para os botões (usando grid para garantir posição)
        btn_frame = ttk.Frame(container, style="Card.TFrame", padding="10")
        btn_frame.grid(row=1, column=0, sticky="ew")

        # Botões alinhados à direita
        save_btn = create_button(
            btn_frame, "💾 Salvar", self._salvar_observacao, "primary"
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = create_button(
            btn_frame, "❌ Cancelar", self._on_close, "secondary"
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _on_close(self):
        self.window.destroy()
        self.window = None

    def _on_casa_selected(self, event):
        casa_key = self.casa_var.get()
        if not casa_key:
            return

        casa = self.casas_dict[casa_key]

        # Carregar dados do Gestão à Vista
        df_gestao = self.data_service.load_gestao()
        if df_gestao is None or df_gestao.empty:
            messagebox.showerror(
                "Erro", "Por favor, carregue primeiro o arquivo de Gestão à Vista!"
            )
            return

        # Encontrar a linha correspondente à casa selecionada
        casa_row = df_gestao[df_gestao["codigo"] == casa.codigo]
        if casa_row.empty:
            messagebox.showerror(
                "Erro",
                f"Casa de código {casa.codigo} não encontrada no arquivo de Gestão à Vista!",
            )
            return

        # Carregar observações existentes para esta casa
        observacoes_existentes = self.observacao_service.listar_observacoes_por_casa(
            casa.codigo
        )
        documentos_com_observacao = {obs.documento for obs in observacoes_existentes}

        # Identificar documentos faltantes (colunas onde não tem "X" e não tem observação)
        documentos_faltantes = []
        for coluna in df_gestao.columns[1:]:  # Ignorar a coluna 'codigo'
            valor = str(casa_row[coluna].iloc[0]).upper().strip()
            if valor != "X" and coluna not in documentos_com_observacao:
                documentos_faltantes.append(coluna)

        if not documentos_faltantes:
            messagebox.showinfo(
                "Info", "Esta casa não possui documentos faltantes sem observação!"
            )
            self.doc_combo["values"] = []
            self.documento_var.set("")
            return

        self.doc_combo["values"] = documentos_faltantes
        self.documento_var.set(documentos_faltantes[0])

    def _salvar_observacao(self):
        casa_key = self.casa_var.get()
        documento = self.documento_var.get()
        comentario = self.comentario_text.get("1.0", tk.END).strip()

        if not all([casa_key, documento, comentario]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        casa = self.casas_dict[casa_key]

        observacao = Observacao(
            casa_oracao_id=casa.codigo, documento=documento, comentario=comentario
        )

        self.observacao_service.criar_observacao(observacao)

        messagebox.showinfo("Sucesso", "Observação adicionada com sucesso!")

        self._on_close()

    def _on_casa_selected_view(self, event):
        """Manipula a seleção de casa no modo de visualização"""
        casa_key = self.casa_var.get()
        if not casa_key:
            return

        # Limpar frame de observações
        for widget in self.observacoes_frame.winfo_children():
            widget.destroy()

        casa = self.casas_dict[casa_key]
        observacoes = self.observacao_service.listar_observacoes_por_casa(casa.codigo)

        if not observacoes:
            no_data_label = create_label(
                self.observacoes_frame,
                "Nenhuma observação encontrada para esta casa.",
                "body1",
            )
            no_data_label.pack(pady=20)
            return

        # Container para os cards com padding
        cards_container = ttk.Frame(self.observacoes_frame, style="Card.TFrame")
        cards_container.pack(fill=tk.BOTH, expand=True, padx=5)

        # Criar cards para cada observação
        for obs in observacoes:
            card = ttk.Frame(cards_container, style="Card.TFrame", padding=10)
            card.pack(fill=tk.X, pady=5, padx=5)

            # Cabeçalho do card com documento e data
            header_frame = ttk.Frame(card, style="Card.TFrame")
            header_frame.pack(fill=tk.X)

            # Documento
            doc_label = create_label(header_frame, f"Documento: {obs.documento}", "h3")
            doc_label.pack(side=tk.LEFT)

            # Data
            data_label = create_label(
                header_frame,
                f"Data: {obs.data_criacao.strftime('%d/%m/%Y %H:%M')}",
                "body2",
            )
            data_label.pack(side=tk.RIGHT)

            # Linha separadora
            separator = ttk.Frame(card, height=1, style="Separator.TFrame")
            separator.pack(fill=tk.X, pady=5)

            # Comentário
            comentario_label = create_label(card, "Comentário:", "body1")
            comentario_label.pack(anchor=tk.W)

            comentario_text = tk.Text(
                card,
                height=3,
                font=DESIGN_SYSTEM["typography"]["body1"],
                fg=DESIGN_SYSTEM["colors"]["text"]["primary"],
                bg=DESIGN_SYSTEM["colors"]["background"]["paper"],
                relief="flat",
                wrap=tk.WORD,
            )
            comentario_text.insert("1.0", obs.comentario)
            comentario_text.configure(state="disabled")
            comentario_text.pack(fill=tk.X, pady=5)

            # Frame para botões
            btn_frame = ttk.Frame(card, style="Card.TFrame")
            btn_frame.pack(fill=tk.X)

            # Botão Editar
            edit_btn = create_button(
                btn_frame,
                "✏️ Editar",
                lambda o=obs: self._editar_observacao(o),
                "primary",
            )
            edit_btn.pack(side=tk.RIGHT, padx=5)

            # Botão Excluir
            delete_btn = create_button(
                btn_frame,
                "🗑️ Excluir",
                lambda o=obs: self._excluir_observacao(o),
                "error",
            )
            delete_btn.pack(side=tk.RIGHT, padx=5)

    def _editar_observacao(self, observacao):
        """Abre diálogo para editar uma observação"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Editar Observação")
        dialog.geometry("600x500")  # Aumentando ainda mais o tamanho do modal
        dialog.configure(bg=DESIGN_SYSTEM["colors"]["background"]["default"])

        # Container principal com grid para garantir posicionamento correto
        container = ttk.Frame(dialog, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configurar grid para garantir que os botões fiquem sempre visíveis
        container.grid_rowconfigure(0, weight=0)  # Título
        container.grid_rowconfigure(1, weight=0)  # Documento
        container.grid_rowconfigure(2, weight=0)  # Label comentário
        container.grid_rowconfigure(3, weight=1)  # Campo de texto (expansível)
        container.grid_rowconfigure(4, weight=0)  # Botões
        container.grid_columnconfigure(0, weight=1)

        # Título
        title_label = create_label(container, "Editar Observação", "h2")
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Documento (não editável)
        doc_label = create_label(container, f"Documento: {observacao.documento}", "h3")
        doc_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Campo de Comentário
        comentario_label = create_label(container, "Comentário:", "body1")
        comentario_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

        # Verificar se estamos no Windows
        is_windows = platform.system() == "Windows"

        # Configurar cores para o campo de texto
        if is_windows:
            text_fg = "#0F172A"  # Texto escuro para Windows
            text_bg = "#F8FAFC"  # Fundo branco para Windows
            insert_color = "#0F172A"  # Cursor escuro para Windows
        else:
            text_fg = DESIGN_SYSTEM["colors"]["text"]["primary"]
            text_bg = DESIGN_SYSTEM["colors"]["background"]["paper"]
            insert_color = DESIGN_SYSTEM["colors"]["text"]["primary"]

        comentario_text = tk.Text(
            container,
            height=10,
            font=DESIGN_SYSTEM["typography"]["body1"],
            fg=text_fg,
            bg=text_bg,
            insertbackground=insert_color,
            relief="flat",
            wrap=tk.WORD,
            padx=10,
            pady=10,
        )
        comentario_text.insert("1.0", observacao.comentario)
        comentario_text.grid(row=3, column=0, sticky="nsew", pady=5)

        # Frame para botões
        btn_frame = ttk.Frame(container, style="Card.TFrame")
        btn_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        # Botão Salvar
        save_btn = create_button(
            btn_frame,
            "💾 Salvar",
            lambda: self._salvar_edicao(
                observacao, comentario_text.get("1.0", tk.END).strip(), dialog
            ),
            "success",
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        # Botão Cancelar
        cancel_btn = create_button(
            btn_frame, "❌ Cancelar", dialog.destroy, "secondary"
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _salvar_edicao(self, observacao, novo_comentario, dialog):
        """Salva a edição de uma observação"""
        if not novo_comentario:
            messagebox.showerror("Erro", "O comentário não pode ficar vazio.")
            return

        observacao.comentario = novo_comentario
        self.observacao_service.atualizar_observacao(observacao)
        dialog.destroy()
        self._on_casa_selected_view(None)  # Atualizar a lista
        messagebox.showinfo("Sucesso", "Observação atualizada com sucesso!")

    def _excluir_observacao(self, observacao):
        """Exclui uma observação"""
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir esta observação?"
        ):
            self.observacao_service.excluir_observacao(observacao.id)
            self._on_casa_selected_view(None)  # Atualizar a lista
            messagebox.showinfo("Sucesso", "Observação excluída com sucesso!")
