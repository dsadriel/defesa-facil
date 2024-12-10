"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

""" 
    Adapted from: https://gist.github.com/digitaltembo/eb7c8a7fdef987e6689ee8de050720c4
"""


from PIL import Image, ImageDraw, ImageFont
from enum import Enum
import json

class Alignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

def textBox(text, image_draw, font, box, spacing=0, hAllign = Alignment.LEFT, 
            vAllign = Alignment.TOP, lineHeight=1.3,
            showBorders=False, **kwargs):
    """
    Cria uma caixa de texto em uma imagem com as configurações especificadas.

    Parâmetros:
    - text: O texto a ser exibido na caixa.
    - image_draw: O objeto ImageDraw usado para desenhar na imagem.
    - font: A fonte a ser usada para o texto.
    - box: As coordenadas da caixa de texto no formato (x, y, largura, altura).
    - spacing: O espaçamento entre as palavras na mesma linha (padrão: 0).
    - hAllign: O alinhamento horizontal do texto (padrão: Alignment.LEFT).
    - vAllign: O alinhamento vertical do texto (padrão: Alignment.TOP).
    - lineHeight: A altura da linha em relação à altura da fonte (padrão: 1.3).
    - showBorders: Indica se as bordas da caixa devem ser exibidas (padrão: False).
    - **kwargs: Outros argumentos opcionais a serem passados para a função drawText.

    Retorna:
    - Uma tupla contendo as coordenadas da caixa de texto no formato (x, y, x + largura final, y + altura final).
    """

    x = box[0]
    y = box[1]
    width = box[2]
    height = box[3]
    
    if(showBorders):
        image_draw.rectangle((x, y, x + width, y + height), outline=(255,255,0))
    
    lines = text.split('\n')
    true_lines = []
    for line in lines:
        if font.getlength(line) + (len(line) * spacing) <= width:
            true_lines.append(line) 
        else:
            current_line = ''
            for word in line.split(' '):
                if font.getlength(current_line + word) <= width:
                    if(len(current_line) > 0):
                        current_line += ' '
                    current_line +=  word 
                else:
                    true_lines.append(current_line)
                    current_line = word 
            true_lines.append(current_line)
    
    x_offset = y_offset = 0
    lineheight = font.getmetrics()[0] * lineHeight # Give a margin of 0.2x the font height
    if vAllign == Alignment.CENTER:
        y = int(y + height / 2)
        y_offset = - (len(true_lines) * lineheight) / 2
    elif vAllign == Alignment.BOTTOM:
        y = int(y + height)
        y_offset = - (len(true_lines) * lineheight)
    
    for line in true_lines:
        linewidth = font.getlength(line)
        if hAllign == Alignment.CENTER:
            x_offset = (width - linewidth) / 2
        elif hAllign == Alignment.RIGHT:
            x_offset = width - linewidth
        
        drawText(image_draw, line, (int(x + x_offset), int(y + y_offset)), font, spacing, **kwargs)

        y_offset += lineheight
        if(y_offset > height):
            break
    
    return (x, y, x + x_offset, y + y_offset)

def drawText(ctx, text, pos, font, spacing, **kwargs):
    for char in text:
        ctx.text(pos, char, font=font, **kwargs)
        width = font.getlength(char) + spacing
        pos = (pos[0]+width, pos[1])

def getFont(name, fontSize=20):
    """
    Retorna uma fonte de texto com o nome e tamanho especificados.

    Parâmetros:
    name (str): O nome do arquivo de fonte.
    fontSize (int): O tamanho da fonte.

    Retorna:
    ImageFont: A fonte de texto carregada.

    Exemplo:
    >>> getFont("Arial.ttf", 12)
    <PIL.ImageFont.FreeTypeFont object at ...>
    """
    return ImageFont.truetype(f"./assets/fonts/{name}", fontSize)


def get_credentials(scope:str):
    """
    Retorna as credenciais de acesso ao TinyURL.

    Retorna:
    dict: Um dicionário contendo as credenciais de acesso ao TinyURL.
    """
    json_file = './credenciais.json'
    with open(json_file, 'r') as f:
        content = json.load(f)
    return content[scope]
    
    
    return