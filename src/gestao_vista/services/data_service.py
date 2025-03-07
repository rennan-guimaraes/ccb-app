import os
import json
import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path

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
                return data
            return None
        except Exception as e:
            print(f"Erro ao carregar dados de gestão: {e}")
            return None

    def save_gestao(self, df: pd.DataFrame) -> bool:
        """
        Salva os dados de gestão.

        Args:
            df: DataFrame com os dados de gestão
        """
        try:
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
            if file_path.endswith(".xls"):
                df = pd.read_excel(file_path, header=14, engine="xlrd")
            else:
                df = pd.read_excel(file_path, header=14, engine="openpyxl")

            # Limpar e preparar o DataFrame
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            df = df.dropna(axis=1, how="all")

            self.save_gestao(df)
            return df
        except Exception as e:
            print(f"Erro ao importar arquivo de gestão: {e}")
            return None

    def import_casas_from_excel(self, file_path: str) -> List[CasaOracao]:
        """
        Importa casas de oração de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel
        """
        try:
            if file_path.endswith(".xls"):
                df = pd.read_excel(file_path, engine="xlrd")
            else:
                df = pd.read_excel(file_path, engine="openpyxl")

            casas = []
            for _, row in df.iterrows():
                casa_dict = row.to_dict()
                casa = CasaOracao.from_dict(casa_dict)
                casas.append(casa)

            self.save_casas(casas)
            return casas
        except Exception as e:
            print(f"Erro ao importar arquivo de casas: {e}")
            return []
