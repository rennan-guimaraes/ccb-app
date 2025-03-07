import os
import json
import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from ..models.casa_oracao import CasaOracao


class DataService:
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o serviço de dados.

        Args:
            data_dir: Diretório onde os dados serão armazenados
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.gestao_file = self.data_dir / "gestao.json"
        self.casas_file = self.data_dir / "casas.json"

        # Criar arquivos se não existirem
        if not self.gestao_file.exists():
            self.save_gestao(pd.DataFrame())
        if not self.casas_file.exists():
            self.save_casas([])

    def load_gestao(self) -> Optional[pd.DataFrame]:
        """Carrega os dados de gestão."""
        try:
            if self.gestao_file.exists():
                data = pd.read_json(self.gestao_file)
                if data.empty:
                    return pd.DataFrame(columns=["codigo"])
                return data
            return pd.DataFrame(columns=["codigo"])
        except Exception as e:
            print(f"Erro ao carregar dados de gestão: {e}")
            return pd.DataFrame(columns=["codigo"])

    def save_gestao(self, df: pd.DataFrame) -> bool:
        """
        Salva os dados de gestão.

        Args:
            df: DataFrame com os dados de gestão
        """
        try:
            # Garantir que temos pelo menos a coluna código
            if df.empty and "codigo" not in df.columns:
                df = pd.DataFrame(columns=["codigo"])
            df.to_json(self.gestao_file)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados de gestão: {e}")
            return False

    def load_casas(self) -> List[CasaOracao]:
        """Carrega as casas de oração."""
        try:
            if self.casas_file.exists():
                with open(self.casas_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [CasaOracao.from_dict(casa) for casa in data]
            return []
        except Exception as e:
            print(f"Erro ao carregar casas de oração: {e}")
            return []

    def save_casas(self, casas: List[CasaOracao]) -> bool:
        """
        Salva as casas de oração.

        Args:
            casas: Lista de casas de oração
        """
        try:
            data = [casa.to_dict() for casa in casas]
            with open(self.casas_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar casas de oração: {e}")
            return False

    def clear_gestao(self) -> bool:
        """Limpa os dados de gestão."""
        try:
            if self.gestao_file.exists():
                self.gestao_file.unlink()
            self.save_gestao(pd.DataFrame())
            return True
        except Exception as e:
            print(f"Erro ao limpar dados de gestão: {e}")
            return False

    def clear_casas(self) -> bool:
        """Limpa os dados das casas de oração."""
        try:
            if self.casas_file.exists():
                self.casas_file.unlink()
            self.save_casas([])
            return True
        except Exception as e:
            print(f"Erro ao limpar casas de oração: {e}")
            return False

    def import_gestao_from_excel(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Importa dados de gestão de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel
        """
        try:
            # Tentar ler o arquivo com openpyxl primeiro (formato mais novo)
            try:
                df = pd.read_excel(file_path, header=14, engine="openpyxl")
            except Exception as e:
                print(f"Tentando formato antigo de Excel: {e}")
                # Se falhar, tentar com xlrd para arquivos antigos
                df = pd.read_excel(
                    file_path,
                    header=14,
                    engine="xlrd",
                    on_demand=True,  # Reduz uso de memória
                )

            # Validar se o DataFrame foi carregado corretamente
            if df is None or df.empty:
                raise ValueError("Arquivo Excel está vazio ou com formato inválido")

            # Limpar e preparar o DataFrame
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            df = df.dropna(axis=1, how="all")

            # Validar se temos pelo menos uma coluna
            if df.empty or len(df.columns) == 0:
                raise ValueError("Nenhuma coluna válida encontrada no arquivo")

            # Garantir que a primeira coluna seja o código
            if "codigo" not in df.columns[0].lower():
                df = df.rename(columns={df.columns[0]: "codigo"})

            self.save_gestao(df)
            return df
        except Exception as e:
            print(f"Erro ao importar arquivo de gestão: {e}")
            messagebox.showerror(
                "❌ Erro",
                f"Erro ao importar arquivo de gestão:\n{str(e)}\n\n"
                "Certifique-se que o arquivo está no formato correto e tente novamente.",
            )
            return None

    def import_casas_from_excel(self, file_path: str) -> List[CasaOracao]:
        """
        Importa casas de oração de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel
        """
        try:
            # Tentar ler o arquivo com openpyxl primeiro
            try:
                df = pd.read_excel(file_path, engine="openpyxl")
            except Exception as e:
                print(f"Tentando formato antigo de Excel: {e}")
                df = pd.read_excel(file_path, engine="xlrd", on_demand=True)

            # Validar DataFrame
            if df is None or df.empty:
                raise ValueError("Arquivo Excel está vazio ou com formato inválido")

            # Mapear colunas para o formato esperado
            column_mapping = {
                "Código": "codigo",
                "CÓDIGO": "codigo",
                "CODIGO": "codigo",
                "Nome": "nome",
                "NOME": "nome",
                "Endereço": "endereco",
                "ENDEREÇO": "endereco",
                "ENDERECO": "endereco",
                "Endereco": "endereco",
                "Bairro": "bairro",
                "BAIRRO": "bairro",
                "Cidade": "cidade",
                "CIDADE": "cidade",
                "Responsável": "responsavel",
                "RESPONSÁVEL": "responsavel",
                "Responsavel": "responsavel",
                "RESPONSAVEL": "responsavel",
                "Telefone": "telefone",
                "TELEFONE": "telefone",
            }

            # Renomear colunas se necessário
            df.columns = [column_mapping.get(col, col) for col in df.columns]

            # Validar colunas obrigatórias
            required_columns = ["codigo", "nome"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(
                    f"Colunas obrigatórias não encontradas: {', '.join(missing_columns)}"
                )

            casas = []
            for _, row in df.iterrows():
                try:
                    casa_dict = {
                        "codigo": str(row.get("codigo", "")),
                        "nome": str(row.get("nome", "")),
                        "endereco": str(row.get("endereco", "")),
                        "bairro": str(row.get("bairro", "")),
                        "cidade": str(row.get("cidade", "")),
                        "responsavel": str(row.get("responsavel", "")),
                        "telefone": str(row.get("telefone", "")),
                    }
                    casa = CasaOracao.from_dict(casa_dict)
                    casas.append(casa)
                except Exception as e:
                    print(f"Erro ao processar linha: {e}")
                    continue

            if not casas:
                raise ValueError("Nenhuma casa de oração válida encontrada no arquivo")

            self.save_casas(casas)
            return casas
        except Exception as e:
            print(f"Erro ao importar arquivo de casas: {e}")
            messagebox.showerror(
                "❌ Erro",
                f"Erro ao importar arquivo de casas:\n{str(e)}\n\n"
                "Certifique-se que o arquivo está no formato correto e tente novamente.",
            )
            return []
