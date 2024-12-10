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

    icon = ImageOps.contain(icon, (33, 33))

    img.paste(icon, pos, mask=icon)

    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 30), (pos[0]+40, pos[1], 540, 33), vAllign=tbA.BOTTOM, fill=(0,0,0))


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
    iconeTam = 27
    espacoAposIcone = 8
    spacing = 0
    if(tipo == dNomesT.Orientador):
        texto = f'Orientador(a): {nome}'
        fonteTam = 33
        espacoAposIcone = 7
        spacing = -1
    elif (tipo == dNomesT.Coorientador):
            texto = f'Coorientador(a): {nome}'
            fonteTam = 25
            iconeTam = 25
    else:
        texto = nome
        fonteTam = 35
        fonte = 'JosefinSans/Bold.ttf'

    icon = ImageOps.contain(icon, (iconeTam, iconeTam))

    img.paste(icon, pos, mask=icon)
    font = getFont(fonte, fonteTam)
    # Limita o tamanho do texto removendo as penúltima palavra
    while(font.getlength(texto) > 680):
        texto = texto.split(' ')
        texto = ' '.join(texto[:-2] + [texto[-1]])
        
    textBox(texto, ImageDraw.Draw(img), getFont(fonte, fonteTam), (pos[0] + iconeTam+espacoAposIcone, pos[1], 680, iconeTam+20), spacing=spacing, vAllign=tbA.TOP, fill=(0,0,0))

    
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
    icon = ImageOps.contain(icon, (65, 65))

    img.paste(icon, pos, mask=icon)

    font = getFont('JosefinSans/Bold.ttf', 25)
    y = pos[1]-15

    
    textBox(info, ImageDraw.Draw(img), font, (pos[0] + 65, y, 650, 100), hAllign=tbA.LEFT, vAllign=tbA.CENTER, fill=(0,0,0), lineHeight=1.5)

    
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
    icon = ImageOps.contain(icon, (31, 41))

    img.paste(icon, pos, mask=icon)

    titulo = 'Presencial'
    if(info.startswith('http')):
        titulo = 'Online'
        info = re.sub(r'https?:\/\/', '', info)

    textBox(titulo, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 21), (pos[0] + 36, pos[1] + 3, 250, 23), fill=(0,0,0))
    #textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Regular.ttf', 17), (pos[0] + 34, pos[1] + 27, 250, 45), vAllign=tbA.TOP, fill=(0,0,0))
    ImageDraw.Draw(img).text((pos[0] + 36, pos[1] + 27), info, font=getFont('JosefinSans/Regular.ttf', 17), fill=(0,0,0))


def modeloTCCStories(data, semestre:str):
    if not hasattr(modeloTCCStories, 'counter'): # Inicializa o contador de imagens para salvar com um número sequencial
        modeloTCCStories.counter = 0 
    modeloTCCStories.counter += 1
    

    imagem =  Image.open("./assets/img/tcc/fundo-stories.png")
    d =  ImageDraw.Draw(imagem)
    curso = data[0]['Curso']

    # Escreve o curso e o semestre
    textBox(curso, d,  getFont('JosefinSans/Bold.ttf', 35), (78, 325, 1000, 50), fill=(255,0,0))
    textBox(semestre, d,  getFont('JosefinSans/Medium.ttf', 40), (517, 280, 1000, 50), spacing=-0.5, fill=(0,0,0))


    y_start = 441
    #x_start = 38
    for dados in data:
        # Nome do aluno
        dNomes(imagem, dados['Aluno'], (35, y_start))
        # Orientador
        dNomes(imagem, dados['Orientador'], (38, y_start+55), dNomesT.Orientador)
        
        # Coorientador
        #if dados['Coorientador'] != "":
        #    dNomes(imagem, dados['Coorientador'], (65, 440), dNomesT.Coorientador)

        dTitulo(imagem, dados['Titulo'], (32, y_start+122))

        # Data, hora e local
        dData(imagem, dados['Data'], (775, y_start + 49))
        dData(imagem, dados['Hora'].replace(':', 'h'),  (775, y_start + 89), True)
        dLocal(imagem, dados['Local'], ((776, y_start + 133)))

        # Linha vermelha
        d.rectangle((79, y_start + 238, 972, y_start + 241), fill=(255,0,0))

        y_start += 297
    
    imagem.save(f'./output/imagens/TCC_stories_{datetime.date.today()}_{modeloTCCStories.counter}.png')

