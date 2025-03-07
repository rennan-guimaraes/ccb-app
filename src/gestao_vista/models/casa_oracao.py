from dataclasses import dataclass
from typing import Optional


@dataclass
class CasaOracao:
    codigo: str
    nome: str
    tipo_imovel: Optional[str] = None
    endereco: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

    @property
    def info_completa(self) -> str:
        """Retorna uma string formatada com todas as informações da casa."""
        return (
            f"Casa de Oração {self.codigo} - {self.nome}\n"
            f"Tipo: {self.tipo_imovel or 'Não informado'}\n"
            f"Endereço: {self.endereco or 'Não informado'}\n"
            f"Observações: {self.observacoes or 'Não informado'}\n"
            f"Status: {self.status or 'Não informado'}"
        )

    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário."""
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "tipo_imovel": self.tipo_imovel,
            "endereco": self.endereco,
            "observacoes": self.observacoes,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CasaOracao":
        """Cria uma instância a partir de um dicionário."""
        return cls(**data)
