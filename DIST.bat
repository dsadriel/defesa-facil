@echo off
REM Compila os scripts Python em executáveis usando PyInstaller
REM --onefile: Gera um único arquivo executável
REM --windowed: Não exibe o terminal ao executar o programa
REM --icon: Define o ícone do executável
REM --distpath: Define o caminho onde os executáveis serão gerados

pyinstaller --onefile --windowed --icon=./assets/img/icon.ico --distpath ../dist gerarImagensPOS_email.py
pyinstaller --onefile --windowed --icon=./assets/img/icon.ico --distpath ../dist gerarImagensTCC_GUI.py

REM Copia os arquivos necessários para a pasta de distribuição
REM /s: Copia subdiretórios
REM /e: Copia subdiretórios, mesmo que estejam vazios
REM /i: Considera o destino como um diretório
REM /y: Substitui arquivos existentes sem pedir confirmação

xcopy /s /e /i /y assets ..\dist\assets
xcopy /s /e /i /y data ..\dist\data
xcopy /s /e /i /y output ..\dist\output

REM Remove arquivos de compilação temporários e cache
REM O PyInstaller gera pastas de build e cache que podem ser limpas após a compilação.
if exist build rd /s /q build
if exist __pycache__ rd /s /q __pycache__
if exist *.spec del /q *.spec

REM Pausa para o usuário visualizar as mensagens no console
pause
