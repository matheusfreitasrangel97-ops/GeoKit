# A linha abaixo importa o módulo 'os' (do inglês Operating System - Sistema Operacional), permitindo criar, ler e manipular pastas e caminhos de arquivos no Windows.
import os

# A linha abaixo importa o módulo 'sys' (do inglês System - Sistema), usado para acessar o interpretador Python e caminhos de arquivos em execução.
import sys

# A linha abaixo importa o módulo 'json' para ler e processar o arquivo de versão remota codificado no formato estruturado de dados JSON.
import json

# A linha abaixo importa o módulo 'shutil' (do inglês Shell Utilities - Utilitários de Linha de Comando), utilizado aqui para apagar pastas inteiras de forma segura.
import shutil

# A linha abaixo importa o módulo 'zipfile', que serve para ler e descompactar arquivos comprimidos (arquivos de extensão .zip).
import zipfile

# A linha abaixo importa o módulo 'tempfile', usado para descobrir onde fica a pasta temporária do Windows para salvar downloads provisórios.
import tempfile

# A linha abaixo importa o módulo 'subprocess', utilizado para iniciar novos processos no sistema, como rodar scripts em lote do Windows (.bat).
import subprocess

# A linha abaixo importa o componente de requisições de rede da biblioteca padrão do Python para buscar dados e arquivos da internet.
import urllib.request

# A linha abaixo importa a gestão de erros de rede para tratar falhas de internet ou quedas de conexão.
import urllib.error

# A linha abaixo importa o módulo de paralelismo (processos paralelos - threads), permitindo que a verificação de versão ocorra sem travar a interface gráfica do programa.
import threading

# A linha abaixo importa uma ferramenta específica para comparação inteligente de números de versão de software (ex: comparar "1.10" com "1.9").
from distutils.version import LooseVersion

# A linha abaixo define uma constante contendo o link da internet onde está hospedado o arquivo com as informações da versão mais recente do GeoKit.
VERSION_URL = "https://raw.githubusercontent.com/matheusfreitasrangel97-ops/GeoKit/main/version.json"

# A linha abaixo inicia a definição da função para buscar atualizações em segundo plano.
# Ela recebe a versão atual rodando e uma função de retorno (callback) que será chamada se houver atualização.
def check_for_updates(current_version: str, callback):
    """
    Verifica atualizações em segundo plano por meio de uma tarefa paralela (thread em segundo plano).
    Se uma nova versão estiver disponível, chama a função de retorno (callback) fornecendo a nova versão, URL e as notas.
    """
    # A linha abaixo define uma função interna que será o alvo da execução paralela (tarefa em segundo plano - thread).
    def thread_target():
        # A linha abaixo abre um bloco 'try' para capturar qualquer erro de rede ou processamento de dados sem que o aplicativo trave.
        try:
            # A linha abaixo configura os dados da requisição na rede (conexão HTTP), incluindo um cabeçalho 'User-Agent' (identificação do programa na rede) para identificar que é o atualizador do GeoKit.
            req = urllib.request.Request(
                VERSION_URL, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoKitUpdater'}
            )
            # A linha abaixo abre a conexão com a URL de verificação, estipulando um limite de tempo máximo de espera (timeout) de 5 segundos.
            with urllib.request.urlopen(req, timeout=5) as response:
                # A linha abaixo lê o conteúdo retornado pela internet, converte de bytes para texto UTF-8 (codificação de acentos) e decodifica as informações JSON para um dicionário Python.
                data = json.loads(response.read().decode('utf-8'))
                # A linha abaixo obtém a versão remota declarada no arquivo version.json.
                remote_version = data.get("version")
                # A linha abaixo obtém o link do instalador/atualizador correspondente.
                update_url = data.get("url", "https://github.com/matheusfreitasrangel97-ops/GeoKit")
                # A linha abaixo obtém o texto das notas de atualização (mudanças e novidades).
                notes = data.get("notes", "")

                # A linha abaixo verifica se a versão remota foi lida com sucesso do arquivo JSON.
                if remote_version:
                    # Inicia um bloco interno para comparar as versões com segurança.
                    try:
                        # A linha abaixo tenta verificar se a versão remota é maior/mais nova que a versão atual usando o LooseVersion.
                        is_newer = LooseVersion(remote_version) > LooseVersion(current_version)
                    # Caso a biblioteca de comparação de versões falhe ou não esteja disponível, executa o bloco alternativo.
                    except Exception:
                        # A linha abaixo faz a comparação quebrando o número da versão por pontos (ex: "1.1.0" vira (1, 1, 0)) e comparando as tuplas de números.
                        is_newer = tuple(map(int, remote_version.split('.'))) > tuple(map(int, current_version.split('.')))

                    # A linha abaixo verifica se a versão encontrada é realmente mais nova.
                    if is_newer:
                        # Em caso positivo, aciona a função de retorno informando a nova versão, o link de download e as notas da versão.
                        callback(remote_version, update_url, notes)
        # Se ocorrer qualquer falha durante a verificação (ex: sem internet), captura a exceção em silêncio para não incomodar o usuário.
        except Exception:
            # A linha abaixo apenas indica ao Python para não fazer nada e seguir em frente caso ocorra um erro.
            pass

    # A linha abaixo cria a nova thread em segundo plano (comportamento de daemon, que fecha o processo paralelo de forma automática quando a tela principal do programa é encerrada) passando a função alvo.
    thread = threading.Thread(target=thread_target, daemon=True)
    # A linha abaixo inicia a execução paralela da nossa thread.
    thread.start()


