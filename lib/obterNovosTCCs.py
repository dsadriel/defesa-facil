"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""


import json
import colorama
from termcolor import cprint
import requests

from lib.interpretadorDados import intepretarDados 
from lib.utils import get_credentials
colorama.init()


def obterNovosTCCs(echo = True, saveDiff = True):
    """
    Função que obtém os TCCs do portal de serviços do INF e verifica se há novos TCCs ou TCCs atualizados

    Args:
        echo (bool, optional): Se deve imprimir mensagens na tela. Defaults to True
    """
        
    portal = get_credentials('portalServicosINF')
    content = ''
    s = requests.Session()
    if(echo):
        print('Iniciando sessão no portal...')
    r = s.post('https://www.inf.ufrgs.br/portal/valida.php', data={'loginUsuario': portal['login'], 'senhaUsuario': portal['senha'], 'BtnLogin': '', 'redir': 'painel.php'})
    if(r.url == 'https://www.inf.ufrgs.br/portal/login.php?action=loginFailed'):
        if(echo):
            print('Login no portal falhou, por favor verifique as credenciais no arquivo credenciais.json')
        return {'error': 'Login no portal falhou, por favor verifique as credenciais no arquivo credenciais.json'}
    else:
        content = s.get('https://www.inf.ufrgs.br/portal/apps/TCC-Grad/comunica.php').text

    parsedTCC = intepretarDados('tcc', 'html', content)
    if(echo):
        print('TCCs obtidos com sucesso. \nIninicando interpretação dos dados...')
    

    # Verifica as diferenças entre os dados
    with open('./data/TCCs.json', 'r+', encoding='utf-8') as f:
        TCCs_novos = []
        TCCs_atualizados = []

        f.seek(0)
        savedTCCs = json.load(f)

        for tcc in parsedTCC:
            novoTCC = True
            # Verifica se o TCC é novo ou se teve alterações
            for savedTCC in savedTCCs:
                # Verifica se o TCC já está salvo e teve alterações
                if tcc['Aluno'] == savedTCC['Aluno'] and tcc != savedTCC:
                    savedTCCs[savedTCCs.index(savedTCC)] = tcc
                    TCCs_atualizados.append(tcc)
                    if(echo):
                        cprint(f'\tTCC atualizado: {tcc["Aluno"]}', 'yellow')
                    novoTCC = False
                    break
                # Verifica se o TCC já está salvo
                elif tcc['Aluno'] == savedTCC['Aluno']:
                    novoTCC = False
                    break
            
            # Salva o TCC se for novo
            if novoTCC:
                savedTCCs.append(tcc)
                TCCs_novos.append(tcc)
                if(echo):
                    cprint(f'Novo TCC: {tcc["Aluno"]}', 'green')    
        if(len(TCCs_novos) == 0 and len(TCCs_atualizados) == 0 and echo):
            cprint('Nenhum TCC novo ou atualizado', 'black', 'on_green')
            return {'success': 'Nenhum TCC novo ou atualizado'}
        else:
            # Salva os TCCs atualizados
            f.seek(0)
            f.truncate()
            f.write(json.dumps(savedTCCs, ensure_ascii=False, indent=4))
            if(saveDiff):
            # Salva os TCCs novos e atualizados
                with open('./data/TCCs-novos.json', 'r+', encoding='utf-8') as f:
                    if(f.read() == ''):
                        f.write(json.dumps(TCCs_novos, ensure_ascii=False, indent=4))
                    else:
                        f.seek(0)
                        TCCs_novos = json.load(f) + TCCs_novos
                        f.seek(0)
                        f.truncate()
                        f.write(json.dumps(TCCs_novos, ensure_ascii=False, indent=4))
                with open('./data/TCCs_atualizados.json', 'r+', encoding='utf-8') as f:
                    if(f.read() == ''):
                        f.write(json.dumps(TCCs_atualizados, ensure_ascii=False, indent=4))
                    else:
                        f.seek(0)
                        TCCs_atualizados = json.load(f) + TCCs_atualizados
                        f.seek(0)
                        f.truncate()
                        f.write(json.dumps(TCCs_atualizados, ensure_ascii=False, indent=4))
                        
            if(echo):
                cprint('TCCs obtidos com sucesso', 'green')
            return {'success': 'TCCs obtidos com sucesso'}