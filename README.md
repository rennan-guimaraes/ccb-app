# Gestão à Vista - Casas de Oração

Aplicação desktop para gerenciamento e visualização de dados das Casas de Oração.

## Funcionalidades

- Importação de dados de Gestão à Vista (Excel)
- Importação de dados das Casas de Oração (Excel)
- Visualização gráfica das características
- Gerenciamento de Casas de Oração (CRUD)
- Exportação de relatórios de casas faltantes

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/church-app.git
cd church-app
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

Execute a aplicação com:

```bash
python -m src.gestao_vista
```

## Estrutura do Projeto

```
church-app/
├── data/                  # Diretório para armazenamento de dados
├── dist/                  # Diretório com executáveis gerados
├── src/                   # Código fonte
│   └── gestao_vista/     # Pacote principal
│       ├── core/         # Lógica principal da aplicação
│       ├── models/       # Modelos de dados
│       ├── services/     # Serviços e gerenciadores
│       ├── ui/           # Componentes da interface
│       └── utils/        # Utilitários e configurações
├── requirements.txt      # Dependências do projeto
└── README.md            # Documentação
```

## Gerando Executável

Para gerar um executável da aplicação, siga os passos:

1. Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

2. Execute o PyInstaller para gerar o executável:

```bash
# Para macOS
pyinstaller --name church-app --onefile --windowed src/gestao_vista/main.py

# Para Windows (execute em um ambiente Windows)
pyinstaller --name church-app --onefile --windowed src/gestao_vista/main.py
```

O executável será gerado na pasta `dist/` com o nome `church-app`.

**Observações:**

- O executável gerado é específico para a plataforma onde foi compilado
- Para gerar executáveis para diferentes sistemas operacionais, o comando deve ser executado no sistema operacional correspondente
- O executável inclui todas as dependências necessárias e não requer instalação do Python

## Desenvolvimento

O projeto segue as seguintes práticas:

- Código em Python com tipagem estática
- Arquitetura modular e orientada a objetos
- Interface gráfica com Tkinter
- Persistência de dados em JSON
- Design system consistente

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
