# -*- coding: utf-8 -*-
# A linha acima declara a codificação UTF-8 do arquivo de texto para que o Python leia corretamente os caracteres acentuados em português.

# As linhas abaixo explicam didaticamente o propósito do script:
# Este é um script auxiliar para automatizar o envio (Upload/Carregamento) de uma nova versão (Release/Lançamento) do GeoKit diretamente para o repositório no GitHub.

# A linha abaixo importa o módulo 'os' para gerenciar arquivos, caminhos e variáveis de ambiente do sistema operacional.
import os

# A linha abaixo importa o módulo 'sys' para interagir com parâmetros do interpretador e saídas do sistema.
import sys

# A linha abaixo importa o módulo 'zipfile' para compactar os arquivos de código e o executável em um pacote ZIP antes de enviar.
import zipfile

# A linha abaixo importa o módulo 'json' para ler e processar arquivos no formato estruturado de dados JSON.
import json

# A linha abaixo importa a biblioteca 'requests', que serve para fazer requisições HTTP (enviar dados e se comunicar com APIs web, como a do GitHub).
import requests

# A linha abaixo importa o módulo 'subprocess' para executar comandos nativos do Git e do sistema através do prompt de comando.
import subprocess

# A linha abaixo define o caminho do repositório remoto no GitHub (nome do usuário/nome do projeto).
REPO = "matheusfreitasrangel97-ops/GeoKit"

# As linhas abaixo abrem e leem de forma dinâmica o arquivo 'version.json' para carregar a versão atual do software.
try:
    with open("version.json", "r", encoding="utf-8") as f_versao:
        dados_versao = json.load(f_versao)
        VERSION = dados_versao.get("version", "1.2.0")
except Exception:
    # Se a leitura falhar, define o valor padrão 1.2.0 por segurança.
    VERSION = "1.2.0"

# A linha abaixo define o nome da etiqueta (tag) correspondente a esta versão (por exemplo, "v1.2.0").
TAG_NAME = f"v{VERSION}"

# A linha abaixo define a função que busca o token (chave secreta de acesso) do GitHub.
def get_github_token():
    """Recupera a chave secreta de segurança (token do GitHub) armazenada no gerenciador de credenciais do Git local."""
    # Imprime no console a mensagem de busca de credenciais.
    print("Buscando a chave de segurança (token do GitHub) no gerenciador de credenciais do Git...")
    # Tenta usar o gerenciador de senhas do Git local para pegar a chave secreta (token) de forma segura.
    try:
        # Inicia um processo em segundo plano que executa o comando de preenchimento de credenciais do Git ('git credential fill').
        p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        # Envia os parâmetros informando que deseja as credenciais de acesso do site github.com.
        out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
        # Varre cada uma das linhas retornadas pelo gerenciador de credenciais do Git.
        for line in out.splitlines():
            # Se a linha de texto começar com 'password=' (onde fica guardada a senha ou chave de acesso).
            if line.startswith('password='):
                # Extrai o valor correspondente pulando o caractere de igual '='.
                token = line.split('=', 1)[1].strip()
                # Se a chave secreta (token) não for nula ou vazia.
                if token:
                    # Imprime mensagem de sucesso informando que o token foi carregado com sucesso do gerenciador de credenciais do Git.
                    print("Chave de segurança (token do GitHub) obtida com sucesso via auxiliar de credenciais do Git (Git Credential Helper).")
                    # Retorna a chave de acesso.
                    return token
    # Se ocorrer qualquer erro ou falha ao interagir com o gerenciador de credenciais do Git.
    except Exception as e:
        # Exibe mensagem de aviso com a falha encontrada.
        print(f"Aviso ao consultar credenciais do Git: {e}")
        
    # Procedimento alternativo: tenta ler a chave (token) a partir de uma variável de ambiente do sistema chamada 'GITHUB_TOKEN'.
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    # Se encontrou a chave na variável de ambiente do Windows.
    if token:
        # Exibe mensagem informando que o token foi carregado da variável de ambiente.
        print("Chave de segurança (token) obtida através da variável de ambiente GITHUB_TOKEN.")
        # Retorna a chave.
        return token
        
    # Retorna uma string vazia caso a chave de acesso não seja encontrada por nenhum procedimento.
    return ""