# A linha abaixo define a função que faz o download do instalador e executa a instalação local da atualização.
# Ela recebe o link do instalador, e funções de retorno para notificar o progresso, a conclusão e erros.
def download_and_install_update(download_url: str, progress_callback, completion_callback, error_callback):
    """
    Baixa o arquivo ZIP de atualização em uma thread secundária, reporta o progresso de download,
    descompacta o pacote, gera um script em lote (.bat) de instalação automática, executa-o e encerra o app principal.
    """
    # A linha abaixo cria a função que executará todo o download e descompactação em paralelo para não travar a tela principal do programa.
    def thread_target():
        # A linha abaixo abre o bloco para captura de falhas durante todo o processo de download e extração de arquivos.
        try:
            # A linha abaixo cria a requisição de conexão na rede (HTTP) contendo cabeçalhos de identificação do navegador para efetuar a transferência do arquivo (download) com segurança.
            req = urllib.request.Request(
                download_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoKitUpdater'}
            )
            # A linha abaixo abre a transferência do instalador (download) da internet, com limite de 20 segundos para conexão inicial (timeout).
            with urllib.request.urlopen(req, timeout=20) as response:
                # A linha abaixo lê o tamanho total do arquivo declarado nos metadados do servidor (cabeçalho de tamanho Content-Length).
                content_length = response.getheader('Content-Length')
                # A linha abaixo converte esse tamanho total para número inteiro de bytes, caso essa informação esteja disponível na resposta da rede.
                total_size = int(content_length) if content_length else 0
                
                # A linha abaixo inicializa a contagem de bytes que já foram baixados até o momento.
                downloaded_size = 0
                # A linha abaixo define o tamanho do bloco (buffer) de dados que leremos por vez da internet (16 Kilobytes).
                block_size = 16384
                
                # A linha abaixo obtém o caminho padrão da pasta de arquivos temporários do sistema operacional Windows.
                temp_dir = tempfile.gettempdir()
                # A linha abaixo define o caminho e nome final do arquivo ZIP temporário que será gerado pelo download.
                zip_path = os.path.join(temp_dir, "GeoKit_update.zip")
                
                # A linha abaixo abre o arquivo temporário ZIP para gravação em modo binário ('wb').
                with open(zip_path, 'wb') as f:
                    # Inicia um laço de repetição infinito para ir puxando blocos de dados da internet.
                    while True:
                        # A linha abaixo lê um pequeno pedaço de dados do download da internet.
                        buffer = response.read(block_size)
                        # A linha abaixo verifica se os dados acabaram (fim do arquivo). Se sim, sai do laço.
                        if not buffer:
                            break
                        # A linha abaixo escreve o bloco binário recém-baixado no arquivo temporário.
                        f.write(buffer)
                        # A linha abaixo soma o tamanho do bloco baixado ao total acumulado.
                        downloaded_size += len(buffer)
                        
                        # A linha abaixo verifica se o servidor nos informou o tamanho total do arquivo para podermos calcular a porcentagem de progresso.
                        if total_size > 0:
                            # A linha abaixo calcula a porcentagem concluída (entre 0.0 e 1.0).
                            percent = downloaded_size / total_size
                            # A linha abaixo chama a função de progresso informando a porcentagem e os tamanhos baixados convertidos para Megabytes (MB).
                            progress_callback(percent, downloaded_size / (1024 * 1024), total_size / (1024 * 1024))
                        # Se o servidor de download não nos informou o tamanho total do arquivo anteriormente.
                        else:
                            # A linha abaixo chama a função de progresso passando o valor de -1 (progresso indeterminado) e os MB acumulados.
                            progress_callback(-1, downloaded_size / (1024 * 1024), 0.0)
                
                # A linha abaixo define o nome da pasta temporária onde os arquivos internos do ZIP serão extraídos.
                extract_dir = os.path.join(temp_dir, "GeoKit_extracted")
                # A linha abaixo verifica se a pasta temporária de extração já existia de tentativas anteriores.
                if os.path.exists(extract_dir):
                    # Se existia, remove a pasta inteira e todos os seus arquivos internos para evitar conflitos de versão.
                    shutil.rmtree(extract_dir)
                # A linha abaixo cria a pasta temporária de extração vazia no sistema de arquivos.
                os.makedirs(extract_dir, exist_ok=True)
                
                # A linha abaixo abre o arquivo ZIP recém-baixado em modo de leitura ('r').
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # A linha abaixo extrai todos os arquivos contidos dentro do arquivo ZIP para a pasta temporária criada.
                    zip_ref.extractall(extract_dir)
                
                # A linha abaixo verifica as propriedades do interpretador Python para descobrir se o programa roda a partir do código-fonte ou de um executável independente (.exe).
                if getattr(sys, 'frozen', False):
                    # Se for executável independente (.exe), obtém o caminho absoluto do arquivo executável do aplicativo.
                    app_executable = sys.executable
                    # A linha abaixo obtém a pasta atual onde está gravado o arquivo executável no seu computador.
                    app_dir = os.path.dirname(app_executable)
                    # A linha abaixo extrai apenas o nome do arquivo executável (ex: "GeoKit.exe").
                    exe_name = os.path.basename(app_executable)
                    # A linha abaixo marca a variável de controle informando que o programa está rodando em formato compilado.
                    is_frozen = True
                # Caso o programa esteja sendo executado como um script Python convencional (.py).
                else:
                    # A linha abaixo define o executável do sistema como o interpretador Python ativo.
                    app_executable = sys.executable
                    # A linha abaixo obtém a pasta onde está gravado o arquivo de script inicial ("main.py").
                    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                    # A linha abaixo define o nome do executável compilado como nulo, pois não se trata de um .exe empacotado.
                    exe_name = None
                    # A linha abaixo define que o programa não está rodando de forma compilada.
                    is_frozen = False
                
                # A linha abaixo define o caminho e nome do arquivo de script de comandos em lote (arquivo .bat do Windows) a ser gerado para fazer a instalação definitiva.
                bat_path = os.path.join(temp_dir, "geokit_install.bat")
                
                # A linha abaixo cria e abre o arquivo script .bat para escrita usando a codificação de texto UTF-8.
                with open(bat_path, 'w', encoding='utf-8') as bat_file:
                    # Escreve o comando de desativar exibição de linhas de código na tela do terminal.
                    bat_file.write("@echo off\n")
                    # Escreve o comando para mudar a página de código do terminal do Windows (prompt de comando) para suportar acentuação em português (UTF-8).
                    bat_file.write("chcp 65001 > nul\n")
                    # Imprime divisórias de decoração visual no console do Windows.
                    bat_file.write("echo =======================================================\n")
                    # Imprime a informação da instalação no console do Windows.
                    bat_file.write("echo Instalando Atualização do GeoKit...\n")
                    # Imprime divisórias de decoração visual no console do Windows.
                    bat_file.write("echo =======================================================\n")
                    # Imprime mensagem avisando que está aguardando o encerramento do processo do GeoKit atual para liberar escrita.
                    bat_file.write("echo Aguardando o GeoKit fechar completamente...\n")
                    
                    # Se o aplicativo for um executável independente (.exe) compilado.
                    if is_frozen and exe_name:
                        # Cria um ponto de marcação (ancoragem) no laço de repetição (loop) do lote.
                        bat_file.write(f":wait_loop\n")
                        # Verifica na lista de processos do Windows se o GeoKit.exe ainda está em execução ativa.
                        bat_file.write(f"tasklist /fi \"IMAGENAME eq {exe_name}\" 2>NUL | find /I /N \"{exe_name}\" >NUL\n")
                        # Se o comando encontrar o processo rodando (código de erro igual a 0).
                        bat_file.write(f"if \"%ERRORLEVEL%\"==\"0\" (\n")
                        # Aguarda exatamente 1 segundo antes de tentar verificar novamente.
                        bat_file.write(f"    timeout /t 1 /nobreak >nul\n")
                        # Redireciona o script de volta para o ponto inicial de verificação criando um laço.
                        bat_file.write(f"    goto wait_loop\n")
                        # Fecha a instrução condicional do lote.
                        bat_file.write(f")\n")
                    # Caso o programa esteja sendo executado via interpretador de script Python padrão.
                    else:
                        # Aguarda exatamente 2 segundos de margem de segurança para o script atual ser finalizado.
                        bat_file.write("timeout /t 2 /nobreak > nul\n")
                        
                    # Imprime mensagem informando o início da cópia dos novos arquivos baixados sobre a versão atual.
                    bat_file.write("echo Copiando novos arquivos...\n")
                    # Copia todos os arquivos extraídos temporariamente para a pasta original do aplicativo, sobrescrevendo os arquivos antigos (/y), incluindo subpastas vazias ou com arquivos (/e /s) e forçando a criação caso a pasta não exista (/i).
                    bat_file.write(f"xcopy /y /e /s /i \"{extract_dir}\\*.*\" \"{app_dir}\\\" >nul\n")
                    
                    # Imprime mensagem no console indicando que reiniciará o aplicativo.
                    bat_file.write("echo Reiniciando o GeoKit...\n")
                    # Se for executável independente, inicia novamente o executável atualizado.
                    if is_frozen:
                        bat_file.write(f"start \"\" \"{app_executable}\"\n")
                    # Se estiver rodando como código fonte, chama o interpretador python passando o arquivo de script principal.
                    else:
                        main_py_path = os.path.join(app_dir, "main.py")
                        bat_file.write(f"start \"\" \"{app_executable}\" \"{main_py_path}\"\n")
                        
                    # Imprime mensagem avisando sobre a limpeza de resíduos criados durante a atualização.
                    bat_file.write("echo Limpando arquivos temporarios...\n")
                    # Apaga a pasta temporária onde descompactamos os arquivos da nova versão.
                    bat_file.write(f"rd /s /q \"{extract_dir}\"\n")
                    # Apaga o arquivo comprimido ZIP que foi baixado inicialmente.
                    bat_file.write(f"del /q \"{zip_path}\"\n")
                    # Imprime mensagem sinalizando a conclusão total de todas as etapas.
                    bat_file.write("echo Concluido com sucesso!\n")
                    # Remove o próprio arquivo .bat temporário da memória do disco rígido após a sua execução.
                    bat_file.write("del \"%~f0\"\n")
                
                # A linha abaixo usa o subprocesso para executar o arquivo script .bat criado no Windows abrindo uma nova tela de console independente.
                subprocess.Popen(
                    [bat_path], 
                    shell=True, 
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                
                # Aciona a função de retorno de sucesso após disparar o atualizador de lote no Windows.
                completion_callback()
                
        # Caso ocorra qualquer tipo de problema técnico (ex: falha de download ou disco cheio), captura o erro.
        except Exception as e:
            # Aciona a função de retorno de falha descrevendo o erro encontrado.
            error_callback(str(e))

    # A linha abaixo encapsula toda a lógica descrita acima em uma thread de processamento independente.
    thread = threading.Thread(target=thread_target, daemon=True)
    # A linha abaixo inicia a execução paralela de nossa thread de download e atualização.
    thread.start()
