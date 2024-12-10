"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

import csv
import datetime
import os
import json
from enum import Enum

def add30min(str):
    end_time = datetime.datetime.strptime(str, '%H:%M').time()
    end_time = (datetime.datetime.combine(datetime.date.today(), end_time) + datetime.timedelta(minutes=30)).time()
    return end_time.strftime('%H:%M')

def dadosParaLinha(d):
    """
    Função que recebe um dicionário contendo os dados de uma defesa de TCC e retorna uma linha formatada para ser adicionada a um calendário.

    Parâmetros:
    - d (dict): Dicionário contendo os dados da defesa de TCC, incluindo 'Data', 'Hora', 'Aluno', 'Curso', 'Titulo', 'Orientador', 'Coorientador' e 'Banca'.

    Retorna:
    - row (dict): Dicionário contendo os campos 'Title', 'Start', 'End', 'Categories' e 'Content' preenchidos com os dados formatados da defesa de TCC.
    """
    # Formata a data para o formato necessário
    formatedDate = '-'.join(tuple(d['Data'].split('/'))[::-1])

    # Cria a linha
    row = {
        'Title': f'TCC de {d['Aluno']}',
        'Start': formatedDate + ' ' + d['Hora'],
        'End': formatedDate + ' ' + add30min(d['Hora']),
        'Categories': 'TCC - ' + ('ECP' if d['Curso'].startswith('Engenharia') else 'CIC'),
        'Content': ''
    }

    # Adiciona o conteúdo
    row['Content'] += f'<b>Título do Trabalho:</b> {d['Titulo']}<br><b>Orientador(a):</b> {d['Orientador']}<br>'

    # Adiciona o coorientador se houver
    if(len(d['Coorientador']) > 1):
        row['Content']  += f'<b>Coorientador(a):</b> {d['Coorientador']}<br>'
    
    # Adiciona a banca e a data
    row['Content']  += f'<b>Banca:</b> {', '.join(d['Banca'])}<br>'
    row['Content']  += f'<b>Data:</b> {d['Data']} {d['Hora']} <br>'

    # Adiciona o link ou o local
    if(d['Local'].startswith('http')):
        row['Content']  += f'<b>Link:</b> <a href="{d['Local']}">{d['Local']}</a>'
    else:
        row['Content']  += f'<b>Local:</b> {d['Local']}'

    # Retorna a linha
    return row

def gerarCalendarioEventos(eventos:list, nome_arquivo:str = ""):
    """
    Gera um arquivo CSV contendo os eventos fornecidos.

    Args:
        eventos (list): Lista de eventos a serem adicionados ao calendário.
        nome_arquivo (str): Nome do arquivo a ser salvo.
    """
    if(nome_arquivo == ""):
        nome_arquivo = f'calendario-{datetime.date.today()}'
    else:
        nome_arquivo = f'calendario-{nome_arquivo}'

    CSVFile = open(f"./output/calendario/{nome_arquivo}.csv", 'w+', newline='')
    writer = csv.DictWriter(CSVFile, fieldnames=['Title', 'Start', 'End', 'Categories', 'Content'])
    writer.writeheader()
    
    for linha in eventos:
        writer.writerow(dadosParaLinha(linha))
    
    CSVFile.close()


def gerarCalendariosCSV(tipo:list, modo:list):
    """
    Função que gera um arquivo CSV contendo os eventos de TCCs, defesas e teses.

    Parâmetros:
    - tipo (list): Lista contendo os tipos de dados a serem adicionados ao calendário (1: TCCs, 2: defesas, 3: teses).
    - modo (list): Lista contendo os modos de dados a serem adicionados ao calendário (1: novos, 2: atualizados, 3: todos).
    """
    
    # Abre o arquivo CSV para escrita
    CSVFile = open(f"./output/calendario/calendario-{datetime.date.today()}.csv", 'w+', newline='')
    writer = csv.DictWriter(CSVFile, fieldnames=['Title', 'Start', 'End', 'Categories', 'Content'])
    writer.writeheader()
    i = 0

    for tipo in tipo:
        for modo in modo:
            fileName = ['TCCs', 'defesas', 'teses'][tipo] + ['-novos', '-atualizados', ''][modo] + '.json'

            # Carrega os dados
            with open('./data/' + fileName, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for linha in dados:
                    writer.writerow(dadosParaLinha(linha))

                print('Calendário gerado com sucesso!')
                if(len(dados) == 0):
                    print('Nenhum evento foi adicionado ao calendário')
                else:
                    print(f'{len(dados)} eventos foram adicionados ao calendário\n')

                if(modo == 2):
                    print('- Lembre-se de REMOVER os eventos antigos do CALENDÁRIO manualmente!')
                if(modo == 1 or modo == 2):
                    print(f'- Lembre-se de ATUALIZAR o arquivo {fileName} para evitar duplicatas!')


    CSVFile.close()
    print(f'\nArquivo salvo em: {os.path.join(os.getcwd(), f"\\output\\calendario\\calendario-{datetime.date.today()}.csv")}\n\n')

    print("Para saber como importar o arquivo gerado leia o arquivo 'README.MD' na pasta 'calendarios'")

def gerarCalendarioPrompt():
    print('Gerar calendário de apresentações de TCCs\n')
    origem_tipos = {'n': 0, 'a': 1, 't': 2}
    origem = ''
    while(origem not in origem_tipos.keys()):
        origem = input('Deseja gerar imagens para os TCCs (n)ovos, (a)tualizados ou (t)odos? ').lower()
    
    gerarCalendariosCSV([0], [origem_tipos[origem]])
    