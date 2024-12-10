"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
from lib.utils import getFont, textBox, Alignment as tbA
from enum import Enum
import re

class dNomesT(Enum):
    Orientador = 0
    Coorientador = 1
    Aluno = 2

def dData(img:Image, info, pos, hora=False):
    """
    Insere a data e hora em uma imagem.

    Parâmetros:
    - img: Imagem onde a data e hora serão inseridas.
    - info: Informação da data e hora a ser inserida.
    - pos: Posição onde a data e hora serão inseridas na imagem.
    - hora: Indica se a informação é referente à hora. O valor padrão é False.

    Retorna:
    Nenhum valor de retorno.
    """

    if(hora):
        icon = Image.open('./assets/img/relogio.png')
    else:
        icon = Image.open('./assets/img/calendario.png')

    icon = ImageOps.contain(icon, (28, 28))

    img.paste(icon, pos, mask=icon)

    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 25), (pos[0]+35, pos[1], 540, 33), vAllign=tbA.CENTER, fill=(0,0,0))


def dNomes(img:Image, nome, pos, tipo=dNomesT.Aluno):
    """
    Adiciona um nome à imagem.

    Args:
        img (Image): A imagem onde o nome será adicionado.
        nome (str): O nome a ser adicionado.
        pos (tuple): A posição onde o nome será colocado na imagem.
        tipo (dNomesT): O tipo de nome a ser adicionado. Padrão é dNomesT.Aluno.

    Returns:
        None
    """
    icon = Image.open('./assets/img/seta.png')

    fonte = 'JosefinSans/Regular.ttf'
    fonteTam = 0
    iconeTam = 23
    espacoAposIcone = 8
    spacing = 0
    if(tipo == dNomesT.Orientador):
        texto = f'Orientador(a): {nome}'
        fonteTam = 27
        iconeTam = 25
        espacoAposIcone = 6
        spacing = -1
    elif (tipo == dNomesT.Coorientador):
            texto = f'Coorientador(a): {nome}'
            fonteTam = 23
            iconeTam = 20
            espacoAposIcone = 10
    else:
        texto = nome
        fonteTam = 30
        fonte = 'JosefinSans/Bold.ttf'

    icon = ImageOps.contain(icon, (iconeTam, iconeTam))

    img.paste(icon, pos, mask=icon)
    font = getFont(fonte, fonteTam)
    # Limita o tamanho do texto removendo as penúltima palavra
    while(font.getlength(texto) > 590):
        texto = texto.split(' ')
        texto = ' '.join(texto[:-2] + [texto[-1]])

    textBox(texto, ImageDraw.Draw(img), font, (pos[0] + iconeTam+espacoAposIcone, pos[1], 590, iconeTam), spacing=spacing, vAllign=tbA.TOP, fill=(0,0,0))

    
def dTitulo(img:Image, info, pos):
    """
    Função responsável por adicionar o título em uma imagem.

    Parâmetros:
    - img: Imagem onde o título será adicionado.
    - info: Informação do título a ser adicionado.
    - pos: Posição onde o título será colocado na imagem.

    Retorno:
    Nenhum retorno.
    """

    icon = Image.open('./assets/img/caderno.png')
    icon = ImageOps.contain(icon, (58, 58))

    img.paste(icon, pos, mask=icon)

    font = getFont('JosefinSans/Bold.ttf', 25)

    textBox(info, ImageDraw.Draw(img), font, (pos[0] + 58, pos[1]-20, 550, 100), vAllign=tbA.CENTER, fill=(0,0,0))

    
def dLocal(img:Image, info, pos):
    """
    Função responsável por adicionar um ícone e informações sobre a localização em uma imagem.

    Parâmetros:
    - img (PIL.Image.Image): A imagem onde o ícone e as informações serão adicionados.
    - info (str): As informações sobre a localização.
    - pos (tuple): A posição onde o ícone será colocado na imagem.

    Retorno:
    A função não retorna nenhum valor.
    """
    
    icon = Image.open('./assets/img/local.png')
    icon = ImageOps.contain(icon, (26, 35))

    img.paste(icon, pos, mask=icon)

    titulo = 'Presencial'
    if(info.startswith('http')):
        titulo = 'Online'
        info = re.sub(r'https?:\/\/', '', info)

    textBox(titulo, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 17), (pos[0] + 30, pos[1], 250, 23), fill=(0,0,0))

    ImageDraw.Draw(img).text((pos[0] + 30, pos[1] + 20), info, font=getFont('JosefinSans/Regular.ttf', 17), fill=(0,0,0))

def modeloTCCFeed(data):
    if not hasattr(modeloTCCFeed, "counter"):
        modeloTCCFeed.counter = 0  # it doesn't exist yet, so initialize it
    modeloTCCFeed.counter += 1
    
    imagem =  Image.open("./assets/img/tcc/fundo-feed.png")
    d =  ImageDraw.Draw(imagem)

    y_start = 232
    #x_start = 38
    for dados in data:
        # Nome do aluno
        dNomes(imagem, dados['Aluno'], (70, y_start))
        # Orientador
        dNomes(imagem, dados['Orientador'], (70, y_start+47), dNomesT.Orientador)
    
        
        if dados['Coorientador'] != "":
            dNomes(imagem, dados['Coorientador'], (70, y_start+83), dNomesT.Coorientador)
            y_start += 35

        dTitulo(imagem, dados['Titulo'], (65, y_start+103))


        
        # Data, hora e local
        dData(imagem, dados['Data'], (701, y_start + 42))
        dData(imagem, dados['Hora'].replace(':', 'h'),  (701, y_start + 76), True)
        dLocal(imagem, dados['Local'], ((702, y_start + 115)))

        # Linha vermelha
        d.rectangle((107, y_start + 203, 870, y_start + 207), fill=(255,0,0))

        y_start += 255
    
    imagem.save(f'./output/imagens/TCC_feed_{datetime.date.today()}_{modeloTCCFeed.counter}.png')
