"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

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

    icon = ImageOps.contain(icon, (80, 80))

    img.paste(icon, pos, mask=icon)

    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 65), (pos[0] + 100, pos[1]+10, 540, 40), vAllign=tbA.TOP, fill=(0,0,0), spacing=-1)


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
    iconeTam = 55
    espaçamento = 68
    if(tipo == dNomesT.Orientador):
        texto = f'Orientador(a): {nome}'
        fonteTam = 54
        iconeTam = 45
        espaçamento = 55
    else:
        if (tipo == dNomesT.Coorientador):
            texto = f'Coorientador(a): {nome}'
            fonteTam = 50
            iconeTam = 40
            espaçamento = 55
        else:
            texto = nome
            fonteTam = 67
            fonte = 'JosefinSans/Bold.ttf'

    icon = ImageOps.contain(icon, (iconeTam, iconeTam))
    img.paste(icon, pos, mask=icon)

    font = getFont(fonte, fonteTam)
    # Limita o tamanho do texto removendo palavras até que ele caiba na imagem
    while(font.getlength(texto) > 1400):
        texto = texto.split(' ')
        texto = ' '.join(texto[:-2] + [texto[-1]])

    textBox(texto, ImageDraw.Draw(img), font, (pos[0] + espaçamento, pos[1], 1500, iconeTam+20), vAllign=tbA.TOP, fill=(0,0,0), spacing=-2)

    
def dTitulo(img:Image, info, pos, escala=1):
    """
    Função responsável por adicionar o título em uma imagem.

    Parâmetros:
    - img: Imagem onde o título será adicionado.
    - info: Informação do título a ser adic'ionado.
    - pos: Posição onde o título será colocado na imagem.

    Retorno:
    Nenhum retorno.
    """

    icon = Image.open('./assets/img/caderno.png')
    icon = ImageOps.contain(icon, (160, 160))

    img.paste(icon, pos, mask=icon)

    font = getFont('JosefinSans/Bold.ttf', 80 * escala)
    y = pos[1] - 20
    if(font.getlength(info)  <= 1500):
        y = pos[1] + 20
    
        
    textBox(info, ImageDraw.Draw(img), font, (pos[0] + 160, y, 1500, 300), vAllign=tbA.TOP, fill=(0,0,0), spacing=-1)

    
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
    icon = ImageOps.contain(icon, (75, 95))

    img.paste(icon, pos, mask=icon)

    if(info.find('\n') != -1):
        titulo = 'Híbrida'
    elif(info.startswith('http')):
        titulo = 'Online'
    else:
        titulo = 'Presencial'
        
    # Remove o protocolo da URL
    info = re.sub(r'https?:\/\/', '', info)

    textBox(titulo, ImageDraw.Draw(img), getFont('JosefinSans/Bold.ttf', 65), (pos[0] + 100, pos[1]+ 20, 540, 40), vAllign=tbA.TOP, fill=(0,0,0), spacing=-1)
    textBox(info, ImageDraw.Draw(img), getFont('JosefinSans/Regular.ttf', 43), (pos[0] + 102, pos[1] + 105, 700, 150), vAllign=tbA.TOP, fill=(0,0,0), spacing=-0.4)



def modeloDefesaTotem(tituloCard, dados: dict, escalaTitulo=1): 
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


    imgTotem = Image.open("./assets/img/pos/fundo-totem.png")
    
    # Gera imagem para o totem
    d =  ImageDraw.Draw(imgTotem)
    textBox(tituloCard.upper(), d,  getFont('MyriadPro/Regular.OTF', 123), (175, 468, 2000, 0), spacing=4, fill=(0,0,0))

    # Data, hora e local    
    infoPos = [1945, 685]
    infoSpacing = 125
    dData(imgTotem, dados['Data'], tuple(infoPos))
    infoPos[1] += infoSpacing
    dData(imgTotem, dados['Hora'].replace(':', 'h'), tuple(infoPos), True)


    infoPos[1] += infoSpacing
    dLocal(imgTotem, dados['Local'], tuple(infoPos))
    # Nome do aluno
    dNomes(imgTotem, dados['Aluno'], (175, 765))
    # Orientador
    dNomes(imgTotem, dados['Orientador'], (175, 890), dNomesT.Orientador)

    
    # Coorientador
    if dados['Coorientador'] != "":
        dNomes(imgTotem, dados['Coorientador'], (175, 965), dNomesT.Coorientador)
        dTitulo(imgTotem, dados['Titulo'], (175, 1090), escalaTitulo)
    else:
        dTitulo(imgTotem, dados['Titulo'], (175, 1060), escalaTitulo)

    
    
    imgTotem.save(f'./output/imagens/defesa-{dados['Aluno'].replace(' ', '-')}(t).png')
    ##imgTotem.show()
