# A linha abaixo importa o módulo 'sys' da biblioteca padrão do Python. 
# Esse módulo nos dá acesso a recursos do sistema operacional e funções do interpretador Python.
import sys

# A linha abaixo importa a biblioteca 'customtkinter' e dá a ela o apelido 'ctk'.
# Esta biblioteca é usada para criar a interface gráfica moderna (janelas, botões, etc.) do nosso aplicativo.
import customtkinter as ctk

# A linha abaixo importa a classe 'GeoKitApp' de dentro da pasta (pacote) 'geokit', arquivo 'app.py'.
# É esta classe que contém o desenho principal da tela e a lógica da nossa janela principal.
from geokit.app import GeoKitApp

# A linha abaixo configura o modo de aparência padrão do CustomTkinter para 'System'.
# Isso faz com que o aplicativo siga automaticamente o tema claro ou escuro configurado no seu sistema operacional (Windows).
ctk.set_appearance_mode("System")

# A linha abaixo define o tema de cores padrão do aplicativo como 'blue' (azul).
# Isso significa que os botões e outros elementos destacados terão tons de azul por padrão.
ctk.set_default_color_theme("blue")

# A linha abaixo inicia a definição da nossa função principal, chamada 'main'.
# Esta função serve como ponto de partida da execução do programa.
def main():
    # A linha abaixo abre uma estrutura de tratamento de erros 'try' (bloco de tentativa). Todo o código aqui dentro será testado pelo interpretador.
    # Se algum problema ou falha técnica ocorrer nesta área, o fluxo irá direto para a seção de captura de erro 'except' no final deste bloco.
    try:
        # A linha abaixo cria um objeto (uma instância) chamado 'app' a partir da classe 'GeoKitApp'.
        # Isso efetivamente carrega a janela principal do aplicativo na memória.
        app = GeoKitApp()
        # A linha abaixo chama a função 'mainloop' (laço principal de execução e eventos da interface gráfica) da nossa janela.
        # Isso ativa a renderização gráfica do aplicativo de forma contínua na tela, aguardando interações de cliques de mouse ou toques de teclado.
        app.mainloop()
    # A linha abaixo captura qualquer erro (exceção) que ocorra dentro do bloco 'try' e o guarda na variável 'e'.
    except Exception as e:
        # Se ocorrer uma falha ao iniciar a janela moderna do CustomTkinter, inicia um novo bloco 'try' interno.
        # Este segundo bloco tentará exibir uma mensagem de erro mais simples utilizando a interface gráfica básica padrão do Python.
        try:
            # A linha abaixo importa a biblioteca básica de interfaces gráficas do Python chamada 'tkinter' como 'tk'.
            import tkinter as tk
            # A linha abaixo importa o componente 'messagebox' do tkinter, que é responsável por mostrar caixinhas de alerta na tela.
            from tkinter import messagebox
            # A linha abaixo inicializa a janela básica escondida do tkinter necessária para podermos exibir a caixa de erro.
            root = tk.Tk()
            # A linha abaixo oculta a janela básica secundária que foi criada temporariamente na memória, deixando apenas o popup de erro visível.
            root.withdraw()
            # A linha abaixo exibe uma janela de alerta pop-up de erro (caixa de diálogo exclusiva de aviso) com o título "Erro de Inicialização".
            # Ela explica de forma clara ao usuário qual foi o erro técnico contido na variável 'e'.
            messagebox.showerror(
                "Erro de Inicialização", 
                f"Ocorreu um erro fatal ao iniciar o GeoKit:\n\n{str(e)}\n\n"
                "Verifique se o seu ambiente Python possui suporte a interfaces gráficas (Tcl/Tk)."
            )
        # Se mesmo a exibição do erro simples falhar (por exemplo, se o computador não tiver suporte algum a telas), executa este bloco.
        except Exception:
            # Imprime o erro técnico de forma simples no canal de erros padrão da linha de comando (terminal do sistema).
            print(f"Erro fatal ao iniciar GeoKit: {e}", file=sys.stderr)
        # A linha abaixo encerra o programa por completo, retornando o código de erro 1 para o sistema operacional, indicando uma falha.
        sys.exit(1)

# A linha abaixo verifica se este arquivo está sendo executado diretamente pelo usuário.
# Em Python, se executarmos este arquivo diretamente (por exemplo, 'python main.py'), a variável especial '__name__' será igual a '__main__'.
if __name__ == "__main__":
    # Se for o caso, chama a função 'main()' que definimos acima para iniciar o aplicativo.
    main()
