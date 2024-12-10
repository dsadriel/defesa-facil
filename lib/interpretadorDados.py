"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

from bs4 import BeautifulSoup
import re
from lib.encurtador_tinyURL import encurtarURLDefesa

def intepretarDados(tipo:str, origem:str, conteudo:str):
    if(tipo == 'pos'):
        if(origem == 'html'):
            return None
        elif(origem == 'email'):
            return emailPos(conteudo)
        else:
            return None
    
    elif(tipo == 'tcc'):
        if(origem == 'html'):
            return htmlTCC(conteudo)
        elif(origem == 'email'):
            return emailTCC(conteudo)
        else:
            return None
    else :
        return None
    

def htmlTCC(html_content):
    """
    Extrai informações de um conteúdo HTML e retorna uma lista de dicionários contendo os dados extraídos.

    Parâmetros:
    - html_content (str): O conteúdo HTML a ser analisado.

    Retorna:
    - linhas (list): Uma lista de dicionários contendo os dados extraídos do conteúdo HTML.

    Exemplo de uso:
    >>> html_content = "<html>...</html>"
    >>> dados = htmlTCC(html_content)
    >>> print(dados)
    [{'Curso': 'Engenharia de Software', 'Aluno': 'João Silva', 'Orientador': 'Maria Santos', ...}, ...]
    """
    soup = BeautifulSoup(html_content, 'lxml')
    linhas = []
    
    if(len(soup.find_all('tr')) <= 2):
            return []

    for rows in soup.find_all('tr'):

        cols = rows.find_all('td')
        if(len(cols) == 0):
            continue # pula o cabeçalho
        
        dados = {
            'Curso': cols[2].text,
            'Aluno': cols[3].text,
            'Orientador': cols[4].text,
            'Coorientador': cols[5].text,
            'Titulo': cols[6].text,
            'Banca': re.split(r' ?- ', cols[7].text.strip())[1:],
            'Data': re.search(r'\d{2}\/\d{2}\/\d{4}', cols[0].text)[0],
            'Hora': re.search(r'\d{2}:\d{2}', cols[0].text)[0]
        }

        if(cols[1].text.startswith('REMOTO:')):
            dados['Local'] = cols[1].find('a')['href']
            # Verifica se a URL já foi encurtada e encurta se necessário
            if(not dados['Local'].startswith('https://tinyurl.com')):
                dados['Local'] = encurtarURLDefesa(dados['Local'], dados['Aluno'])
        else:
            dados['Local'] = cols[1].text.split(':')[1]
        
        linhas.append(dados)
        
    return linhas

