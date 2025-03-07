from dataclasses import dataclass
from typing import Optional


@dataclass
class CasaOracao:
    codigo: str
    nome: str
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    responsavel: Optional[str] = None
    telefone: Optional[str] = None

    @property
    def info_completa(self) -> str:
        """Retorna uma string formatada com todas as informações da casa."""
        return (
            f"Casa de Oração {self.codigo} - {self.nome}\n"
            f"Endereço: {self.endereco or 'Não informado'}\n"
            f"Bairro: {self.bairro or 'Não informado'}\n"
            f"Cidade: {self.cidade or 'Não informado'}\n"
            f"Responsável: {self.responsavel or 'Não informado'}\n"
            f"Telefone: {self.telefone or 'Não informado'}"
        )

    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário."""
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "endereco": self.endereco,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "responsavel": self.responsavel,
            "telefone": self.telefone,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CasaOracao":
        """Cria uma instância a partir de um dicionário."""
        return cls(**data)
