import os
import json
import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from gestao_vista.models.casa_oracao import CasaOracao
from gestao_vista.utils.constants import normalizar_nome_documento


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
                    if not isinstance(data, list):
                        print(
                            f"Erro: dados do arquivo não são uma lista, recebido {type(data)}"
                        )
                        return []
                    return [CasaOracao.from_dict(casa) for casa in data]
            return []
        except Exception as e:
            print(f"Erro ao carregar casas de oração: {str(e)}")
            return []

    def save_casas(self, casas: List[CasaOracao]) -> bool:
        """
        Salva as casas de oração.

        Args:
            casas: Lista de casas de oração
        """
        try:
            if not isinstance(casas, list):
                print(f"Erro: casas deve ser uma lista, recebido {type(casas)}")
                return False

            data = [casa.to_dict() for casa in casas]
            with open(self.casas_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar casas: {str(e)}")
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
            # Primeiro, tentar com openpyxl (para .xlsx)
            try:
                return pd.read_excel(
                    file_path,
                    header=header_row,
                    engine="openpyxl",
                    dtype=str,
                )
            except Exception as e:
                print(f"Erro ao tentar ler com openpyxl: {e}")
                pass

            # Se falhar, tentar com xlrd (para .xls)
            try:
                return pd.read_excel(
                    file_path,
                    header=header_row,
                    engine="xlrd",
                    dtype=str,
                )
            except Exception as e:
                print(f"Erro ao tentar ler com xlrd: {e}")
                pass

            # Se ainda falhar, tentar com odf (para .ods)
            try:
                return pd.read_excel(
                    file_path,
                    header=header_row,
                    engine="odf",
                    dtype=str,
                )
            except Exception as e:
                print(f"Erro ao tentar ler com odf: {e}")
                pass

            # Se todas as tentativas falharem, tentar uma última vez com o engine padrão
            return pd.read_excel(
                file_path,
                header=header_row,
                dtype=str,
            )

        except Exception as e:
            print(f"Erro ao ler arquivo Excel: {e}")
            raise ValueError(
                "Não foi possível ler o arquivo Excel. "
                "Certifique-se que o arquivo não está corrompido e está no formato correto (.xls ou .xlsx)"
            )

    def import_gestao_from_excel(
        self, file_path: str, should_save: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        Importa dados de gestão de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel
            should_save: Se True, salva os dados no arquivo gestao.json. Se False, apenas retorna o DataFrame.
        """
        try:
            df = self._import_gestao_from_excel_internal(file_path)

            if df is not None and should_save:
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

    def _import_gestao_from_excel_internal(
        self, file_path: str
    ) -> Optional[pd.DataFrame]:
        """
        Função interna para importar dados de gestão de um arquivo Excel.
        Esta função não salva os dados, apenas processa e retorna o DataFrame.

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

            # Normalizar nomes das colunas usando o dicionário DOCUMENTOS
            colunas_normalizadas = {}
            colunas_para_remover = []

            # Primeiro passo: normalizar todas as colunas
            for col in df.columns:
                if col.lower() != "codigo":  # Não normalizar a coluna código
                    try:
                        nome_normalizado = normalizar_nome_documento(col)

                        if nome_normalizado in colunas_normalizadas:
                            # Se já existe uma coluna com esse nome normalizado,
                            # combinar os valores (X em qualquer uma das colunas = X)
                            df[colunas_normalizadas[nome_normalizado]] = (
                                df[colunas_normalizadas[nome_normalizado]]
                                .fillna("")
                                .str.upper()
                                .str.strip()
                                .combine(
                                    df[col].fillna("").str.upper().str.strip(),
                                    lambda x, y: "X" if "X" in [x, y] else "",
                                )
                            )
                            colunas_para_remover.append(col)
                        else:
                            colunas_normalizadas[nome_normalizado] = nome_normalizado
                            if col != nome_normalizado:
                                df = df.rename(columns={col: nome_normalizado})
                    except Exception as e:
                        print(f"Erro ao normalizar coluna {col}: {e}")
                        continue

            # Remover colunas duplicadas
            if colunas_para_remover:
                df = df.drop(columns=colunas_para_remover)

            # Converter todos os valores para string e limpar
            for col in df.columns:
                df[col] = df[col].astype(str).str.strip()

            return df
        except Exception as e:
            print(f"Erro ao importar arquivo de gestão: {e}")
            raise

    def import_casas_from_excel(self, file_path: str) -> List[CasaOracao]:
        """
        Importa casas de oração de um arquivo Excel.

        Args:
            file_path: Caminho para o arquivo Excel

        Returns:
            List[CasaOracao]: Lista de casas importadas
        """
        try:
            # Verificar extensão do arquivo
            if not file_path.endswith((".xlsx", ".xls")):
                raise ValueError("Arquivo deve ser do tipo Excel (.xlsx ou .xls)")

            # Ler o arquivo Excel
            try:
                print(f"Tentando ler arquivo: {file_path}")
                df = pd.read_excel(file_path, dtype=str)
                print(
                    f"Arquivo lido com sucesso. Colunas encontradas: {df.columns.tolist()}"
                )
            except Exception as e:
                print(f"Erro detalhado ao ler Excel: {str(e)}")
                raise ValueError(f"Erro ao ler arquivo Excel: {str(e)}")

            if df.empty:
                raise ValueError("Arquivo Excel está vazio")

            # Validar colunas necessárias
            required_columns = ["codigo", "nome"]
            df.columns = (
                df.columns.str.lower().str.strip()
            )  # Converter e limpar nomes das colunas
            print(f"Colunas após normalização: {df.columns.tolist()}")

            # Verificar se as colunas obrigatórias existem
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(
                    f"Colunas obrigatórias não encontradas: {', '.join(missing_columns)}.\n"
                    f"Colunas disponíveis: {', '.join(df.columns)}"
                )

            # Processar cada linha
            casas = []
            for idx, row in df.iterrows():
                try:
                    # Limpar e validar dados
                    codigo = str(row.get("codigo", "")).strip()
                    nome = str(row.get("nome", "")).strip()

                    if not codigo or not nome:
                        print(f"Linha {idx + 1} ignorada: código ou nome vazios")
                        continue

                    print(f"Processando linha {idx + 1}: código={codigo}, nome={nome}")

                    # Criar objeto casa
                    casa = CasaOracao(
                        codigo=codigo,
                        nome=nome,
                        tipo_imovel=str(row.get("tipo_imovel", "")).strip() or None,
                        endereco=str(row.get("endereco", "")).strip() or None,
                        observacoes=str(row.get("observacoes", "")).strip() or None,
                        status=str(row.get("status", "")).strip() or None,
                    )
                    casas.append(casa)
                except Exception as e:
                    print(f"Erro ao processar linha {idx + 1}: {str(e)}")
                    continue

            if not casas:
                raise ValueError("Nenhuma casa de oração válida encontrada no arquivo")

            print(f"Total de casas importadas: {len(casas)}")

            # Salvar casas no arquivo
            if self.save_casas(casas):
                print("Casas salvas com sucesso no arquivo")
                return casas
            else:
                raise ValueError("Erro ao salvar casas no arquivo")

        except Exception as e:
            print(f"Erro ao importar arquivo de casas: {str(e)}")
            raise ValueError(f"Erro ao importar arquivo: {str(e)}")

    def save_casa(
        self,
        dialog: tk.Toplevel,
        entries: Dict[str, ttk.Entry],
        old_casa: Optional[CasaOracao] = None,
    ) -> bool:
        """
        Salva uma casa de oração.

        Args:
            dialog: Janela do formulário
            entries: Dicionário com os campos do formulário
            old_casa: Casa antiga (se for edição)
        """
        try:
            # Validar campos obrigatórios
            codigo = entries["codigo"].get().strip()
            nome = entries["nome"].get().strip()

            if not codigo or not nome:
                messagebox.showerror(
                    "❌ Erro", "Código e nome são campos obrigatórios!"
                )
                return False

            # Se for edição, verificar se o código mudou
            if old_casa and old_casa.codigo != codigo:
                # Verificar se novo código já existe
                casas = self.load_casas()
                if any(casa.codigo == codigo for casa in casas):
                    messagebox.showerror(
                        "❌ Erro", "Já existe uma casa com este código!"
                    )
                    return False

            # Criar objeto casa
            casa = CasaOracao(
                codigo=codigo,
                nome=nome,
                tipo_imovel=entries["tipo_imovel"].get().strip() or None,
                endereco=entries["endereco"].get().strip() or None,
                observacoes=entries["observacoes"].get().strip() or None,
                status=entries["status"].get().strip() or None,
            )

            # Carregar casas existentes
            casas = self.load_casas()

            if old_casa:
                # Atualizar casa existente
                casas = [casa if c.codigo == old_casa.codigo else c for c in casas]
            else:
                # Verificar se código já existe
                if any(c.codigo == casa.codigo for c in casas):
                    messagebox.showerror(
                        "❌ Erro", "Já existe uma casa com este código!"
                    )
                    return False
                # Adicionar nova casa
                casas.append(casa)

            # Salvar todas as casas
            if self.save_casas(casas):
                messagebox.showinfo("✅ Sucesso", "Casa de oração salva com sucesso!")
                dialog.destroy()
                return True
            return False

        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar casa de oração:\n{str(e)}")
            return False

    def delete_casa(self, codigo: str) -> bool:
        """
        Exclui uma casa de oração.

        Args:
            codigo: Código da casa a ser excluída
        """
        try:
            casas = self.load_casas()
            casas = [casa for casa in casas if casa.codigo != codigo]
            if self.save_casas(casas):
                messagebox.showinfo(
                    "✅ Sucesso", "Casa de oração excluída com sucesso!"
                )
                return True
            return False
        except Exception as e:
            messagebox.showerror(
                "❌ Erro", f"Erro ao excluir casa de oração:\n{str(e)}"
            )
            return False
