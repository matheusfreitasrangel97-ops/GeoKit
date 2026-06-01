# A linha abaixo importa o módulo 'os' para manipulação de arquivos e pastas no sistema operacional.
import os

# A linha abaixo importa o módulo 'sys' para interagir com o ambiente e o interpretador Python ativo.
import sys

# A linha abaixo importa o módulo 'subprocess' para executar comandos do sistema operacional (como instalar pacotes com o pip).
import subprocess

# A linha abaixo define a função que fará a compilação do GeoKit.
def run_build():
    """
    Executa o empacotamento do GeoKit com a ferramenta PyInstaller.
    Compila o projeto em um único arquivo executável independente (.exe compilado de funcionamento autônomo)
    incluindo todas as dependências internas de código e recursos da biblioteca visual CustomTkinter.
    """
    # Imprime no terminal a mensagem de início do processo de compilação.
    print("Iniciando a compilação do GeoKit...")
    
    # Abre um bloco de captura de erros para tentar importar a ferramenta de compilação PyInstaller.
    try:
        # Tenta importar o módulo PyInstaller instalado no ambiente Python.
        import PyInstaller
    # Se o PyInstaller não estiver instalado no computador (gerando erro de importação).
    except ImportError:
        # Exibe mensagem avisando que instalará o PyInstaller automaticamente.
        print("A ferramenta PyInstaller não está instalada no ambiente Python. Instalando biblioteca de compilação necessária...")
        # Executa o comando do instalador (pip) de forma silenciosa para instalar o PyInstaller.
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Importa o módulo inicial de execução por linha de comando do PyInstaller.
    import PyInstaller.__main__

    # As linhas abaixo criam uma lista de argumentos/parâmetros para configurar a compilação:
    # - 'GeoKit.spec': Indica o arquivo de especificação que contém todas as regras de compilação e imports do projeto.
    # - '--clean': Limpa arquivos e pastas temporárias de compilações anteriores antes de começar.
    args = [
        'GeoKit.spec',
        '--clean'
    ]

    # Imprime no terminal a mensagem com os parâmetros configurados de compilação.
    print(f"Executando comando do PyInstaller com argumentos: {args}")
    # Chama o compilador PyInstaller passando a lista de argumentos. Ele gerará o arquivo .exe com base nas especificações do GeoKit.spec.
    PyInstaller.__main__.run(args)
    # Imprime mensagem avisando a conclusão do processo.
    print("Compilação finalizada! O executável final estará disponível na pasta 'dist/'.")

# Verifica se o arquivo build_spec.py está sendo executado diretamente.
if __name__ == "__main__":
    # Chama a função run_build para iniciar a compilação do executável.
    run_build()
