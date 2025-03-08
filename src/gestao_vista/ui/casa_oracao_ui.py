import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Tuple

from ..models.casa_oracao import CasaOracao
from ..services.casa_oracao_service import CasaOracaoService
from ..ui.components import create_dialog_window, create_button, create_form_field


class CasaOracaoUI:
    def __init__(self, casa_oracao_service: CasaOracaoService):
        self.casa_oracao_service = casa_oracao_service

    def view_casas(self, parent: tk.Tk):
        """Abre janela para visualizar e editar casas de oração"""
        dialog = create_dialog_window(parent, "Casas de Oração", width=1000, height=700)

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
        tree = self._create_treeview(table_frame)

        # Preencher dados
        self._populate_treeview(tree)

        # Adicionar menu de contexto
        self._setup_context_menu(tree, dialog)

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
            lambda: self._handle_save(dialog, entries, casa),
            "success",
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = create_button(button_frame, "❌ Cancelar", dialog.destroy, "error")
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _create_treeview(self, parent: ttk.Frame) -> ttk.Treeview:
        """Cria e configura o Treeview"""
        columns = [
            "codigo",
            "nome",
            "tipo_imovel",
            "endereco",
            "observacoes",
            "status",
        ]
        tree = ttk.Treeview(
            parent, columns=columns, show="headings", selectmode="browse"
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

        # Adicionar scrollbars
        y_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        x_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)

        return tree

    def _populate_treeview(self, tree: ttk.Treeview):
        """Preenche o Treeview com os dados das casas"""
        # Limpar dados existentes
        for item in tree.get_children():
            tree.delete(item)

        # Preencher dados
        for casa in self.casa_oracao_service.casas:
            values = []
            for col in tree["columns"]:
                value = getattr(casa, col, "")
                values.append(value if value is not None else "")
            tree.insert("", tk.END, values=values)

    def _setup_context_menu(self, tree: ttk.Treeview, dialog: tk.Toplevel):
        """Configura o menu de contexto do Treeview"""

        def show_context_menu(event):
            item = tree.selection()
            if item:
                menu = tk.Menu(dialog, tearoff=0)
                menu.add_command(
                    label="✏️ Editar",
                    command=lambda: self._handle_edit(dialog, tree, item[0]),
                )
                menu.add_command(
                    label="🗑️ Excluir",
                    command=lambda: self._handle_delete(tree, item[0]),
                )
                menu.post(event.x_root, event.y_root)

        tree.bind("<Button-3>", show_context_menu)
        tree.bind(
            "<Double-1>",
            lambda e: (
                self._handle_edit(dialog, tree, tree.selection()[0])
                if tree.selection()
                else None
            ),
        )

    def _handle_save(
        self,
        dialog: tk.Toplevel,
        entries: Dict[str, ttk.Entry],
        old_casa: Optional[CasaOracao] = None,
    ):
        """Manipula o salvamento de uma casa"""
        if self.casa_oracao_service.save_casa(dialog, entries, old_casa):
            # Atualizar a visualização
            self.view_casas(dialog.master)

    def _handle_edit(self, dialog: tk.Toplevel, tree: ttk.Treeview, item: str):
        """Manipula a edição de uma casa"""
        values = tree.item(item)["values"]
        casa = CasaOracao(**dict(zip(tree["columns"], values)))
        self.add_edit_casa(dialog, casa)

    def _handle_delete(self, tree: ttk.Treeview, item: str):
        """Manipula a exclusão de uma casa"""
        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir esta casa de oração?"
        ):
            values = tree.item(item)["values"]
            codigo = str(values[0])

            if self.casa_oracao_service.delete_casa(codigo):
                tree.delete(item)