# A linha abaixo define a função principal que comanda as etapas de empacotamento, envio e publicação.
def main():
    # Chama a função definida anteriormente para buscar o token e guarda na variável 'token'.
    token = get_github_token()
    # Se a chave (token) não foi encontrada (está vazia).
    if not token:
        # Exibe mensagem de erro no console informando que o envio de atualizações falhou.
        print("ERRO: Chave de segurança (token do GitHub) não encontrada!")
        print("Certifique-se de estar autenticado no Git ou de configurar a variável de ambiente GITHUB_TOKEN.")
        # Encerra a execução do programa com código de falha 1.
        sys.exit(1)
        
    # 1. ETAPA DE REGISTRO E ENVIO (COMMIT E PUSH) DO CÓDIGO FONTE
    # Imprime no terminal o status da operação.
    print("Registrando localmente (commit) e enviando (push) as alterações para o GitHub...")
    # Tenta rodar os comandos básicos de controle de versão do Git.
    try:
        # Roda o comando 'git add' para registrar os arquivos de configuração na fila de alterações.
        subprocess.run(['git', 'add', 'build.bat', 'build_spec.py', 'geokit/__init__.py', 'version.json'], check=True)
        # Roda o comando 'git commit' (gravação local) adicionando um comentário descritivo informando a nova versão compilada.
        subprocess.run(['git', 'commit', '-m', f"Compilação: Atualização {VERSION} - Executável Único"], check=False)
        # Roda o comando 'git push origin main' (envio remoto) para enviar as updates do código fonte para o repositório remoto.
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        # Imprime mensagem confirmando a gravação definitiva do código no GitHub.
        print("Alterações registradas e enviadas para o repositório Git com sucesso!")
    # Se ocorrer alguma falha de sincronização do Git (ex: conflitos ou sem internet).
    except Exception as e:
        # Exibe o erro e interrompe a execução do script.
        print(f"Erro ao atualizar o repositório Git: {e}")
        sys.exit(1)

    # 2. ETAPA DE EMPACOTAMENTO NO ARQUIVO COMPRIMIDO ZIP
    # Imprime mensagem de início de criação do pacote ZIP.
    print(f"Iniciando empacotamento compactado do GeoKit v{VERSION}...")
    # Define o nome físico do arquivo ZIP final que conterá o programa completo.
    zip_filename = "GeoKit.zip"
    
    # Define as pastas que serão incluídas dentro do pacote ZIP de distribuição.
    include_dirs = ["geokit"]
    # Define os arquivos individuais na raiz do projeto que serão incluídos no pacote ZIP.
    include_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "build.bat",
        "build_spec.py",
        "version.json"
    ]
    
    # Se um arquivo ZIP com o mesmo nome já existir na raiz do projeto devido a criações antigas.
    if os.path.exists(zip_filename):
        # Remove o arquivo ZIP antigo para evitar misturar arquivos antigos com novos.
        os.remove(zip_filename)
        
    # Verifica se o arquivo executável compilado (.exe) do GeoKit não existe na pasta 'dist/'.
    if not os.path.exists("dist/GeoKit.exe"):
        # Mostra erro informando que o programa precisa ser compilado com o script de compilação antes de gerar a release.
        print("ERRO: O arquivo executável dist/GeoKit.exe não foi encontrado! Execute a compilação antes.")
        # Encerra a execução do script.
        sys.exit(1)

    # Cria e abre o arquivo compactado ZIP novo para escrita comprimida ('w').
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as z:
        # Grava o executável independente GeoKit.exe diretamente na pasta raiz dentro do arquivo ZIP.
        z.write("dist/GeoKit.exe", "GeoKit.exe")
        # Confirma a inclusão do executável.
        print("Adicionado arquivo executável GeoKit.exe na raiz do arquivo ZIP.")
        
        # Varre cada um dos arquivos listados na lista 'include_files'.
        for file in include_files:
            # Se o arquivo existir fisicamente no disco.
            if os.path.exists(file):
                # Escreve o arquivo no arquivo ZIP comprimido.
                z.write(file)
                # Confirma a inclusão do arquivo.
                print(f"Adicionado arquivo: {file}")
                
        # Varre as pastas listadas para inclusão de forma recursiva (todas as subpastas e arquivos internos).
        for directory in include_dirs:
            # Se a pasta existir no disco.
            if os.path.exists(directory):
                # Varre a estrutura interna da pasta usando 'os.walk'.
                for root, dirs, files in os.walk(directory):
                    # Ignora pastas temporárias do compilador Python ('__pycache__') para não inflar o arquivo de distribuição.
                    if "__pycache__" in root:
                        continue
                    # Varre todos os arquivos encontrados na pasta atual.
                    for file in files:
                        # Reconstrói a rota física absoluta do arquivo.
                        filepath = os.path.join(root, file)
                        # Adiciona o arquivo correspondente mantendo a sua estrutura original de pastas dentro do ZIP.
                        z.write(filepath)
                        # Confirma a inclusão do arquivo.
                        print(f"Adicionado: {filepath}")

    # Imprime no terminal sinalizando que o pacote compactado foi criado.
    print("ZIP gerado com sucesso!")
    
    # 3. ETAPA DE CRIAÇÃO DA VERSÃO DE LANÇAMENTO (RELEASE) NO GITHUB VIA CANAL DE INTEGRAÇÃO (API)
    # Imprime no terminal o início da comunicação remota.
    print("Conectando aos servidores do GitHub para criar o registro de Lançamento de Versão (Release)...")
    # Define os cabeçalhos de envio de dados contendo a chave de segurança (token) e o tipo de aceitação padrão da API.
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    
    # Define a URL padrão da API do GitHub para gerenciar Releases no repositório.
    release_url = f"https://api.github.com/repos/{REPO}/releases"
    # Define os dados estruturados de payload (conteúdo) que serão enviados na requisição para criar a Release.
    release_payload = {
        "tag_name": TAG_NAME,
        "target_commitish": "main",
        "name": TAG_NAME,
        "body": f"Atualização {VERSION} do GeoKit.\n\nNovidades:\n- Agora o GeoKit é compilado como um único arquivo executável standalone (.exe) sem dependência de outras pastas!\n- Inclusão dos scripts build_spec.py e build.bat corrigidos.",
        "draft": False,
        "prerelease": False
    }
    
    # Faz uma consulta (GET) à API do GitHub para verificar se já existe uma Release criada com essa etiqueta (tag).
    check_resp = requests.get(f"{release_url}/tags/{TAG_NAME}", headers=headers)
    # Se a resposta do servidor retornar código 200 (OK), significa que uma release para essa tag já existia no GitHub.
    if check_resp.status_code == 200:
        # Decodifica as informações da release existente em uma estrutura de dicionário.
        existing_release = check_resp.json()
        # Imprime mensagem avisando que deletará a release antiga correspondente para poder publicar a nova por cima.
        print(f"O Lançamento {TAG_NAME} já existe no servidor. Deletando versão anterior antiga (Identificador ID: {existing_release['id']}) para recriar...")
        # Envia uma requisição de deleção para os servidores do GitHub.
        del_resp = requests.delete(f"{release_url}/{existing_release['id']}", headers=headers)
        # Se a deleção retornou sucesso (código de retorno 204).
        if del_resp.status_code == 204:
            # Confirma que a versão antiga foi removida do GitHub.
            print("Versão de lançamento anterior deletada com sucesso.")
            
    # Envia uma requisição de criação (POST) na API do GitHub com o payload contendo as notas da nova versão.
    resp = requests.post(release_url, headers=headers, json=release_payload)
    # Se a resposta do servidor não retornar código de sucesso (200 ou 201).
    if resp.status_code not in [200, 201]:
        # Exibe mensagens de falha e encerra a execução.
        print(f"Erro ao criar a versão de lançamento (release): {resp.status_code}")
        print(resp.text)
        sys.exit(1)
        
    # Decodifica a resposta em formato JSON contendo os dados da nova versão criada no GitHub.
    release_info = resp.json()
    # Obtém o endereço de rede para envio de arquivos anexos (ativos/assets) associado a este lançamento.
    upload_url_tmpl = release_info["upload_url"]
    # Limpa a rota de rede removendo parâmetros extras.
    upload_url = upload_url_tmpl.split("{")[0]
    # Confirma que o lançamento de versão foi gerado e exibe o identificador ID numérico atribuído pelo GitHub.
    print(f"Nova versão de lançamento (Release) criada com sucesso! Identificador ID: {release_info['id']}")
    
    # 4. ETAPA DE ENVIO (UPLOAD) DOS ARQUIVOS ANEXOS (RECURSOS) DO LANÇAMENTO
    # Varre a lista com os dois arquivos de anexo que serão enviados para a versão de lançamento: o pacote compactado zip e o versionador json.
    for asset_name, mime_type in [("GeoKit.zip", "application/zip"), ("version.json", "application/json")]:
        # Imprime o andamento do envio do anexo.
        print(f"Enviando anexo de recurso '{asset_name}' para o servidor...")
        # Abre o arquivo de anexo correspondente para leitura binária ('rb').
        with open(asset_name, "rb") as asset_file:
            # Lê todo o conteúdo binário do arquivo para a memória RAM.
            asset_data = asset_file.read()
            
        # Constrói o link de envio de arquivo (upload) para o anexo nos servidores do GitHub.
        asset_upload_url = f"{upload_url}?name={asset_name}"
        # Copia as credenciais de autenticação definindo o tipo e o tamanho exato dos dados binários que serão transmitidos.
        upload_headers = headers.copy()
        upload_headers["Content-Type"] = mime_type
        upload_headers["Content-Length"] = str(len(asset_data))
        
        # Envia a requisição de transmissão dos dados binários para o servidor do GitHub.
        up_resp = requests.post(asset_upload_url, headers=upload_headers, data=asset_data)
        # Se a transmissão retornou sucesso (códigos 200, 201 ou 202).
        if up_resp.status_code in [200, 201, 202]:
            # Confirma que o anexo foi enviado e associado ao lançamento.
            print(f"Anexo de recurso '{asset_name}' enviado com sucesso!")
        # Se ocorreu falha de transmissão do anexo.
        else:
            # Exibe mensagem de erro e aborta.
            print(f"Erro ao enviar anexo de recurso '{asset_name}': {up_resp.status_code}")
            print(up_resp.text)
            sys.exit(1)

    # Imprime no terminal a mensagem final informando a conclusão de todas as rotinas de lançamento de versão.
    print("Processo de Lançamento de Versão (Release) finalizado com total sucesso!")

# Verifica se o script make_release.py está rodando diretamente.
if __name__ == "__main__":
    # Inicia a execução da rotina principal de release.
    main()
