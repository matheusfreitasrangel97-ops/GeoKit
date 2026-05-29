import os
import sys
import subprocess

def run_build():
    """
    Executa o empacotamento do GeoKit com PyInstaller.
    Compila o projeto em um único arquivo executável standalone (.exe)
    incluindo todas as dependências internas e recursos do CustomTkinter.
    """
    print("Iniciando build do GeoKit...")
    
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não está instalado no ambiente Python. Instalando dependência de build...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    import PyInstaller.__main__

    # Parâmetros de compilação do PyInstaller:
    # - --onefile: compacta tudo em um único arquivo .exe independente
    # - --noconsole: oculta a janela de terminal preta ao abrir a GUI
    # - --collect-all=customtkinter: inclui todos os assets, temas e subcomponentes do customtkinter
    # - --clean: limpa o cache do compilador antes de iniciar
    args = [
        'main.py',
        '--onefile',
        '--noconsole',
        '--collect-all=customtkinter',
        '--name=GeoKit',
        '--clean'
    ]

    print(f"Executando comando do PyInstaller com argumentos: {args}")
    PyInstaller.__main__.run(args)
    print("Compilação finalizada! O executável final estará disponível na pasta 'dist/'.")

if __name__ == "__main__":
    run_build()
