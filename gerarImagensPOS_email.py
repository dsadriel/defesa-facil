"""
DefesaFácil: Solução para criação de imagens de defesas de TCC, mestrado e doutorado
Desenvolvido por Adriel de Souza (adsouza@inf.ufrgs.br)
"""

from lib.pos.imagemFeed import modeloDefesaFeed
from lib.pos.imagemTotem import modeloDefesaTotem
from lib.interpretadorDados import intepretarDados
import os
from lib.ctk_dialog import CTkDialog


import customtkinter
import pyperclip

# Inicializa a aplicação
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  
app = customtkinter.CTk() 
app.title("Gerar imagens de defesa de POS a partir de email")
app.iconbitmap('assets/img/icon.ico')
app.grid_columnconfigure((0, 1), weight=1)


# Define a posição dos elementos na tela
padx = 5
pady = 5
sticky = 'ew'

# Adiciona o campo para título do card
customtkinter.CTkLabel(app, text="Título do card:").grid(row=0, column=0, padx=20, pady=20)
_tituloCard = customtkinter.CTkEntry(app, placeholder_text="Em branco para automático")
_tituloCard.grid(row=0, column=1, padx=padx, pady=pady, sticky=sticky)

# Campo para escala do título
customtkinter.CTkLabel(app, text="Escala do título:").grid(row=1, column=0, padx=padx, pady=pady, sticky=sticky)
_escalaCard = customtkinter.CTkEntry(app, placeholder_text="1 para normal")
_escalaCard .grid(row=1, column=1, padx=padx, pady=pady, sticky=sticky)


# Adiciona o campo para o conteúdo do email
_conteudoEmail = customtkinter.CTkTextbox(app, height=200, width=600)
_conteudoEmail.grid(row=2, column=0, columnspan=2, padx=padx, pady=pady, sticky=sticky)



def button_function():
    """
    Função que é chamada ao clicar no botão de gerar imagens.
    """

    global _tituloCard, _escalaCard, _conteudoEmail

    # Pega os valores dos campos e interpreta os dados do email
    conteudoEmail = _conteudoEmail.get('1.0', 'end-1c')
    escalaCard = float(_escalaCard.get().replace(',', '.')) if _escalaCard.get() else 1
    tituloCard = _tituloCard.get() if _tituloCard.get() else None
    dados = intepretarDados('pos', 'email', conteudoEmail)

    if(not dados):
        CTkDialog('Erro', 'Não foi possível interpretar os dados do email')
    
    ## Se o título não for informado, usa o 
    if(not tituloCard):
        tituloCard = dados['Tipo'] if dados['Tipo'] else 'Tese de Doutorado'
    
    print(escalaCard)
    modeloDefesaFeed(tituloCard, dados, escalaCard)
    modeloDefesaTotem(tituloCard, dados, escalaCard)
    print(dados)
    
    os.startfile('output\\imagens')
    
    textoParaPostagem = f"{tituloCard.title()} - PPGC 📚\n\nAluno(a): {dados['Aluno']}\nOrientador(a): {dados['Orientador']}\n"
    textoParaPostagem += f'Coorientador(a): {dados['Coorientador']}\n' if dados['Coorientador'] else ''
    textoParaPostagem += f"\"{dados['Titulo']}\"\n\nData: {dados['Data']}\nHorário: {dados['Hora'].replace(':', 'h')}\n{dados['Local']}"

    CTkDialog('Sucesso', f'Imagens geradas com sucesso!\n\nTexto para postagem copiado para a área de transferência.')
    pyperclip.copy(textoParaPostagem)
# Adiciona o botão para gerar as imagens
customtkinter.CTkButton(master=app, text="Gerar imagens", command=button_function).grid(row=4, column=0,
                                                                                        columnspan=2, padx=padx, pady=pady, sticky=sticky)

# Inicia a aplicação
app.mainloop()
