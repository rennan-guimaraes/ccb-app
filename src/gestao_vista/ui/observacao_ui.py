import tkinter as tk
from tkinter import ttk, messagebox
from ..services.observacao_service import ObservacaoService
from ..services.casa_oracao_service import CasaOracaoService
from ..models.observacao import Observacao
from .styles import *
from ..services.data_service import DataService
from .components import create_label, create_button, create_combobox


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
        if self.window is not None:
            self.window.lift()
            return

        # Resetar as variáveis
        self.casa_var.set("")
        self.documento_var.set("")

        self.window = tk.Toplevel(self.root)
        self.window.title("Adicionar Observação")
        self.window.geometry("800x600")  # Reduzindo o tamanho
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
        title_label = create_label(content_frame, "Adicionar Observação", "h1")
        title_label.pack(pady=(0, 20))

        # Seleção da Casa de Oração
        casa_label = create_label(content_frame, "Casa de Oração:", "h3")
        casa_label.pack(anchor=tk.W, pady=(0, 5))

        self.casa_combo = create_combobox(content_frame, self.casa_var)
        self.casa_combo.pack(fill=tk.X, pady=(0, 15))
        self.casa_combo.bind("<<ComboboxSelected>>", self._on_casa_selected)

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

        self.comentario_text = tk.Text(
            text_frame,
            height=10,  # Reduzindo a altura
            font=DESIGN_SYSTEM["typography"]["body1"],
            fg=DESIGN_SYSTEM["colors"]["text"]["primary"],
            bg=DESIGN_SYSTEM["colors"]["background"]["paper"],
            insertbackground=DESIGN_SYSTEM["colors"]["text"]["primary"],
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

        # Resetar os valores dos comboboxes
        self.doc_combo["values"] = []
        self.comentario_text.delete("1.0", tk.END)

        self._carregar_casas_oracao()

    def _on_close(self):
        self.window.destroy()
        self.window = None

    def _carregar_casas_oracao(self):
        casas = self.casa_oracao_service.load_casas()
        self.casas_dict = {f"{casa.nome} (Cód: {casa.codigo})": casa for casa in casas}
        self.casa_combo["values"] = list(self.casas_dict.keys())

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
