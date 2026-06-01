# A linha abaixo importa o módulo 'os' para manipulação de arquivos, diretórios e caminhos do sistema operacional Windows.
import os

# A linha abaixo importa o módulo 'sys' para acessar recursos do sistema, como o fechamento imediato do aplicativo.
import sys

# A linha abaixo importa o módulo 'time' que permite fazer o programa esperar (dormir) por alguns segundos.
import time

# A linha abaixo importa o módulo 'webbrowser' que serve para abrir links da internet no navegador padrão do usuário.
import webbrowser

# A linha abaixo importa a biblioteca 'customtkinter' sob o apelido 'ctk' para construir interfaces visuais modernas.
import customtkinter as ctk

# A linha abaixo importa a caixa de mensagens ('messagebox') clássica para exibir caixas de erro, aviso e confirmações na tela.
from tkinter import messagebox

# A linha abaixo importa a variável '__version__' que armazena a versão atual do GeoKit diretamente do pacote principal.
from geokit import __version__

# A linha abaixo importa a função do arquivo 'updater.py' encarregada de verificar se há atualizações do programa na internet.
from geokit.updater import check_for_updates

# A linha abaixo importa a classe que desenha o módulo SinaFlor (conversor de planilhas de coordenadas).
from geokit.modules.sinaflor import FrameSinaFlor

# A linha abaixo importa a classe que desenha o módulo Fepam (reprojetor de arquivos geográficos).
from geokit.modules.fepam import FrameFepam

# A linha abaixo importa a classe que desenha o módulo Fotos (conversor de fotos com GPS em mapas KMZ).
from geokit.modules.fotos import FrameFotosKMZ

