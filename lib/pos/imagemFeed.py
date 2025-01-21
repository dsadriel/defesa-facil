"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
from lib.utils import textBox, Alignment as tbA
from enum import Enum
import re


class dNomesT(Enum):
    Orientador = 0
    Coorientador = 1
    Aluno = 2

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

    icon = ImageOps.contain(icon, (43, 43))

    img.paste(icon, pos, mask=icon)

    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 40), (pos[0] + 53, pos[1]+5, 350, 40), vAllign=tbA.TOP, fill=(0,0,0))


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
    iconeTam = 30
    if(tipo == dNomesT.Orientador):
        texto = f'Orientador(a): {nome}'
        fonteTam = 35
    else:
        if (tipo == dNomesT.Coorientador):
            texto = f'Coorientador(a): {nome}'
            fonteTam = 25
            iconeTam = 25
        else:
            texto = nome
            fonteTam = 40
            fonte = 'JosefinSans/Bold.ttf'

    icon = ImageOps.contain(icon, (iconeTam, iconeTam))
    img.paste(icon, pos, mask=icon)


    font = getFont(fonte, fonteTam)
    # Limita o tamanho do texto removendo palavras até que ele caiba na imagem
    while(font.getlength(texto) > 975):
        texto = texto.split(' ')
        texto = ' '.join(texto[:-2] + [texto[-1]])
    

    textBox(texto, ImageDraw.Draw(img), font, (pos[0] + 40, pos[1], 1000, iconeTam+20), vAllign=tbA.TOP, fill=(0,0,0))

    
def dTitulo(img:Image, info, pos, escala=1):
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

    img.paste(icon, [pos[0], pos[1]+25], mask=icon)

    font = getFont('JosefinSans/Bold.ttf', 40 * escala)
    y = pos[1] -15
    if(font.getlength(info)  <= 775):
        y = pos[1] + 15
    
    textBox(info, ImageDraw.Draw(img), font, (pos[0] + 65, y, 825, 150), hAllign=tbA.LEFT, vAllign=tbA.CENTER, fill=(0,0,0), showBorders=False)

    
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
    icon = ImageOps.contain(icon, (43, 125))

    img.paste(icon, pos, mask=icon)

    if(info.find('\n') != -1):
        titulo = 'Híbrida'
    elif(info.startswith('http')):
        titulo = 'Online'
    else:
        titulo = 'Presencial'
        
    # Remove o protocolo da URL
    info = re.sub(r'https?:\/\/', '', info)

    textBox(titulo, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 40), (pos[0] + 53, pos[1], 350, 40), vAllign=tbA.CENTER, fill=(0,0,0))
    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Regular.ttf', 25), (pos[0] + 53, pos[1] + 35, 350, 300), vAllign=tbA.TOP, fill=(0,0,0))



def modeloDefesaFeed(tituloCard, dados: dict, escalaTitulo=1): 
    """
    Gera uma imagem para a defesa de uma dissertação de mestrado.

    Parâmetros:
    - tituloCard (str): Título do card da defesa.
    - dados (dict): Dados da defesa, incluindo data, hora, local, aluno, orientador, coorientador e título.

    Retorno:
    Nenhum.

    Exemplo de uso:
    modeloDefesa("Defesa de Dissertação", {
        "Data": "2022-10-15",
        "Hora": "14:00",
        "Local": "Sala 101",
        "Aluno": "João Silva",
        "Orientador": "Maria Souza",
        "Coorientador": "Pedro Santos",
        "Titulo": "Análise de dados"
    })
    """


    imgFeed =  Image.open("./assets/img/pos/fundo-feed.png")
    # Gera imagem para o totem
    d =  ImageDraw.Draw(imgFeed)
    textBox(tituloCard.upper(), d,  getFont('MyriadPro/Regular.OTF', 50), (65, 205+120, 1000, 50), spacing=-1, fill=(0,0,0))
    # Data, hora e local    
    infStart = 820
    infoSpacing = 70
    dData(imgFeed, dados['Data'], (560, infStart))
    dData(imgFeed, dados['Hora'].replace(':', 'h'), (560, infStart + infoSpacing), True)
    dLocal(imgFeed, dados['Local'], (560, infStart + 2*infoSpacing))
    # Nome do aluno
    dNomes(imgFeed, dados['Aluno'], (65, 465))
    # Orientador
    dNomes(imgFeed, dados['Orientador'], (65, 520), dNomesT.Orientador)
    # Coorientador
    if dados['Coorientador'] != "":
        dNomes(imgFeed, dados['Coorientador'], (65, 575), dNomesT.Coorientador)
    
    dTitulo(imgFeed, dados['Titulo'], (67, 650), escalaTitulo)
    imgFeed.show()
    imgFeed.save(f'./output/imagens/defesa-{dados['Aluno'].replace(' ', '-')}(f).png')