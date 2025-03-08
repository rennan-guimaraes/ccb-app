import json
from pathlib import Path
from typing import List, Optional
from ..models.observacao import Observacao


class ObservacaoService:
    def __init__(self):
        self.data_dir = Path("data")
        self.observacoes_file = self.data_dir / "observacoes.json"
        self._init_data_file()

    def _init_data_file(self):
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)

        if not self.observacoes_file.exists():
            self.observacoes_file.write_text("[]")

    def _load_observacoes(self) -> List[dict]:
        return json.loads(self.observacoes_file.read_text())

    def _save_observacoes(self, observacoes: List[dict]):
        self.observacoes_file.write_text(json.dumps(observacoes, indent=2))

    def criar_observacao(self, observacao: Observacao) -> Observacao:
        observacoes = self._load_observacoes()

        # Gerar ID único
        novo_id = str(len(observacoes) + 1)
        observacao.id = novo_id

        # Adicionar nova observação
        observacoes.append(observacao.to_dict())
        self._save_observacoes(observacoes)

        return observacao

    def listar_observacoes_por_casa(self, casa_oracao_id: str) -> List[Observacao]:
        observacoes = self._load_observacoes()
        return [
            Observacao.from_dict(obs)
            for obs in observacoes
            if obs["casa_oracao_id"] == casa_oracao_id
        ]

    def buscar_observacao(self, observacao_id: str) -> Optional[Observacao]:
        observacoes = self._load_observacoes()
        for obs in observacoes:
            if obs["id"] == observacao_id:
                return Observacao.from_dict(obs)
        return None

    def atualizar_observacao(self, observacao: Observacao) -> bool:
        """Atualiza uma observação existente"""
        observacoes = self._load_observacoes()

        for i, obs in enumerate(observacoes):
            if obs["id"] == observacao.id:
                observacoes[i] = observacao.to_dict()
                self._save_observacoes(observacoes)
                return True

        return False

    def excluir_observacao(self, observacao_id: str) -> bool:
        """Exclui uma observação"""
        observacoes = self._load_observacoes()
        observacoes = [obs for obs in observacoes if obs["id"] != observacao_id]
        self._save_observacoes(observacoes)
        return True
