import json
import os
import pandas as pd
from pathlib import Path


class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.gestao_file = self.data_dir / "gestao_vista.json"
        self.casas_file = self.data_dir / "casas_oracao.json"

        # Criar diretório de dados se não existir
        self.data_dir.mkdir(exist_ok=True)

    def save_gestao(self, df):
        """Salva os dados de Gestão à Vista"""
        if df is not None:
            data = df.to_json(orient="split")
            with open(self.gestao_file, "w", encoding="utf-8") as f:
                json.dump({"data": data}, f, ensure_ascii=False)

    def load_gestao(self):
        """Carrega os dados de Gestão à Vista"""
        if self.gestao_file.exists():
            with open(self.gestao_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return pd.read_json(data["data"], orient="split")
        return None

    def save_casas(self, df):
        """Salva os dados das Casas de Oração"""
        if df is not None:
            data = df.to_json(orient="split")
            with open(self.casas_file, "w", encoding="utf-8") as f:
                json.dump({"data": data}, f, ensure_ascii=False)

    def load_casas(self):
        """Carrega os dados das Casas de Oração"""
        if self.casas_file.exists():
            with open(self.casas_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return pd.read_json(data["data"], orient="split")
        return None

    def clear_gestao(self):
        """Limpa os dados de Gestão à Vista"""
        if self.gestao_file.exists():
            os.remove(self.gestao_file)

    def clear_casas(self):
        """Limpa os dados das Casas de Oração"""
        if self.casas_file.exists():
            os.remove(self.casas_file)
