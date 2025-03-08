from datetime import datetime


class Observacao:
    def __init__(self, casa_oracao_id: str, documento: str, comentario: str):
        self.id = None  # Será definido ao salvar no banco
        self.casa_oracao_id = casa_oracao_id
        self.documento = documento
        self.comentario = comentario
        self.data_criacao = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "casa_oracao_id": self.casa_oracao_id,
            "documento": self.documento,
            "comentario": self.comentario,
            "data_criacao": self.data_criacao.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict):
        observacao = Observacao(
            casa_oracao_id=data["casa_oracao_id"],
            documento=data["documento"],
            comentario=data["comentario"],
        )
        observacao.id = data.get("id")
        observacao.data_criacao = datetime.fromisoformat(data["data_criacao"])
        return observacao
