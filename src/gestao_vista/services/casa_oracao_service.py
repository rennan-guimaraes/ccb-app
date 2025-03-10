import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional

from gestao_vista.models.casa_oracao import CasaOracao
from gestao_vista.services.data_service import DataService
from gestao_vista.ui.components import create_button, create_form_field


class CasaOracaoService:
    def __init__(self, data_service: DataService):
        self.data_service = data_service
        self.casas: List[CasaOracao] = []

    def load_casas(self):
        """Carrega as casas de oração do arquivo"""
        self.casas = self.data_service.load_casas()
        return self.casas

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

            # Fechar janela
            dialog.destroy()

            messagebox.showinfo("✅ Sucesso", "Casa de oração salva com sucesso!")
            return True
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar casa de oração: {str(e)}")
            return False

    def delete_casa(self, codigo: str) -> bool:
        """
        Exclui uma casa de oração.

        Args:
            codigo: Código da casa a ser excluída

        Returns:
            bool: True se a exclusão foi bem sucedida, False caso contrário
        """
        try:
            # Remover do DataFrame
            self.casas = [casa for casa in self.casas if casa.codigo != codigo]

            # Salvar no arquivo
            self.data_service.save_casas(self.casas)

            messagebox.showinfo("✅ Sucesso", "Casa de oração excluída com sucesso!")
            return True
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao excluir casa de oração: {str(e)}")
            return False

    def clear_casas(self) -> bool:
        """
        Limpa todas as casas de oração.

        Returns:
            bool: True se a operação foi bem sucedida, False caso contrário
        """
        if not messagebox.askyesno(
            "Confirmar", "Deseja realmente limpar os dados das Casas de Oração?"
        ):
            return False

        try:
            if self.data_service.clear_casas():
                self.casas = []
                messagebox.showinfo(
                    "✅ Sucesso", "Dados das Casas de Oração limpos com sucesso!"
                )
                return True
            return False
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao limpar casas de oração: {str(e)}")
            return False

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
                return True
        return False

    def import_casas_from_excel(self, file_path: str) -> List[CasaOracao]:
        """
        Importa casas de oração de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel

        Returns:
            List[CasaOracao]: Lista de casas importadas

        Raises:
            ValueError: Se houver erro de validação
            Exception: Se houver erro inesperado
        """
        novas_casas = self.data_service.import_casas_from_excel(file_path)
        if novas_casas:
            self.casas = novas_casas
            return novas_casas
        return []
