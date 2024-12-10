"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

import datetime
import os
import re
import customtkinter
import json
from lib.tcc.imagemStories import modeloTCCStories
from lib.tcc.imagemFeed import modeloTCCFeed
from lib.obterNovosTCCs import obterNovosTCCs
from lib.gerarCalendariosCSV import gerarCalendarioEventos
from lib.ctk_dialog import CTkDialog

  

# Inicializa a aplicação
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("green")  
app = customtkinter.CTk() 
app.title("Gerar imagens de defesa de TCCs")
app.iconbitmap('assets/img/icon.ico')
app.grid_columnconfigure((0, 1), weight=1)


# Define as variáveis que serão usadas
variables = {
    'data_inicio': customtkinter.StringVar(value=datetime.date.today().strftime('%d/%m/%Y')),
    'intervalo': customtkinter.StringVar(value=6)
    }

listaTCCs = []

def filtrarDatas(elemento, data_inicio = None, intervalo = None):
    """
    Função que filtra os elementos de acordo com a data de início e intervalo

    Args:
        elemento (dict): Elemento a ser filtrado
        data_inicio (datetime.date): Data de início
        intervalo (int): Intervalo de dias

    Returns:
        bool: Retorna True se o elemento está dentro do intervalo
    """
    if not data_inicio or not intervalo:
        data_inicio = variables['data_inicio'].get()
        intervalo = int(variables['intervalo'].get())


    data_evento = datetime.datetime.strptime(elemento['Data'], '%d/%m/%Y').date()
    data_inicio = datetime.datetime.strptime(data_inicio, '%d/%m/%Y').date()
    
    return data_evento >= data_inicio and data_evento <= data_inicio + datetime.timedelta(days=intervalo)


def buscarDados(e = None):
    """
    Função que que busca os dados no JSON local de acordo com a data de início e intervalo

    Args:
        e (Event): Evento que chamou a função
    """

    global listaTCCs
    global variables

    data_inicio = variables['data_inicio'].get()
    intervalo = variables['intervalo'].get()
    if(re.search(r'^\d{2}/\d{2}/\d{4}$', data_inicio) == None):
        CTkDialog('Erro', 'Data de início inválida')
        return
    if(re.search(r'^\d+$', intervalo) == None):
        CTkDialog('Erro', 'Intervalo inválido')
        return
    
    
    with open('./data/TCCs.json', 'r', newline='', encoding='UTF-8') as f:
        json_ = json.load(f)
        filtered = list(filter(filtrarDatas, json_))

        listaTCCs = filtered
    
    nomes.configure(text=f"Apresentações no intervalo selecionado [{len(listaTCCs)}]:\n {', \n'.join([f'{x['Aluno']} ({x['Curso']})' for x in listaTCCs])}")

def importarDadosDoPortal():
    """
    Busca os TCCs no portal de serviços do INF. Utiliza a função obterNovosTCCs do arquivo obterNovosTCCs.py para isso.
    """
    global ultima_atualizacao
    global btn_importarPortal

    ultima_atualizacao.configure(text="Última atualização: Aguarde...")
    btn_importarPortal.configure(state='disabled') # Desabilita o botão de importar

    app.after(100, importarDadosDoPortal_) # Delay the execution of processarDadosDoPortal function


