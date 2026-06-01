# A linha abaixo importa o módulo 'os' da biblioteca padrão, usado para criar diretórios, extrair nomes de arquivos e organizar rotas de pastas.
import os

# A linha abaixo importa a biblioteca 'geopandas' sob o apelido 'gpd'. Ela estende o pandas clássico permitindo carregar, processar e salvar dados de mapas (vetores geográficos).
import geopandas as gpd

# A linha abaixo importa a biblioteca 'customtkinter' sob o apelido 'ctk' para a construção do painel gráfico moderno.
import customtkinter as ctk

# A linha abaixo importa ferramentas de caixa de seleção de pastas ('filedialog') e alertas visuais ('messagebox') da biblioteca básica do Python.
from tkinter import filedialog, messagebox

# A linha abaixo inicia a definição da classe 'FrameFepam', herdando de 'ctk.CTkFrame' para atuar como uma tela secundária integrada.
class FrameFepam(ctk.CTkFrame):
    # A linha abaixo define o método construtor de inicialização do painel da Fepam.
    def __init__(self, master, **kwargs):
        # Inicializa o frame básico definindo a cor de fundo como transparente.
        super().__init__(master, fg_color="transparent", **kwargs)

        # A linha abaixo cria uma lista vazia chamada 'arquivos_para_processar'.
        # Ela guardará os caminhos absolutos dos arquivos de mapas digitais do tipo Shapefile (.shp) ou bancos de dados espaciais compactos Geopackage (.gpkg) selecionados no computador.
        self.arquivos_para_processar = []
        # A linha abaixo cria uma string vazia chamada 'caminho_saida' para armazenar a pasta destino onde os arquivos reprojetados serão gravados.
        self.caminho_saida = ""

        # As linhas abaixo criam o título do cabeçalho da ferramenta em destaque em negrito e tamanho 22.
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="Reprojetor SIRGAS 2000 - Norma FEPAM 07/2015", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        # Posiciona o título no topo da tela com margem vertical de espaçamento.
        self.lbl_titulo.pack(pady=(15, 10))

        # As linhas abaixo criam um texto de descrição didática informando o objetivo técnico de padronização da norma ambiental da FEPAM.
        self.lbl_desc = ctk.CTkLabel(
            self,
            text="Esta ferramenta padroniza arquivos geográficos (.shp, .gpkg) para o Sistema de Referência Geocêntrico para as Américas (SIRGAS 2000) no formato Geográfico (Graus Decimais, EPSG:4674), atendendo às especificações da FEPAM.",
            font=ctk.CTkFont(size=12),
            wraplength=700,
            text_color="gray"
        )
        # Posiciona o texto de descrição limitando a quebra automática de linha a 700 pixels (wraplength).
        self.lbl_desc.pack(pady=(0, 15))

        # A linha abaixo cria um painel (Frame) para agrupar as opções de seleção de arquivos.
        self.frame_entrada = ctk.CTkFrame(self)
        # Posiciona o painel de entrada esticando na horizontal com margens nas laterais de 40 pixels.
        self.frame_entrada.pack(pady=5, fill="x", padx=40)

        # As linhas abaixo criam o botão destacado em azul para selecionar múltiplos arquivos geográficos (.SHP ou .GPKG) no computador.
        self.btn_carregar = ctk.CTkButton(
            self.frame_entrada, 
            text="SELECIONAR ARQUIVOS (.SHP / .GPKG)", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            command=self.selecionar_multiplos_arquivos, 
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        # Posiciona o botão de carregamento preenchendo horizontalmente o painel com margens internas de 20 pixels.
        self.btn_carregar.pack(pady=12, padx=20, fill="x")

        # As linhas abaixo criam a legenda superior da caixa de texto do diagnóstico: "Relatório de Diagnóstico de CRS:".
        self.lbl_titulo_txt = ctk.CTkLabel(
            self, 
            text="Relatório de Diagnóstico de Sistema de Coordenadas (CRS):", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="gray"
        )
        # Posiciona a legenda à esquerda ("w" de west).
        self.lbl_titulo_txt.pack(anchor="w", padx=45, pady=(10, 2))

        # As linhas abaixo criam o componente de Caixa de Texto ('CTkTextbox') com altura de 160 pixels para mostrar os diagnósticos de projeção dos arquivos lidos.
        self.txt_relatorio = ctk.CTkTextbox(
            self, 
            height=160, 
            activate_scrollbars=True, 
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        # Posiciona a caixa de texto esticando-a na horizontal.
        self.txt_relatorio.pack(fill="x", padx=40, pady=2)
        # Insere uma mensagem de aviso inicial dentro da caixa de texto.
        self.txt_relatorio.insert("0.0", "Nenhum arquivo carregado para análise.")
        # Configura marcadores visuais (tags) para colorir textos específicos: erro em vermelho, conformidade em verde, alerta em laranja.
        self.txt_relatorio.tag_config("erro_vermelho", foreground="#E53935")
        self.txt_relatorio.tag_config("ok_verde", foreground="#2E7D32")
        self.txt_relatorio.tag_config("aviso_amarelo", foreground="#E65100")
        # Desativa a edição manual por digitação na caixa de texto, tornando-a somente leitura para o usuário.
        self.txt_relatorio.configure(state="disabled")

        # A linha abaixo cria o painel (Frame) para agrupar as opções de gravação de saída.
        self.frame_saida = ctk.CTkFrame(self)
        # Posiciona o painel de saída esticando-o na horizontal.
        self.frame_saida.pack(pady=15, fill="x", padx=40)

        # As linhas abaixo criam o botão para o usuário selecionar a pasta física do computador onde os arquivos corrigidos serão salvos.
        self.btn_destino = ctk.CTkButton(
            self.frame_saida, 
            text="Definir Pasta de Destino", 
            command=self.selecionar_destino
        )
        # Posiciona o botão de definição de pasta destino.
        self.btn_destino.pack(pady=10)

        # A linha abaixo cria uma legenda textual simples para exibir no painel qual a pasta destino atualmente definida.
        self.lbl_status_saida = ctk.CTkLabel(self, text="Nenhum destino definido.", text_color="gray")
        # Posiciona a legenda da pasta destino na tela.
        self.lbl_status_saida.pack(pady=3)

        # As linhas abaixo criam o botão principal "EXECUTAR REPROJEÇÃO PARA SIRGAS 2000" colorido em verde.
        self.btn_processar = ctk.CTkButton(
            self, 
            text="EXECUTAR REPROJEÇÃO PARA SIRGAS 2000", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            command=self.processar_dados, 
            height=45
        )
        # Posiciona o botão principal de execução no rodapé da janela do módulo.
        self.btn_processar.pack(pady=15, ipadx=20)

    # A linha abaixo define o método que abre o diálogo de seleção de múltiplos arquivos geográficos no disco.
    def selecionar_multiplos_arquivos(self):
        # Define os filtros de extensão de arquivos que o explorador aceitará.
        tipos = [
            ("Arquivos Geográficos", "*.shp *.gpkg"), 
            ("Shapefiles ESRI", "*.shp"), 
            ("GeoPackage", "*.gpkg")
        ]
        # Abre o explorador de arquivos retornando uma lista com as rotas dos arquivos escolhidos.
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos geográficos para análise", 
            filetypes=tipos
        )
        # Se o usuário cancelou a escolha e não selecionou nenhum arquivo.
        if not arquivos: 
            # Interrompe a execução do método.
            return

        # Guarda a lista de arquivos selecionados na nossa variável de controle.
        self.arquivos_para_processar = list(arquivos)
        # Ativa a edição temporária da caixa de texto do diagnóstico para atualizar seu conteúdo.
        self.txt_relatorio.configure(state="normal")
        # Limpa todos os textos antigos da caixa de texto do diagnóstico.
        self.txt_relatorio.delete("0.0", "end")
        # Insere uma linha de cabeçalho na caixa de texto indicando a quantidade total de arquivos abertos.
        self.txt_relatorio.insert(
            "end", 
            f"TOTAL DE ARQUIVOS CARREGADOS: {len(self.arquivos_para_processar)}\n{'-'*75}\n"
        )

        # Inicia um laço de repetição indexado (começando de 1) para fazer a leitura dos metadados de cada arquivo.
        for i, caminho in enumerate(self.arquivos_para_processar, 1):
            # Extrai apenas o nome final do arquivo de dados geográficos (ex: "fazenda.shp").
            nome_arq = os.path.basename(caminho)
            # Tenta ler os metadados do arquivo geográfico sem carregar todas as feições para a memória, otimizando o tempo de execução (rows=1).
            try:
                gdf_schema = gpd.read_file(caminho, rows=1)
                # Insere o índice e nome do arquivo no diagnóstico textual.
                self.txt_relatorio.insert("end", f"[{i}] Arquivo: {nome_arq}\n")
                
                # Se o arquivo lido não possuir nenhum Sistema de Referência de Coordenadas (CRS) definido (nulo).
                if gdf_schema.crs is None:
                    # Registra a ausência do Sistema de Referência de Coordenadas (CRS) no diagnóstico.
                    self.txt_relatorio.insert("end", "    Projeção atual: Sem CRS definido\n    Situação: ")
                    # Destaca em vermelho que o arquivo é incompatível devido à falta de projeção.
                    self.txt_relatorio.insert("end", "Incompatível (Sem Projeção - Requer definição manual)\n\n", "erro_vermelho")
                # Se o arquivo possuir projeção declarada.
                else:
                    # Tenta obter o código de número padrão internacional de identificação da projeção cartográfica (código EPSG).
                    epsg = gdf_schema.crs.to_epsg()
                    # Obtém o nome legível da projeção geográfica (exemplo: "SIRGAS 2000").
                    crs_name = gdf_schema.crs.name
                    
                    # Insere as informações de projeção no texto do diagnóstico.
                    self.txt_relatorio.insert("end", f"    Projeção atual: {crs_name} (EPSG:{epsg if epsg else 'Não identificado'})\n    Situação: ")
                    
                    # Se o código EPSG for igual a 4674 (que representa a projeção geográfica SIRGAS 2000, exigida pela FEPAM).
                    if epsg == 4674:
                        # Destaca o texto em verde indicando que o arquivo já atende aos requisitos normativos do órgão ambiental.
                        self.txt_relatorio.insert("end", "Em conformidade com a Norma 07/2015 FEPAM (SIRGAS 2000)\n\n", "ok_verde")
                    # Caso a projeção seja diferente da Norma 07/2015.
                    else:
                        # Destaca em laranja informando que ele é incompatível, mas será corrigido (reprojetado) pelo GeoKit.
                        self.txt_relatorio.insert("end", "Incompatível (Será reprojetado para SIRGAS 2000)\n\n", "aviso_amarelo")
            # Se ocorrer alguma falha técnica na tentativa de leitura do cabeçalho do arquivo geográfico (ex: arquivo shapefile incompleto).
            except Exception as e:
                # Escreve a mensagem de falha em vermelho na caixa de diagnóstico do aplicativo.
                self.txt_relatorio.insert(
                    "end", 
                    f"[{i}] Arquivo: {nome_arq}\n    Erro ao ler metadados: {str(e)}\n\n", 
                    "erro_vermelho"
                )

        # Desativa a digitação na caixa de texto do diagnóstico mantendo apenas a leitura.
        self.txt_relatorio.configure(state="disabled")

    # A linha abaixo define o método que abre a caixa de diálogo para escolher o diretório de gravação dos resultados.
    def selecionar_destino(self):
        # Abre o explorador de pastas do Windows retornando a rota da pasta escolhida.
        pasta = filedialog.askdirectory(title="Selecione a pasta onde salvar os arquivos corrigidos")
        # Se uma pasta foi selecionada pelo usuário.
        if pasta:
            # Armazena o caminho na nossa variável de controle.
            self.caminho_saida = pasta
            # Atualiza o texto da tela exibindo a pasta definida em azul.
            self.lbl_status_saida.configure(text=f"Pasta de Destino: {pasta}", text_color="#1f538d")

    # A linha abaixo define o método principal de processamento de reprojeção para SIRGAS 2000 (Norma FEPAM).
    def processar_dados(self):
        # Verifica se o usuário não selecionou nenhum arquivo geográfico ainda.
        if not self.arquivos_para_processar:
            # Mostra uma caixinha de aviso e encerra o processamento.
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo de entrada primeiro.")
            return
        # Verifica se o usuário não escolheu a pasta física de destino.
        if not self.caminho_saida:
            # Mostra uma caixinha de aviso e encerra.
            messagebox.showwarning("Aviso", "Defina a pasta de destino dos arquivos convertidos.")
            return

        # Inicializa contadores de progresso.
        reprojecoes = 0
        mantidos = 0
        erros = 0
        
        # Cria um caminho absoluto para uma nova pasta chamada "dados_sirgas2000" dentro do destino escolhido.
        pasta_final = os.path.join(self.caminho_saida, "dados_sirgas2000")
        # Cria fisicamente a pasta no Windows caso ela ainda não exista (exist_ok=True).
        os.makedirs(pasta_final, exist_ok=True)

        # Varre cada um dos caminhos de arquivos geográficos da nossa lista de entrada.
        for arquivo_path in self.arquivos_para_processar:
            # Extrai o nome do arquivo.
            nome_arq = os.path.basename(arquivo_path)
            # Tenta efetuar o carregamento completo do arquivo, sua reprojeção e gravação em disco.
            try:
                # Carrega o arquivo geográfico completo (tabela e geometrias espaciais) na memória com geopandas.
                gdf = gpd.read_file(arquivo_path)
                
                # Se o arquivo não possuir projeção nativa definida (CRS nulo).
                if gdf.crs is None:
                    # Ativa a caixa de texto de relatório de diagnóstico para escrever.
                    self.txt_relatorio.configure(state="normal")
                    # Registra a mensagem de falha em vermelho na caixa de diagnóstico.
                    self.txt_relatorio.insert("end", f"⚠️ Falha no arquivo {nome_arq}: Não possui CRS definido para reprojeção.\n", "erro_vermelho")
                    # Bloqueia a edição da caixa de diagnóstico.
                    self.txt_relatorio.configure(state="disabled")
                    # Soma 1 unidade ao contador de erros de processamento.
                    erros += 1
                    # Pula imediatamente para o próximo arquivo da lista.
                    continue

                # Extrai a extensão do arquivo (ex: ".shp" ou ".gpkg") e o nome principal puro sem extensão.
                ext = os.path.splitext(nome_arq)[1]
                nome_base = os.path.splitext(nome_arq)[0]
                # Gera o nome do novo arquivo de saída adicionando o prefixo "sirgas_" no início.
                novo_nome = f"sirgas_{nome_base}{ext}"
                # Define a rota absoluta final de onde o novo arquivo corrigido será gravado.
                caminho_final = os.path.join(pasta_final, novo_nome)

                # Obtém o código EPSG identificador do sistema de projeção do arquivo lido.
                epsg_code = gdf.crs.to_epsg()
                
                # Se o arquivo já estiver na projeção correta de conformidade EPSG:4674 (SIRGAS 2000 Geográfico).
                if epsg_code == 4674:
                    # Apenas salva uma cópia limpa do arquivo original na pasta de destino final.
                    gdf.to_file(caminho_final)
                    # Soma 1 unidade ao contador de arquivos que já estavam conformes e foram mantidos.
                    mantidos += 1
                # Caso a projeção seja diferente (por exemplo, WGS84 ou sistema projetado UTM).
                else:
                    # Converte de forma matemática todas as geometrias do arquivo para o código EPSG:4674 (SIRGAS 2000).
                    gdf_sirgas = gdf.to_crs(epsg=4674)
                    # Grava o novo arquivo resultante reprojetado de forma definitiva na pasta de destino final.
                    gdf_sirgas.to_file(caminho_final)
                    # Soma 1 unidade ao contador de arquivos que foram reprojetados pelo sistema.
                    reprojecoes += 1
                    
            # Se ocorrer qualquer falha no meio do processo de conversão ou gravação de arquivos no computador.
            except Exception as e:
                # Exibe caixinha de aviso indicando o erro específico.
                messagebox.showerror("Erro", f"Falha ao processar o arquivo {nome_arq}:\n{str(e)}")
                # Incrementa o número de arquivos com falha de processamento.
                erros += 1
                # Continua executando para os outros arquivos na fila.
                continue

        # Monta a mensagem final sintetizada resumindo os resultados de todo o processo de reprojeção.
        mensagem = f"Processamento concluído com sucesso!\n\nSalvos em: {pasta_final}\n"
        mensagem += f"• Arquivos reprojetados para SIRGAS 2000 (EPSG:4674): {reprojecoes}\n"
        mensagem += f"• Arquivos copiados (já estavam em conformidade): {mantidos}"
        # Se houveram erros de processamento em algum arquivo.
        if erros > 0:
            # Adiciona a contagem de falhas na mensagem.
            mensagem += f"\n• Arquivos com erro (não processados): {erros}"
            
        # Exibe uma caixa de diálogo clássica com o resumo total de sucesso do processamento.
        messagebox.showinfo("Sucesso", mensagem)
