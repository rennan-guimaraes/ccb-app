"""
Script para gerar ícones para a aplicação Gestão Vista.
Este script cria um ícone básico com as iniciais 'GV' em um fundo azul.

Requisitos:
- Pillow (PIL): pip install pillow

Uso:
python tools/generate_icon.py
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Adicionar o diretório raiz ao path para importar módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cores do design system
PRIMARY_COLOR = "#3B82F6"  # Azul
TEXT_COLOR = "#F8FAFC"  # Branco com tom azulado


def create_directory_if_not_exists(directory):
    """Cria um diretório se ele não existir."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Diretório criado: {directory}")


def generate_icon(size=256):
    """
    Gera um ícone quadrado com as iniciais 'GV' em um fundo azul.

    Args:
        size: Tamanho do ícone em pixels (quadrado)

    Returns:
        Imagem PIL do ícone
    """
    # Criar uma imagem quadrada com fundo azul
    image = Image.new("RGB", (size, size), PRIMARY_COLOR)
    draw = ImageDraw.Draw(image)

    # Tentar carregar uma fonte
    try:
        # Tentar fontes comuns que devem estar disponíveis na maioria dos sistemas
        font_options = [
            "Arial.ttf",
            "arial.ttf",
            "Verdana.ttf",
            "verdana.ttf",
            "Tahoma.ttf",
            "tahoma.ttf",
            "Segoe UI Bold.ttf",
            "segoeui.ttf",
            "DejaVuSans-Bold.ttf",
            "DejaVuSans.ttf",
        ]

        font = None
        for font_name in font_options:
            try:
                font = ImageFont.truetype(font_name, size=int(size * 0.5))
                break
            except IOError:
                continue

        # Se nenhuma fonte for encontrada, usar a fonte padrão
        if font is None:
            font = ImageFont.load_default()

    except Exception as e:
        print(f"Erro ao carregar fonte: {e}")
        font = ImageFont.load_default()

    # Texto a ser desenhado
    text = "GV"

    # Calcular a posição do texto para centralizá-lo
    text_width, text_height = (
        draw.textsize(text, font=font)
        if hasattr(draw, "textsize")
        else (size // 2, size // 2)
    )
    position = ((size - text_width) // 2, (size - text_height) // 2)

    # Desenhar o texto
    draw.text(position, text, fill=TEXT_COLOR, font=font)

    # Adicionar um círculo ao redor do texto
    padding = size * 0.1
    draw.ellipse(
        [(padding, padding), (size - padding, size - padding)],
        outline=TEXT_COLOR,
        width=int(size * 0.03),
    )

    return image


def save_icons():
    """Gera e salva os ícones em diferentes formatos e tamanhos."""
    # Criar diretório de assets se não existir
    assets_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets")
    )
    create_directory_if_not_exists(assets_dir)

    # Gerar ícone PNG para macOS
    icon_png = generate_icon(256)
    png_path = os.path.join(assets_dir, "icon.png")
    icon_png.save(png_path)
    print(f"Ícone PNG salvo em: {png_path}")

    # Gerar ícone ICO para Windows (múltiplos tamanhos)
    sizes = [16, 32, 48, 64, 128, 256]
    icons = [generate_icon(size) for size in sizes]
    ico_path = os.path.join(assets_dir, "icon.ico")

    # O primeiro ícone na lista será usado como base e os outros serão adicionados
    icons[0].save(
        ico_path,
        format="ICO",
        sizes=[(size, size) for size in sizes],
        append_images=icons[1:],
    )
    print(f"Ícone ICO salvo em: {ico_path}")


if __name__ == "__main__":
    try:
        save_icons()
        print("Ícones gerados com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar ícones: {e}")
