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

    def _read_excel_safe(
        self, file_path: str, header_row: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Lê um arquivo Excel de forma segura, tentando diferentes métodos.

        Args:
            file_path: Caminho para o arquivo Excel
            header_row: Linha que contém os cabeçalhos (None para primeira linha)
        """
        try:
            # Primeiro, verificar se é um arquivo .xls (formato antigo)
            if file_path.lower().endswith(".xls"):
                # Para arquivos .xls, usar pandas com engine='xlrd'
                try:
                    return pd.read_excel(
                        file_path,
                        header=header_row,
                        engine="xlrd",
                        dtype=str,  # Ler tudo como string para evitar problemas de tipo
                    )
                except Exception as e:
                    print(f"Erro ao ler arquivo .xls com xlrd: {e}")
                    raise ValueError(
                        "Erro ao ler arquivo .xls. O arquivo pode estar corrompido."
                    )

            # Para outros formatos (.xlsx, etc), usar openpyxl
            return pd.read_excel(
                file_path,
                header=header_row,
                engine="openpyxl",
                dtype=str,  # Ler tudo como string para evitar problemas de tipo
            )
        except Exception as e:
            print(f"Erro ao ler arquivo Excel: {e}")
            raise ValueError(
                "Não foi possível ler o arquivo Excel. "
                "Certifique-se que o arquivo não está corrompido e está no formato correto (.xls ou .xlsx)"
            )

    def import_gestao_from_excel(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Importa dados de gestão de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel
        """
        try:
            # Ler o arquivo Excel
            df = self._read_excel_safe(file_path, header_row=14)

            # Validar se o DataFrame foi carregado corretamente
            if df is None or df.empty:
                raise ValueError("Arquivo Excel está vazio ou com formato inválido")

            # Limpar e preparar o DataFrame
            # Remover colunas vazias ou sem nome
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            df = df.dropna(axis=1, how="all")

            # Remover linhas completamente vazias
            df = df.dropna(how="all")

            # Validar se temos pelo menos uma coluna
            if df.empty or len(df.columns) == 0:
                raise ValueError("Nenhuma coluna válida encontrada no arquivo")

            # Garantir que a primeira coluna seja o código
            if "codigo" not in str(df.columns[0]).lower():
                df = df.rename(columns={df.columns[0]: "codigo"})

            # Converter todos os valores para string e limpar
            for col in df.columns:
                df[col] = df[col].astype(str).str.strip()

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
            # Ler o arquivo Excel, ignorando a primeira linha
            df = self._read_excel_safe(file_path)

            # Remover a primeira linha (cabeçalho)
            df = df.iloc[1:]

            # Validar DataFrame
            if df is None or df.empty:
                raise ValueError("Arquivo Excel está vazio ou com formato inválido")

            # Converter todas as colunas para string
            df.columns = df.columns.astype(str)

            # Se as colunas são números (0, 1, 2, etc), mapear para os nomes corretos
            if all(col.isdigit() for col in df.columns):
                # Mapear colunas numéricas para nomes
                numeric_mapping = {
                    "0": "codigo",
                    "1": "nome",
                    "2": "casa_oracao",  # Ignorar esta coluna
                    "3": "tipo_imovel",
                    "4": "endereco",
                    "5": "observacoes",
                    "6": "status",
                }
                df = df.rename(columns=numeric_mapping)
            else:
                # Mapear colunas para o formato esperado
                column_mapping = {
                    "Código": "codigo",
                    "CÓDIGO": "codigo",
                    "CODIGO": "codigo",
                    "codigo": "codigo",
                    "Nome": "nome",
                    "NOME": "nome",
                    "nome": "nome",
                    "Tipo Imóvel": "tipo_imovel",
                    "TIPO IMÓVEL": "tipo_imovel",
                    "tipo_imovel": "tipo_imovel",
                    "Endereço": "endereco",
                    "ENDEREÇO": "endereco",
                    "ENDERECO": "endereco",
                    "Endereco": "endereco",
                    "endereco": "endereco",
                    "Observações": "observacoes",
                    "OBSERVAÇÕES": "observacoes",
                    "observacoes": "observacoes",
                    "Status": "status",
                    "STATUS": "status",
                    "status": "status",
                }

                # Limpar nomes das colunas
                df.columns = [str(col).strip() for col in df.columns]

                # Tentar encontrar as colunas corretas mesmo com variações de nome
                for original_col in df.columns:
                    # Tentar encontrar o mapeamento ignorando acentos e maiúsculas/minúsculas
                    normalized_col = original_col.lower().strip()
                    for key in column_mapping:
                        if key.lower().strip() == normalized_col:
                            df = df.rename(columns={original_col: column_mapping[key]})
                            break

            # Validar colunas obrigatórias
            required_columns = ["codigo", "nome"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(
                    f"Colunas obrigatórias não encontradas: {', '.join(missing_columns)}\n"
                    f"Colunas encontradas: {', '.join(df.columns)}"
                )

            casas = []
            for idx, row in df.iterrows():
                try:
                    # Limpar e converter valores
                    casa_dict = {
                        "codigo": str(row.get("codigo", "")).strip(),
                        "nome": str(row.get("nome", "")).strip(),
                        "tipo_imovel": str(row.get("tipo_imovel", "")).strip(),
                        "endereco": str(row.get("endereco", "")).strip(),
                        "observacoes": str(row.get("observacoes", "")).strip(),
                        "status": str(row.get("status", "")).strip(),
                    }

                    # Validar dados obrigatórios
                    if not casa_dict["codigo"] or not casa_dict["nome"]:
                        print(f"Linha {idx + 2}: Código ou nome vazios")
                        continue

                    casa = CasaOracao.from_dict(casa_dict)
                    casas.append(casa)
                except Exception as e:
                    print(f"Erro ao processar linha {idx + 2}: {e}")
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
