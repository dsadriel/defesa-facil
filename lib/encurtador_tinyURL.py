"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

import requests
import json
import colorama
from unidecode import unidecode 
from lib.utils import get_credentials
from termcolor import cprint
colorama.init()


tinyurl = get_credentials('TinyURL')

headers = {
        "Authorization": "Bearer " + tinyurl['token'], 
        "Content-Type": "application/json"
}


def update_aliases_cache(alias:str, url:str):
    """
    Atualiza o cache de aliases com um novo alias e sua URL correspondente.

    Args:
        alias (str): O alias da URL encurtada.
        url (str): A URL correspondente ao alias.

    Returns:
        None
    """
    with open('data/url-aliases-cache.json', 'r') as f:
        aliases = json.load(f)
        aliases[alias] = url
    with open('data/url-aliases-cache.json', 'w+') as f:
        json.dump(aliases, f, indent=4)

def get_alias_from_cache(alias:str):
    """
    Obtém a URL correspondente a um alias a partir do cache de aliases.
    
    Args:
        url (str): O URL referente ao alias. Se não existir, retorna None.

    Returns:
        str: A URL correspondente ao alias, se existir. Caso contrário, None.
    """
    with open('data/url-aliases-cache.json', 'r') as f:
        j = json.load(f)
        return j[alias] if alias in j else None
        

def unshorten_url(alias:str):
    """
    Desencurta uma URL usando um serviço de desencurtamento de URLs.

    Args:
        alias (str): O alias da URL encurtada.

    Returns:
        dict: Um dicionário com os dados da URL desencurtada.
    """
    
    # O endereço do serviço de desencurtamento de urls
    endpoint = "https://api.tinyurl.com/alias" + '/tinyurl.com/' + alias
    # As credenciais para acessar o serviço

   
    # Realizando a requisição
    response = requests.get(endpoint, headers=headers)
    #print(response.json())
    return response.json()['data']

def shorten_url(url:str, alias:str=None):
    """
    Encurta uma URL usando o serviço de encurtamento de URLs.

    Parâmetros:
        url (str): A URL que será encurtada.
        alias (str, opcional): Um alias personalizado para a URL encurtada.

    Retorna:
        str: A URL encurtada.

    Exemplo:
    >>> shorten_url("https://www.example.com")
    "https://tinyurl.com/abc123"
    """
    
    # O endereço do serviço de encurtamento de urls
    cachedURL = get_alias_from_cache(alias)
    if cachedURL == url: # A URL já está encurtada e corresponde ao link desejado
        return 'https://tinyurl.com/' + alias
    
    # O payload da requisição
    payload = {
        "url": url,
        "domain": "tinyurl.com",
        "alias": alias if alias else "",
    }

    # Realizando a requisição
    response = requests.post("https://api.tinyurl.com/create", headers=headers, json=payload)
    
    # Verificando se houve algum erro na requisição
    if response.status_code != 200:
        # Verificando se o alias já está em uso
        if  'Alias is not available.' in response.json()['errors']:
            # Se o alias já está em uso e este aponta para a url desejada, retorna o link
            urlData = unshorten_url(alias)
            if urlData['url'] == url and (urlData['user']['email'] == tinyurl['email']):
                return 'https://tinyurl.com/' + alias
            else:
                # Se o alias já está em uso e aponta para outra url, imprime um aviso e tenta encurtar a url novamente
                cprint(f'Alias {alias} já está em uso e aponta para {urlData["url"]}. ', 'yellow')

                contador = 0
                # Verifica se o alias já possui um número no final e incrementa o contador
                while(alias[-1].isdigit()):
                    contador = contador*10 + int(alias[-1])
                    alias = alias[:-1]
                return shorten_url(url, alias + str(contador + 1))
        else:
            # Se houve outro erro, imprime o erro e retorna None
            cprint(response.json(), 'red')
            raise Exception('Erro ao encurtar a URL')

    # Retornando a url encurtada
    update_aliases_cache(alias, response.json()['data']['tiny_url'])
    return response.json()['data']['tiny_url']


def update_url(url:str, alias:str):
    raise NotImplementedError('A conta do Comunica não possui permissão para atualizar URLs encurtadas.')
    """
    Atualiza uma URL destino com um alias personalizado.

    Args:
        url (str): A URL original que será atualizada.
        alias (str): O alias personalizado para a URL encurtada.

    Returns:
        str: A URL encurtada atualizada com o alias personalizado.
            Retorna None se a atualização falhar.
    """
    
    payload = {
        "alias": alias,
        "domain": "tinyurl.com",
        "url": url
    }
    if(alias == None or len(alias) == 0):
        return None

    # Realizando a requisição para atualizar a url
    response = requests.patch('https://api.tinyurl.com/change', headers=headers, json=payload)
    if(response.status_code != 200):
        cprint(response.json(), 'red')
        return None    
    
    update_aliases_cache(alias, url)
    return "https://tinyurl.com/" + alias


def encurtarURLDefesa(link:str, aluno:str=None):
    """
    Encurta a url de defesa de um aluno e retorna a url encurtada com um alias

    Args:
        link (str): A URL de defesa do aluno.
        aluno (str, optional): O nome do aluno. Se não for fornecido, um alias genérico será usado.

    Returns:
        str: A URL encurtada com um alias.
    """
    if(aluno == None):
        return shorten_url(link)
    
    aluno = unidecode(aluno)
    nomes = aluno.split(' ')
    for i in range(len(nomes)-1):
        nomes[i] = nomes[i][:2]

    # Cria um alias para a url no formato 'defesa-[iniciaisDoNome][sobrenomeDoAluno]'
    alias = 'defesa-' + aluno.split(' ')[0][:2] + aluno.split(' ')[-1][:15]
    return shorten_url(link, alias)
