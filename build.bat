@echo off
rem A linha abaixo desativa a exibição dos comandos na tela do console enquanto o script é executado, mantendo a visualização limpa.

rem As linhas abaixo imprimem mensagens de boas-vindas e decoração no terminal do sistema.
echo =======================================================
echo Compilador GeoKit (Distribuicao Executavel Unico)
echo =======================================================
rem A linha abaixo imprime uma linha em branco no console para espaçamento visual.
echo.

rem A linha abaixo imprime a indicação da primeira etapa (limpeza de resíduos de compilações anteriores).
echo [1/3] Limpando arquivos de builds anteriores...
rem A linha abaixo verifica se a pasta 'build' existe no diretório atual. Se existir, apaga a pasta e todo o seu conteúdo silenciosamente (/s /q).
if exist build rmdir /s /q build
rem A linha abaixo verifica se a pasta 'dist' existe. Se existir, apaga ela e todos os seus arquivos internos para evitar conflito com a nova versão.
if exist dist rmdir /s /q dist
rem Observação: Não deletamos o arquivo GeoKit.spec para preservar seus comentários didáticos explicativos em português.
echo.

rem As linhas abaixo imprimem no console a mensagem de início da compilação do novo executável.
echo [2/3] Iniciando empacotamento baseado no build_spec.py...
echo Isso pode levar alguns minutos. Aguarde...
rem A linha abaixo chama o interpretador Python instalado localmente no ambiente virtual do projeto (.venv) para rodar o script 'build_spec.py'.
call .venv\Scripts\python.exe build_spec.py
rem A linha abaixo imprime uma linha vazia para separar os blocos de mensagens.
echo.

rem As linhas abaixo imprimem no terminal as instruções de encerramento do processo e mostram onde o arquivo executável final foi gerado.
echo [3/3] Processo finalizado!
echo =======================================================
echo O seu aplicativo pronto para uso esta localizado na pasta:
rem Imprime o caminho completo da pasta 'dist' utilizando a variável de ambiente '%CD%' que representa o diretório atual de trabalho.
echo %CD%\dist
echo.
echo Para abrir o programa, basta executar o arquivo:
rem Imprime a rota completa para o arquivo executável definitivo GeoKit.exe.
echo %CD%\dist\GeoKit.exe
echo =======================================================
rem A linha abaixo pausa a execução do script e exibe a mensagem "Pressione qualquer tecla para continuar...".
rem Isso evita que a janela do terminal feche instantaneamente, permitindo ao usuário ler o relatório de compilação.
pause