def importarDadosDoPortal_():
    global ultima_atualizacao
    global btn_importarPortal

    message = obterNovosTCCs(False, False) # Obtem os TCCs do portal

    # Exibe mensagens de erro ou sucesso
    for key in message:
        if key == 'error':
            CTkDialog('Erro', message[key])
            ultima_atualizacao.configure(text=f"Ocorreu um erro ao buscar os TCCs")
            return
        elif key == 'success':
            CTkDialog('Sucesso', message[key])
            ultima_atualizacao.configure(text=f"Última atualização: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            return
        else:
            CTkDialog(key, message[key])
            ultima_atualizacao.configure(text=f"Ocorreu um erro ao buscar os TCCs")

    btn_importarPortal.configure(state='normal') # Habilita o botão de importar



def gerarImagens(stories = True, feed = False):
    global listaTCCs
    dados = listaTCCs

    if(len(dados) == 0):
        CTkDialog('Erro', 'Nenhum TCC encontrado')
        return
    
    ecp = sorted(filter(lambda x: x['Curso'] == 'Engenharia de Computação', dados), key=lambda x: x['Data'])
    cic = sorted(filter(lambda x: x['Curso'] == 'Ciência da Computação', dados), key=lambda x: x['Data'])

    if(feed):
        grupos = [ecp[i:i+2] for i in range(0, len(ecp), 2)] # Agrupa de 2 em 2
        for s in grupos:
            modeloTCCFeed(s)

        groupos = [cic[i:i+2] for i in range(0, len(cic), 2)] # Agrupa de 2 em 2
        for s in groupos:
            modeloTCCFeed(s)
    
    if(stories):
        grupos = [ecp[i:i+4] for i in range(0, len(ecp), 4)] # Agrupa de 4 em 4
        for s in grupos:
            modeloTCCStories(s, '2024/1')
        
        grupos = [cic[i:i+4] for i in range(0, len(cic), 4)] # Agrupa de 4 em 4
        for s in grupos:
            modeloTCCStories(s, '2024/1')

    os.startfile('output\\imagens')
    CTkDialog('Sucesso', 'Imagens geradas com sucesso')

def gerarCalendario():
    global listaTCCs
    global variables
    gerarCalendarioEventos(listaTCCs, nome_arquivo=f"TCCs_{variables['data_inicio'].get().replace('/', '-')}_{variables['intervalo'].get()}")
    CTkDialog('Sucesso', 'Calendário gerado com sucesso\nVerifique a pasta output/calendario')


# Define a posição dos elementos na tela
padx = 5
pady = 5
sticky = 'ew'

# Linha 0
btn_importarPortal = customtkinter.CTkButton(master=app, text="Buscar TCCs no portal", command=importarDadosDoPortal)
btn_importarPortal.grid(row=0, column=0, columnspan=1, padx=padx, pady=pady, sticky=sticky)

ultima_atualizacao = customtkinter.CTkLabel(app, text="Última atualização: ", justify="left")
ultima_atualizacao.grid(row=0, column=1, columnspan=2, padx=padx, pady=pady, sticky='w')
ultima_atualizacao.configure(text=f"Última atualização: {datetime.datetime.fromtimestamp(os.path.getmtime('./data/TCCs.json')).strftime('%d/%m/%Y %H:%M:%S')}")


# Linha 1
customtkinter.CTkLabel(app, text="Data de ínicio:").grid(row=1, column=0, padx=20, pady=20)
data_ini =  customtkinter.CTkEntry(app, textvariable=variables['data_inicio'])
data_ini.grid(row=1, column=1, padx=padx, pady=pady, sticky=sticky)
data_ini.bind("<Return>", buscarDados)

customtkinter.CTkLabel(app, text="Intervalo de dias:").grid(row=1, column=2, padx=20, pady=20)
intervalo = customtkinter.CTkEntry(app, textvariable=variables['intervalo'])
intervalo.grid(row=1, column=4, padx=padx, pady=pady, sticky=sticky)
intervalo.bind("<Return>", buscarDados)

nomes = customtkinter.CTkLabel(app, text="")
nomes.grid(row=5, column=0, columnspan=5, sticky='ew')
nomes.configure(text="Nomes dos alunos: ")

# Adiciona o botão para gerar as imagens
customtkinter.CTkButton(master=app, text="Gerar imagens", command=gerarImagens).grid(row=4, column=0,
                                                                                        columnspan=2, padx=padx, pady=pady, sticky=sticky)
customtkinter.CTkButton(master=app, text="Gerar CSV calendário", command=gerarCalendario).grid(row=4, column=3,
                                                                                        columnspan=2, padx=padx, pady=pady, sticky=sticky)


# Inicia a aplicação
buscarDados()
app.mainloop()