def emailTCC(fileName, curso):
    """
    Extrai informações de um arquivo de email contendo dados de TCCs.

    Args:
        fileName (str): O caminho do arquivo de email.
        curso (str): O nome do curso.

    Returns:
        list: Uma lista de dicionários contendo as informações extraídas dos TCCs.
            Cada dicionário contém as seguintes chaves:
                - 'Curso': O nome do curso.
                - 'Aluno': O nome do aluno.
                - 'Orientador': O nome do orientador.
                - 'Coorientador': O nome do coorientador.
                - 'Titulo': O título do trabalho.
                - 'Banca': Uma lista de membros da banca.
                - 'Data': A data da defesa.
                - 'Hora': A hora da defesa.
                - 'Local': O local da defesa.
    """
    # Regex para consulta no e-mail.
    
    r = r'\n{0,}\s{0,}Alun(o|a): +(?P<aluno>.+?)$\n{0,}\s{0,}Título( do Trabalho)?: +(?P<titulo>.+?)$\n{0,}\s{0,}Orientador(a?)(es)?: +(?P<orientador>.+?)$(\n{0,}\s{0,}Coorientador(a?)(es)?: +(?P<coorientador>.+?)$)?\n{0,}\s{0,}Banca: +(?P<banca>.+?)$\n{0,}\s{0,}Data: +(?P<data>.+?)$\n{0,}\s{0,}(Link|Sala): +(?P<local>.*?)$'
    lista = []
    with open(fileName, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.finditer(r, content, re.MULTILINE)

        for match in matches:
            m = match.groupdict()
            dados = {
                'Curso': curso,
                'Aluno': m['aluno'].title(),
                'Orientador': m['orientador'] if m['orientador'] else '',
                'Coorientador': m['coorientador'] if m['coorientador'] else '',
                'Titulo': m['titulo'].replace('_', ' '),
                'Banca': m['banca'].split(', '),
                'Data': m['data'].split(' ')[0],
                'Hora': m['data'].split(' ')[2].lower().replace('h', ':'),
                'Local': re.sub(r'\[\d+\]', '', m['local']).strip
            }

            if dados['Hora'].endswith(':'):
                dados['Hora'] += '00'

            lista.append(dados)

    return lista


def emailPos(content):
    """
    Extrai informações de um arquivo de email contendo dados de TCCs.

    Args:
        fileName (str): O caminho do arquivo de email.
        curso (str): O nome do curso.

    Returns:
        list: Uma lista de dicionários contendo as informações extraídas dos TCCs.
            Cada dicionário contém as seguintes chaves:
                - 'Curso': O nome do curso.
                - 'Aluno': O nome do aluno.
                - 'Orientador': O nome do orientador.
                - 'Coorientador': O nome do coorientador.
                - 'Titulo': O título do trabalho.
                - 'Banca': Uma lista de membros da banca.
                - 'Data': A data da defesa.
                - 'Hora': A hora da defesa.
                - 'Local': O local da defesa.
    """

    # Regex para extrair os dados
    regex = r'\n{0,}\s{0,}DEFESA DE +(?P<tipo_defesa>.+?)$(?:\n|.)+Alun(?:o\(a\)|o|a): (?P<aluno>.+?)$(?:\n|.)+?Orientador(?:\(a\)|a)?: (?P<orientador>.+?)$(?:(?:\n|.)+Coorientador(?:\(a\)|a)?: (?P<coorientador>.+?)$)?(?:\n|.)+Título: (?P<titulo>.+?)$(?:\n|.)+(?:Data: (?P<data>\d{2}\/\d{2}\/\d{4}))$(?:\n|.)+(?:Horário|Hora): (?P<horario>\d{1,2}(?:h|\:)\d{2}(min)?)(?:\n|.)+Local: (?P<local>.+?)$'

    m = re.search(regex, content, re.MULTILINE | re.IGNORECASE)
            
    if(not m):
        raise ValueError('Não foi possível encontrar os dados da defesa no email.')


    dados = {
        'Aluno': m['aluno'].title(),
        'Tipo': m['tipo_defesa'],
        'Orientador': m['orientador'] if m['orientador'] else '',
        'Coorientador': m['coorientador'] if m['coorientador'] else '',
        'Titulo': m['titulo'].replace('_', ' '),
        #'Banca': m['banca'].split(', '),
        'Data': m['data'],
        'Hora': m['horario'].lower().replace('h', ':'),
    }

    # FIX-ME não está funcionando corretamente para defesas hibrídas

    infoLocal = [
        re.search(r'Sala(?P<tipo_defesa>.+?)\s+Prédio (?P<predio>\d+(?:\.\d+)?)', m['local'], re.IGNORECASE),
        re.search(r'https?://\S+', m['local'])]
    infoLocal = [i[0] if i != None else '' for i in infoLocal] 
    
    
    #Se existir um link e não for um link do tinyurl, então encurta
    if(infoLocal[1]):
        if(not infoLocal[1].startswith('https://tinyurl.com')):
            # Remove o ponto final, se existir
            infoLocal[1] = infoLocal[1][:-1] if infoLocal[1].endswith('.') else infoLocal[1]

            # Encurta a URL
            infoLocal[1] = encurtarURLDefesa(infoLocal[1], dados['Aluno'])

    infoLocal = [i for i in infoLocal if i]
    
    dados['Local'] = '\n'.join(infoLocal)
    print(dados['Local'])

    if dados['Hora'].endswith(':'):
        dados['Hora'] += '00'

    return dados