# A linha abaixo define uma nova classe chamada 'UpdateProgressWindow' (Janela de Progresso de Atualização).
# Esta classe herda de 'ctk.CTkToplevel', o que significa que ela é uma janela secundária (pop-up) que abre acima da principal.
class UpdateProgressWindow(ctk.CTkToplevel):
    # A linha abaixo define o método construtor '__init__' (inicializador da janela) que recebe a janela mãe ('parent') e a rota de rede para download ('download_url').
    def __init__(self, parent, download_url):
        # A linha abaixo inicializa a classe pai 'CTkToplevel' associando esta janela pop-up flutuante à janela mãe 'parent'.
        super().__init__(parent)
        # A linha abaixo define o título que aparece na borda superior da janela de atualização.
        self.title("Atualizando GeoKit")
        # A linha abaixo define o tamanho físico da janela em pixels (420 de largura por 200 de altura).
        self.geometry("420x200")
        # A linha abaixo impede que o usuário altere o tamanho da janela arrastando as bordas (largura=Falso, altura=Falso).
        self.resizable(False, False)
        # A linha abaixo faz com que esta janela fique sempre flutuando acima da janela principal do programa.
        self.transient(parent)
        
        # A linha abaixo faz com que esta janela bloqueie as interações com a janela principal (comportamento modal) até que ela seja fechada.
        self.grab_set()
        
        # As linhas abaixo atualizam e calculam a posição geométrica para centralizar de forma exata a janela pop-up no centro da janela principal.
        parent.update_idletasks()
        # Calcula a posição horizontal (eixo X) central baseando-se no tamanho da janela mãe.
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 210
        # Calcula a posição vertical (eixo Y) central baseando-se no tamanho da janela mãe.
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 100
        # Define o tamanho físico da janela e a posiciona nos pontos X e Y calculados acima.
        self.geometry(f"420x200+{x}+{y}")
        
        # As linhas abaixo criam um rótulo de texto explicativo (Label) para mostrar o estado atual de carregamento da atualização.
        self.label_status = ctk.CTkLabel(
            self, 
            text="Preparando download...", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        # A linha abaixo desenha e posiciona o texto explicativo na janela com um espaçamento vertical (pady).
        self.label_status.pack(pady=(25, 10))
        
        # A linha abaixo cria um componente gráfico de Barra de Progresso ('CTkProgressBar') com largura de 340 pixels.
        self.progress_bar = ctk.CTkProgressBar(self, width=340)
        # A linha abaixo zera o preenchimento da barra de progresso (0% concluído).
        self.progress_bar.set(0.0)
        # A linha abaixo desenha e posiciona a barra de progresso na tela do pop-up.
        self.progress_bar.pack(pady=10)
        
        # A linha abaixo cria uma legenda para exibir o progresso em porcentagem e os Megabytes (MB) baixados da internet.
        self.label_percent = ctk.CTkLabel(self, text="0% (0.0 MB / 0.0 MB)", text_color="gray")
        # A linha abaixo posiciona a legenda textualmente abaixo da barra de progresso.
        self.label_percent.pack(pady=5)
        
        # As linhas abaixo importam a função responsável pelo download e instalação de dentro do módulo 'updater.py'.
        from geokit.updater import download_and_install_update
        # A linha abaixo inicia o download do arquivo de nova versão de maneira assíncrona (em segundo plano sem travar a interface do aplicativo), passando a rota e as funções de tratamento.
        download_and_install_update(
            download_url,
            self.on_progress,
            self.on_complete,
            self.on_error
        )
        
    # A linha abaixo define a função que recebe informações de progresso do download e agenda a atualização visual na tela.
    def on_progress(self, percent, downloaded_mb, total_mb):
        # A linha abaixo solicita ao CustomTkinter para atualizar a interface visual ('_update_ui') com segurança na linha principal de processamento (thread principal).
        self.after(0, lambda: self._update_ui(percent, downloaded_mb, total_mb))
        
    # A linha abaixo define o método que atualiza os elementos visuais na janela com os dados reais do download.
    def _update_ui(self, percent, downloaded_mb, total_mb):
        # Verifica se o download é de tamanho desconhecido/indeterminado (retorno igual a -1).
        if percent == -1:
            # Altera o texto de status informando que está baixando arquivos.
            self.label_status.configure(text="Baixando atualização...")
            # Atualiza o texto exibindo o total parcial de Megabytes baixados.
            self.label_percent.configure(text=f"{downloaded_mb:.1f} MB baixados")
            # Define o comportamento da barra de progresso como indeterminado (uma barra que vai e volta).
            self.progress_bar.configure(mode="indeterminate")
            # Inicia o movimento contínuo da barra indeterminada na tela.
            self.progress_bar.start()
        # Caso o tamanho total do download seja conhecido.
        else:
            # Altera o texto de status informando o download.
            self.label_status.configure(text="Baixando arquivos da nova versão...")
            # Preenche visualmente a barra de progresso com a porcentagem correspondente (entre 0.0 e 1.0).
            self.progress_bar.set(percent)
            # Atualiza o texto informando a porcentagem exata e a relação de Megabytes baixados contra o tamanho total.
            self.label_percent.configure(text=f"{int(percent * 100)}% ({downloaded_mb:.1f} MB / {total_mb:.1f} MB)")
            
    # A linha abaixo define o método acionado de forma automática quando o download do arquivo comprimido ZIP de atualização termina.
    def on_complete(self):
        # Agenda a execução do procedimento interno de finalização ('_finalize') para ser disparado na tela principal.
        self.after(0, self._finalize)
        
    # A linha abaixo define a rotina que fecha o programa para permitir a instalação definitiva da nova versão.
    def _finalize(self):
        # Atualiza a interface avisando ao usuário que o download terminou e a instalação foi iniciada.
        self.label_status.configure(text="Download concluído! Instalando...", text_color="green")
        # Força a atualização gráfica dos elementos da tela para que o texto acima seja renderizado.
        self.update_idletasks()
        # Faz o programa pausar por 1 segundo na tela antes de rodar o instalador externo.
        time.sleep(1.0)
        # Destrói e fecha a janela pop-up de atualização.
        self.destroy()
        # Encerra o programa atual por completo para que os arquivos antigos possam ser substituídos.
        sys.exit(0)
        
    # A linha abaixo define o método que é chamado quando ocorre algum erro de rede ou de disco durante o download.
    def on_error(self, err_msg):
        # Agenda a exibição do erro na tela principal do CustomTkinter de forma segura.
        self.after(0, lambda: self._show_error(err_msg))
        
    # A linha abaixo define o método que de fato exibe a caixa de aviso informando que o download falhou.
    def _show_error(self, err_msg):
        # Abre uma caixa de aviso clássica informando o erro técnico detalhado.
        messagebox.showerror(
            "Erro na Atualização", 
            f"Não foi possível baixar ou instalar a atualização:\n\n{err_msg}"
        )
        # Fecha a janela secundária de progresso, retornando o controle do aplicativo para a janela principal.
        self.destroy()


# A linha abaixo define a classe principal do aplicativo, chamada 'GeoKitApp'.
# Ela herda de 'ctk.CTk', representando a janela principal do programa.
class GeoKitApp(ctk.CTk):
    # A linha abaixo define o construtor da janela principal.
    def __init__(self):
        # Inicializa a classe base 'CTk' para que a janela seja criada pelo sistema operacional.
        super().__init__()

        # A linha abaixo define o título visível na barra superior da janela principal do GeoKit.
        self.title(f"GeoKit v{__version__} - Caixa de Ferramentas Geográficas")
        # A linha abaixo define a largura e altura iniciais da janela do aplicativo (1000 por 720 pixels).
        self.geometry("1000x720")
        # A linha abaixo estipula a dimensão mínima que a janela pode ter (950 por 680 pixels), impedindo que fique pequena demais.
        self.minsize(950, 680)

        # As linhas abaixo definem a estrutura da janela principal usando o sistema de posicionamento em grelha (Grid).
        # Configura a linha única (linha 0) para expandir e ocupar todo o espaço vertical disponível (atribuindo peso de expansão igual a 1).
        self.grid_rowconfigure(0, weight=1)
        # Configura a segunda coluna (coluna 1) para ocupar todo o espaço horizontal livre (onde estarão as ferramentas).
        self.grid_columnconfigure(1, weight=1)

        # ---------------- MENU LATERAL ----------------
        # A linha abaixo cria a barra/painel lateral esquerdo (Frame organizador de layout) que conterá os botões de navegação.
        self.frame_menu = ctk.CTkFrame(self, width=240, corner_radius=0)
        # Posiciona o painel lateral na coluna 0, linha 0, esticando vertical e horizontalmente ("nsew").
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        # Configura a linha 6 do menu lateral para expandir verticalmente, empurrando os elementos abaixo dela para o rodapé.
        self.frame_menu.grid_rowconfigure(6, weight=1) 

        # A linha abaixo cria o texto do logotipo principal "GeoKit" na parte superior da barra lateral.
        self.logo_label = ctk.CTkLabel(
            self.frame_menu, 
            text="GeoKit", 
            font=ctk.CTkFont(size=26, weight="bold", family="Outfit")
        )
        # Posiciona o logotipo principal na primeira linha da barra lateral com espaçamento interno (padding).
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        # A linha abaixo cria o texto secundário abaixo do logotipo "Ferramentas Geográficas".
        self.sub_logo_label = ctk.CTkLabel(
            self.frame_menu, 
            text="Ferramentas Geográficas", 
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        # Posiciona o texto secundário na segunda linha da barra lateral.
        self.sub_logo_label.grid(row=1, column=0, padx=20, pady=(0, 25))

        # A linha abaixo cria o botão para ativar o módulo SinaFlor (Conversor de coordenadas).
        self.btn_sinaflor = ctk.CTkButton(
            self.frame_menu, 
            text="🌲  SinaFlor (DMS)", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_sinaflor
        )
        # Posiciona o botão do SinaFlor na terceira linha da barra lateral, esticando-o de ponta a ponta.
        self.btn_sinaflor.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        # A linha abaixo cria o botão para abrir o módulo da Norma FEPAM (Padronizador de projeções).
        self.btn_fepam = ctk.CTkButton(
            self.frame_menu, 
            text="📋  Norma FEPAM (CRS)", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_fepam
        )
        # Posiciona o botão do Fepam na quarta linha da barra lateral.
        self.btn_fepam.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        # A linha abaixo cria o botão para carregar o módulo Fotos para KMZ.
        self.btn_fotos = ctk.CTkButton(
            self.frame_menu, 
            text="📸  Fotos -> KMZ", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_fotos
        )
        # Posiciona o botão de fotos na quinta linha da barra lateral.
        self.btn_fotos.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        # A linha abaixo cria a legenda de texto explicativo sobre o seletor de aparência do sistema.
        self.theme_label = ctk.CTkLabel(
            self.frame_menu, 
            text="Aparência do Sistema:", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        )
        # Posiciona a legenda da aparência na oitava linha (row 7) do painel lateral.
        self.theme_label.grid(row=7, column=0, padx=20, pady=(10, 2), sticky="w")
        
        # A linha abaixo cria o menu de seleção com as opções de temas ("Sistema", "Claro", "Escuro").
        self.theme_menu = ctk.CTkOptionMenu(
            self.frame_menu, 
            values=["Sistema", "Claro", "Escuro"],
            command=self.alterar_tema,
            height=28
        )
        # Posiciona o menu de temas na nona linha (row 8) do painel lateral.
        self.theme_menu.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")
        # Define "Sistema" como o tema padrão selecionado inicialmente no menu.
        self.theme_menu.set("Sistema")

        # A linha abaixo cria o rótulo de créditos informando os dados do criador do software GeoKit.
        self.lbl_creditos = ctk.CTkLabel(
            self.frame_menu, 
            text="Desenvolvido por:\nMatheus Rangel\n(51) 99790-3841", 
            font=ctk.CTkFont(size=11, slant="italic"), 
            text_color="gray"
        )
        # Posiciona o texto de créditos na décima linha (row 9) alinhado ao rodapé ("s" de sul).
        self.lbl_creditos.grid(row=9, column=0, padx=20, pady=(10, 25), sticky="s")

        # ---------------- ÁREAS DE CONTEÚDO ----------------
        # A linha abaixo cria um painel de contêiner transparente do lado direito da tela para exibir as ferramentas.
        self.frame_container = ctk.CTkFrame(self, fg_color="transparent")
        # Posiciona o contêiner na coluna 1, linha 0, com margens externas (padx e pady) de 25 pixels.
        self.frame_container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        # Configura as linhas e colunas internas do contêiner para expandirem e preencherem toda a tela disponível.
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        # As linhas abaixo instanciam e criam fisicamente as telas de cada um dos três módulos do GeoKit na memória.
        self.frame_sinaflor_view = FrameSinaFlor(self.frame_container)
        self.frame_fepam_view = FrameFepam(self.frame_container)
        self.frame_fotos_view = FrameFotosKMZ(self.frame_container)

        # A linha abaixo inicia o programa exibindo a tela do módulo SinaFlor por padrão ao carregar.
        self.mostrar_sinaflor()

        # A linha abaixo agenda a execução da função de verificar atualizações após 2 segundos (2000 milissegundos) da abertura do programa.
        self.after(2000, self.verificar_atualizacoes)

    # --- LÓGICA DE NAVEGAÇÃO ---
    # A linha abaixo define o método que esconde todas as telas de ferramentas e reseta as cores dos botões para o padrão inativo.
    def esconder_tudo(self):
        # Remove temporariamente a renderização gráfica dos três painéis de ferramentas da janela.
        self.frame_sinaflor_view.grid_forget()
        self.frame_fepam_view.grid_forget()
        self.frame_fotos_view.grid_forget()
        
        # Reseta os três botões de navegação para a cor transparente e texto adaptável (claro/escuro).
        self.btn_sinaflor.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])
        self.btn_fepam.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])
        self.btn_fotos.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])

    # A linha abaixo define o método para destacar visualmente o botão da ferramenta que estiver selecionada e ativa no momento.
    def destacar_botao(self, botao):
        # Configura o botão ativo com a cor azul de destaque do tema do CustomTkinter e texto na cor branca.
        botao.configure(fg_color=["#3a7ebf", "#1f538d"], text_color="#ffffff")

    # A linha abaixo define o método que exibe na tela o módulo do SinaFlor.
    def mostrar_sinaflor(self):
        # Oculta todas as telas ativas na interface.
        self.esconder_tudo()
        # Desenha a tela do SinaFlor no painel de contêiner.
        self.frame_sinaflor_view.grid(row=0, column=0, sticky="nsew")
        # Destaca visualmente o botão do SinaFlor na barra lateral esquerda.
        self.destacar_botao(self.btn_sinaflor)

    # A linha abaixo define o método que exibe na tela o módulo da Norma FEPAM.
    def mostrar_fepam(self):
        # Oculta todas as telas ativas na interface.
        self.esconder_tudo()
        # Desenha a tela do Fepam no painel de contêiner.
        self.frame_fepam_view.grid(row=0, column=0, sticky="nsew")
        # Destaca visualmente o botão da Fepam na barra lateral esquerda.
        self.destacar_botao(self.btn_fepam)

    # A linha abaixo define o método que exibe na tela o módulo de Conversão de Fotos.
    def mostrar_fotos(self):
        # Oculta todas as telas ativas na interface.
        self.esconder_tudo()
        # Desenha a tela de conversão de fotos no painel de contêiner.
        self.frame_fotos_view.grid(row=0, column=0, sticky="nsew")
        # Destaca visualmente o botão de Fotos na barra lateral esquerda.
        self.destacar_botao(self.btn_fotos)

    # A linha abaixo define o método para mudar o tema de cores do aplicativo baseado no menu de seleção.
    def alterar_tema(self, tema_selecionado):
        # Se a opção escolhida for "Claro", ajusta o aplicativo para o modo claro.
        if tema_selecionado == "Claro":
            ctk.set_appearance_mode("Light")
        # Se for "Escuro", ajusta o aplicativo para o modo escuro.
        elif tema_selecionado == "Escuro":
            ctk.set_appearance_mode("Dark")
        # Caso contrário, ajusta para acompanhar automaticamente o tema do sistema operacional.
        else:
            ctk.set_appearance_mode("System")

    # --- ATUALIZADOR ASSÍNCRONO ---
    # A linha abaixo define o método que chama o processo em segundo plano para checar por novas atualizações.
    def verificar_atualizacoes(self):
        # Dispara a busca informando a versão instalada e o método que deve ser executado ao encontrar novidades ('on_update_found').
        check_for_updates(__version__, self.on_update_found)

    # A linha abaixo define o método disparado quando o atualizador encontra uma nova versão do GeoKit no GitHub.
    def on_update_found(self, remote_version, url, notes):
        # Agenda a exibição do pop-up de atualização de forma segura na thread principal de interface gráfica.
        self.after(0, lambda: self.exibir_popup_atualizacao(remote_version, url, notes))

    # A linha abaixo define a rotina que pergunta ao usuário se ele gostaria de atualizar o programa automaticamente.
    def exibir_popup_atualizacao(self, remote_version, url, notes):
        # Monta o texto de notificação contendo o número da nova versão identificada.
        mensagem = f"Uma nova versão ({remote_version}) do GeoKit está disponível!\n"
        # Adiciona ao texto as notas de atualização caso existam detalhes informados pelo desenvolvedor.
        if notes:
            mensagem += f"\nNotas de atualização:\n{notes}\n"
        # Adiciona a pergunta de confirmação final.
        mensagem += "\nDeseja baixar e instalar esta nova versão de forma automática?"
        
        # Exibe uma caixa de diálogo na tela com as opções de Sim e Não ('askyesno').
        resposta = messagebox.askyesno("Atualização Disponível", mensagem, icon="info")
        # Se a resposta do usuário for Sim (resposta verdadeira).
        if resposta:
            # Cria a janela de progresso ('UpdateProgressWindow') iniciando o download e instalação da atualização.
            UpdateProgressWindow(self, url)
