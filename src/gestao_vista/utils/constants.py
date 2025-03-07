"""Constantes utilizadas no sistema."""

DOCUMENTOS = {
    # Documentos de Propriedade
    "Escritura Definitiva - Compra e Venda/Permuta": "Escritura de Compra e Venda",
    "Escritura Pública - Inventário/Arrolamento": "Escritura de Inventário",
    "Escritura de Usucapião": "Escritura de Usucapião",
    "Sentença de Usucapião": "Sentença de Usucapião",
    "Formal de Partilha/Carta de Adjudicação": "Formal de Partilha",
    # Documentos de Construção/Funcionamento
    "Habite-se": "Habite-se",
    "Projeto Aprovado Pela Prefeitura": "Projeto Aprovado",
    "Alvará de Funcionamento": "Alvará de Funcionamento",
    "Averbação da Construção na Matricula": "Averbação de Construção",
    # Documentos de Segurança
    "AVCB - Auto de Vistoria do Corpo de Bombeiros": "Bombeiros",
    "CLCB - Certificado de Licença Corpo de Bombeiros": "Bombeiros",
    "SCPO - Sistema de Comunicação Prévia de Obras": "SCPO",
    # Instrumentos Particulares
    "Instrumento Particular - Cessão de Direitos de Compra e Venda": "Cessão de Direitos Particular",
    "Instrumento Particular - Cessão de Posse": "Cessão de Posse Particular",
    "Instrumento Particular - Cessão de Direitos Hereditários": "Cessão Hereditária Particular",
    "Instrumento Particular - Doação": "Doação Particular",
    "Instrumento Particular - Promessa de Compra e Venda": "Promessa de Compra Particular",
    # Instrumentos Públicos
    "Instrumento Público - Cessão de Direitos de Compra e Venda": "Cessão de Direitos Público",
    "Instrumento Público - Cessão de Direitos Hereditários": "Cessão Hereditária Público",
    "Instrumento Público - Cessão de Posse": "Cessão de Posse Público",
    "Instrumento Público - Doação": "Doação Público",
    "Instrumento Público - Promessa de Compra e Venda": "Promessa de Compra Público",
    # Outros Documentos
    "CNO – Cadastro Nacional de Obras": "CNO",
    "Licença de Ocupação": "Licença de Ocupação",
    "Regularização Fundiária": "REURB",
    "Contrato de Aluguel": "Contrato de Aluguel",
}

# Documentos obrigatórios para funcionamento
DOCUMENTOS_OBRIGATORIOS = [
    "Alvará de Funcionamento",
    "Bombeiros",
    "Projeto Aprovado",
    "Habite-se",
]


def _normalizar_texto(texto: str) -> str:
    """Normaliza o texto removendo espaços extras, acentos e convertendo para minúsculo."""
    import unicodedata

    # Remover acentos
    texto = (
        unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    )
    # Converter para minúsculo e remover espaços extras
    return texto.lower().strip()


def normalizar_nome_documento(nome: str) -> str:
    """Normaliza o nome do documento conforme o dicionário DOCUMENTOS."""
    # Criar um dicionário com chaves normalizadas
    docs_normalizados = {_normalizar_texto(k): v for k, v in DOCUMENTOS.items()}

    # Normalizar o nome de entrada
    nome_normalizado = _normalizar_texto(nome)

    # Procurar correspondência
    for key, value in docs_normalizados.items():
        if nome_normalizado in key or key in nome_normalizado:
            return value

    return nome


def is_documento_obrigatorio(nome: str) -> bool:
    """Verifica se um documento é obrigatório."""
    nome_normalizado = normalizar_nome_documento(nome)
    return nome_normalizado in DOCUMENTOS_OBRIGATORIOS
