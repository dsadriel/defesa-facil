"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

from PIL import Image, ImageDraw
import json
from lib.tcc.imagemStories import modeloTCCStories
from lib.tcc.imagemFeed import modeloTCCFeed
from lib.obterNovosTCCs import obterNovosTCCs
from lib.gerarCalendariosCSV import gerarCalendarioPrompt

importar_do_portal = ''
while(importar_do_portal != 's' and importar_do_portal != 'n'):
    importar_do_portal = input('Deseja importar os dados dos TCCs do portal? (s/n): ').lower()

if importar_do_portal == 's':
    obterNovosTCCs()


origem = ''
origem_tipos = {'n': 'novos', 'a': 'atualizados', 't': 'todos'}
while(origem not in origem_tipos.keys() and origem not in origem_tipos.values()):
    origem = input('Deseja gerar imagens para os TCCs (n)ovos, (a)tualizados ou (t)odos? ').lower()

if(len(origem) == 1):
    origem = origem_tipos[origem]

if(origem != 'todos'):
    origem = f'./data/TCCs-{origem}.json'
else:
    origem = './data/TCCs.json'

print('Carregando dados dos TCCs...')

# Carrega os dados dos TCCs e gera as imagens de teste
with open(origem, 'r', newline='', encoding='UTF-8') as f:
    dados = json.load(f)
    

    # Gera imagens para o feed
    ecp = filter(lambda x: x['Curso'] == 'Engenharia de Computação', dados)
    ecp = sorted(ecp, key=lambda x: x['Data'])
    ecp = [ecp[i:i+2] for i in range(0, len(ecp), 2)]
    for s in ecp:
        modeloTCCFeed(s)
        print(f'Gerado {modeloTCCFeed.counter} de {len(dados)/2} imagens para feed', end='\r')

    cic = filter(lambda x: x['Curso'] == 'Ciência da Computação', dados)
    cic = sorted(cic, key=lambda x: x['Data'])
    cic = [cic[i:i+2] for i in range(0, len(cic), 2)]
    for s in cic:
        modeloTCCFeed(s)
        print(f'Gerado {modeloTCCFeed.counter} de {len(dados)/2} imagens para feed', end='\r')
    
    # Gera imagens para o stories
    print('\n')
    ecp = filter(lambda x: x['Curso'] == 'Engenharia de Computação', dados)
    ecp = sorted(ecp, key=lambda x: x['Data'])
    ecp = [ecp[i:i+4] for i in range(0, len(ecp), 4)]
    for s in ecp:
        modeloTCCStories(s, '2024/1')
        print(f'Gerado {modeloTCCStories.counter} de {len(ecp)} imagens para stories ECP', end='\r')
    
    print('\n')
    modeloTCCStories.counter = 0
    cic = filter(lambda x: x['Curso'] == 'Ciência da Computação', dados)
    cic = sorted(cic, key=lambda x: x['Data'])
    cic = [cic[i:i+4] for i in range(0, len(cic), 4)]
    for s in cic:
        modeloTCCStories(s, '2024/1')
        print(f'Gerado {modeloTCCStories.counter} de {len(cic)} imagens para stories CIC', end='\r')


gerar_calendario = ''
while(gerar_calendario != 's' and gerar_calendario != 'n'):
    gerar_calendario = input('Deseja gerar o calendário de apresentações? (s/n): ').lower()

if(gerar_calendario == 's'):
   gerarCalendarioPrompt()