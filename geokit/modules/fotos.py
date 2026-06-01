# A linha abaixo importa o módulo 'os' para gerenciar pastas, obter extensões e extrair caminhos de arquivos.
import os

# A linha abaixo importa a codificação base64 (não usada diretamente aqui, mas preservada para compatibilidade se necessário).
import base64

# A linha abaixo importa o módulo 'zipfile' para criar e compactar o arquivo de mapas digitais .kmz (que é um pacote comprimido em formato zip contendo o mapa e as fotos compactados).
import zipfile

# A linha abaixo importa a classe 'BytesIO' da biblioteca padrão, que permite ler e salvar dados na memória como se fossem arquivos físicos.
from io import BytesIO

# A linha abaixo importa a biblioteca 'customtkinter' sob o apelido 'ctk' para construir a interface visual moderna de botões e caixas de entrada.
import customtkinter as ctk

# A linha abaixo importa ferramentas de caixas de escolha de arquivos e pop-ups de aviso/erro da biblioteca clássica do Python.
from tkinter import filedialog, messagebox

# A linha abaixo importa a classe 'Image' sob o apelido 'ExifImage' da biblioteca 'exif'. Ela é responsável por ler os metadados técnicos (como coordenadas geográficas de GPS) embutidos nas propriedades invisíveis das fotos.
from exif import Image as ExifImage

# A linha abaixo importa as classes 'Image' e 'ImageOps' da biblioteca de processamento de imagens 'Pillow' (PIL). Usada para redimensionar e rotacionar fotos automaticamente.
from PIL import Image as PILImage, ImageOps

# A linha abaixo importa a biblioteca 'simplekml' para facilitar a construção estruturada do arquivo KML de mapa geográfico.
import simplekml

# A linha abaixo inicia a definição da classe 'FrameFotosKMZ' herdando de 'ctk.CTkFrame' para atuar como o painel principal do módulo de fotos.
class FrameFotosKMZ(ctk.CTkFrame):
    # A linha abaixo define o construtor da tela que receberá o contêiner pai ('master').
    def __init__(self, master, **kwargs):
        # Inicializa o frame básico definindo a cor de fundo como transparente.
        super().__init__(master, fg_color="transparent", **kwargs)

        # A linha abaixo inicializa uma lista vazia para armazenar as rotas físicas de todas as fotos JPG selecionadas.
        self.caminhos_fotos = []
        # A linha abaixo cria uma string vazia para guardar a rota de gravação escolhida para salvar o arquivo final .kmz.
        self.caminho_saida = ""

        # As linhas abaixo criam o título principal da tela "Conversor de Fotos com GPS para KMZ" em negrito com tamanho 22.
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="Conversor de Fotos com GPS para KMZ", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        # Desenha e posiciona o título com margem vertical de espaçamento.
        self.lbl_titulo.pack(pady=(15, 10))

        # As linhas abaixo criam o texto didático informando o objetivo do módulo aos usuários.
        self.lbl_desc = ctk.CTkLabel(
            self,
            text="Gere mapas interativos contendo fotos no local exato onde foram tiradas. O sistema lê os metadados de GPS das imagens e cria popups elegantes.",
            font=ctk.CTkFont(size=12),
            wraplength=700,
            text_color="gray"
        )
        # Posiciona a descrição na tela limitando a quebra de linha a 700 pixels.
        self.lbl_desc.pack(pady=(0, 15))

        # ---------------- FRAME DE ENTRADA (FOTOS ORIGEM) ----------------
        # A linha abaixo cria um painel (Frame) para agrupar as opções de seleção das fotos de origem.
        self.frame_entrada = ctk.CTkFrame(self)
        # Posiciona o painel de entrada com margem horizontal lateral.
        self.frame_entrada.pack(pady=10, padx=20, fill="x")

        # Rótulo informativo da entrada de fotos.
        self.lbl_entrada = ctk.CTkLabel(self.frame_entrada, text="Fotos de Origem:", font=ctk.CTkFont(size=12, weight="bold"))
        # Posiciona a legenda na linha 0, coluna 0 do painel de entrada à esquerda.
        self.lbl_entrada.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        # Caixa de texto de entrada de linha única para exibir a quantidade de arquivos carregados.
        self.txt_entrada = ctk.CTkEntry(self.frame_entrada, width=450, placeholder_text="Nenhum arquivo selecionado...")
        # Posiciona a caixa de texto na linha 1, coluna 0 esticando-a na horizontal.
        self.txt_entrada.grid(row=1, column=0, padx=10, pady=(0, 12), sticky="we")

        # Botão "Procurar Fotos..." para abrir o explorador de seleção de arquivos.
        self.btn_selecionar = ctk.CTkButton(
            self.frame_entrada, 
            text="Procurar Fotos...", 
            width=120, 
            command=self.selecionar_fotos
        )
        # Posiciona o botão de seleção ao lado da caixa de texto (coluna 1).
        self.btn_selecionar.grid(row=1, column=1, padx=10, pady=(0, 12))

        # ---------------- FRAME DE SAÍDA (SALVAR KMZ) ----------------
        # A linha abaixo cria um painel para as configurações de gravação de saída do arquivo KMZ.
        self.frame_saida = ctk.CTkFrame(self)
        # Posiciona o painel na tela.
        self.frame_saida.pack(pady=10, padx=20, fill="x")

        # Rótulo informativo da rota de saída.
        self.lbl_saida_tit = ctk.CTkLabel(self.frame_saida, text="Destino do Arquivo KMZ:", font=ctk.CTkFont(size=12, weight="bold"))
        # Posiciona a legenda na coluna 0, linha 0 à esquerda.
        self.lbl_saida_tit.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        # Caixa de texto de entrada para exibir onde o arquivo de mapa KMZ será gerado.
        self.txt_saida = ctk.CTkEntry(self.frame_saida, width=450, placeholder_text="Defina o local e nome para salvar o KMZ...")
        # Posiciona a caixa de texto esticando-a na horizontal.
        self.txt_saida.grid(row=1, column=0, padx=10, pady=(0, 12), sticky="we")

        # Botão "Definir Destino..." para escolher o local de salvamento.
        self.btn_saida = ctk.CTkButton(
            self.frame_saida, 
            text="Definir Destino...", 
            width=120, 
            command=self.definir_saida
        )
        # Posiciona o botão na coluna 1.
        self.btn_saida.grid(row=1, column=1, padx=10, pady=(0, 12))

        # ---------------- FRAME DE CONFIGURAÇÕES (TAMANHO DAS IMAGENS) ----------------
        # A linha abaixo cria um painel para agrupar as opções de redimensionamento e otimização de imagem.
        self.frame_config = ctk.CTkFrame(self)
        # Posiciona o painel de configurações na tela.
        self.frame_config.pack(pady=10, padx=20, fill="x")

        # Legenda das opções de otimização de imagem.
        self.lbl_opcao_tamanho = ctk.CTkLabel(self.frame_config, text="Dimensão / Qualidade das Fotos no Mapa:", font=ctk.CTkFont(size=12, weight="bold"))
        # Posiciona a legenda do lado esquerdo do painel.
        self.lbl_opcao_tamanho.pack(side="left", padx=15, pady=12)
        
        # Cria a caixa de seleção com as opções de qualidade e dimensões disponíveis.
        self.combo_tamanho = ctk.CTkComboBox(self.frame_config, width=280, values=[
            "Compacto (300px) - Arquivo leve", 
            "Médio (600px) - Recomendado", 
            "Grande (1200px) - Alta Definição", 
            "Original - Mantém resolução padrão"
        ])
        # Define a opção "Médio (600px) - Recomendado" como padrão ativo inicial.
        self.combo_tamanho.set("Médio (600px) - Recomendado")
        # Posiciona a caixa de seleção alinhada ao lado direito do painel.
        self.combo_tamanho.pack(side="right", padx=15, pady=12)

        # ---------------- BARRA DE PROGRESSO ----------------
        # A linha abaixo cria o painel transparente de barra de progresso.
        self.frame_progresso = ctk.CTkFrame(self, fg_color="transparent")
        # Posiciona o painel de progresso na tela.
        self.frame_progresso.pack(pady=10, padx=20, fill="x")

        # Texto informativo de andamento do processamento das imagens.
        self.lbl_status_processo = ctk.CTkLabel(
            self.frame_progresso, 
            text="Aguardando definições para iniciar...", 
            font=ctk.CTkFont(size=12, slant="italic"), 
            text_color="gray"
        )
        # Posiciona o texto de status.
        self.lbl_status_processo.pack(pady=2)

        # Cria visualmente a barra de progresso com largura horizontal de 540 pixels.
        self.progress_bar = ctk.CTkProgressBar(self.frame_progresso, width=540)
        # Define o estado inicial da barra como vazio (0%).
        self.progress_bar.set(0)
        # Posiciona a barra de progresso.
        self.progress_bar.pack(pady=5)

        # ---------------- BOTÃO GERAR ----------------
        # As linhas abaixo criam o botão destacado em verde para iniciar a geração do mapa KMZ definitivo.
        self.btn_gerar = ctk.CTkButton(
            self, 
            text="GERAR ARQUIVO KMZ", 
            command=self.validar_e_gerar, 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            height=48, 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        # Posiciona o botão principal de geração no rodapé.
        self.btn_gerar.pack(pady=15)

    # A linha abaixo define a função matemática para converter coordenadas EXIF de GPS (armazenadas em Graus, Minutos e Segundos) para Graus Decimais.
    def converter_para_decimal(self, coords, ref):
        """Converte coordenadas gravadas nas propriedades EXIF (Graus, Minutos, Segundos) da imagem para graus em formato decimal."""
        # Abre bloco de tratamento de erro para caso a leitura de coordenadas falhe.
        try:
            # Extrai os Graus da tupla.
            d = float(coords[0])
            # Extrai os Minutos.
            m = float(coords[1])
            # Extrai os Segundos.
            s = float(coords[2])
            # Efetua o cálculo de conversão clássico de DMS para Decimal.
            decimal = d + (m / 60.0) + (s / 3600.0)
            # Se a referência cardinal for Sul (S) ou Oeste (W), a coordenada deve ser representada como negativa.
            if ref in ['S', 'W']: 
                decimal = -decimal
            # Retorna o valor decimal resultante.
            return decimal
        # Se ocorrer algum erro na fórmula de cálculo (exemplo: dados de coordenada inválidos nas propriedades da imagem).
        except Exception:
            # Retorna o valor nulo (None) indicando ausência de dados válidos.
            return None

    # A linha abaixo define o método que abre o diálogo para escolher as fotos JPEG no disco rígido.
    def selecionar_fotos(self):
        # Abre o explorador aceitando arquivos de imagem com extensão JPG ou JPEG.
        arquivos = filedialog.askopenfilenames(
            title="Selecione as fotos (JPEG)", 
            filetypes=[("Imagens JPEG", "*.jpg *.jpeg"), ("Todos os Arquivos", "*.*")]
        )
        # Se o usuário escolheu uma ou mais fotos.
        if arquivos:
            # Converte a tupla de caminhos retornada para uma lista Python configurando a nossa variável.
            self.caminhos_fotos = list(arquivos)
            # Limpa qualquer texto antigo existente na caixa de entrada.
            self.txt_entrada.delete(0, "end")
            # Insere um resumo informando o total de fotos selecionadas e a pasta de origem.
            self.txt_entrada.insert(0, f"{len(self.caminhos_fotos)} fotos selecionadas em: {os.path.dirname(self.caminhos_fotos[0])}")
            # Atualiza o texto explicativo de status em azul.
            self.lbl_status_processo.configure(text=f"📂 {len(self.caminhos_fotos)} foto(s) carregada(s).", text_color="#1f538d")

    # A linha abaixo define o método que abre o diálogo para escolher onde o arquivo KMZ resultante deve ser salvo.
    def definir_saida(self):
        # Abre a janela de salvar arquivo configurando a extensão padrão como ".kmz".
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".kmz", 
            filetypes=[("Arquivo Google Earth KMZ", "*.kmz")],
            title="Salvar arquivo KMZ"
        )
        # Se o usuário confirmou a pasta e o nome do arquivo.
        if arquivo:
            # Armazena a rota de gravação na nossa variável de controle.
            self.caminho_saida = arquivo
            # Limpa qualquer texto antigo na caixa de texto correspondente.
            self.txt_saida.delete(0, "end")
            # Insere a rota de gravação definida na caixa de texto para visualização.
            self.txt_saida.insert(0, self.caminho_saida)

    # A linha abaixo define o método que verifica se os campos foram preenchidos antes de iniciar o processo de conversão.
    def validar_e_gerar(self):
        # Se o usuário não escolheu nenhuma foto.
        if not self.caminhos_fotos:
            # Exibe aviso alertando sobre a necessidade de escolher imagens.
            messagebox.showwarning("Atenção", "Selecione as fotos que deseja converter.")
            # Cancela a execução imediata.
            return
        # Se o usuário não definiu onde quer salvar o arquivo KMZ final.
        if not self.caminho_saida:
            # Exibe aviso indicando a necessidade de configurar a pasta final de gravação.
            messagebox.showwarning("Atenção", "Defina o destino do arquivo KMZ.")
            # Cancela.
            return
        # Se tudo estiver correto, inicia de fato o processamento definitivo.
        self.processar_conversao()

    # A linha abaixo define a lógica principal de processamento e criação do arquivo KMZ final.
    def processar_conversao(self):
        # Desativa temporariamente o botão de geração para impedir cliques múltiplos acidentais durante o carregamento.
        self.btn_gerar.configure(state="disabled")
        # Obtém o texto do tamanho de imagem selecionado na caixa de seleção pelo usuário.
        escolha = self.combo_tamanho.get()
        # Define o tamanho máximo de pixels (largura/altura) com base na escolha (300px compacta, 600px média, ou 1200px grande).
        tamanho_max = 300 if "Compacto" in escolha else 600 if "Médio" in escolha else 1200
        # Define a largura ideal para a janela pop-up flutuante de exibição estruturada em HTML dentro do mapa correspondente ao tamanho.
        largura_balao = 350 if "Compacto" in escolha else 600 if "Médio" in escolha else 750
        # Define como Verdadeiro se a escolha for "Original", indicando que a resolução das fotos originais de câmera deve ser mantida.
        manter_original = "Original" in escolha

        # Inicializa coletores vazios de dados.
        dados_fotos = [] # Coleta as fotos com metadados de GPS válidos.
        fotos_sem_gps = [] # Coleta nomes de fotos sem dados de GPS para relatório de avisos.
        fotos_erro = [] # Coleta nomes de fotos com erro de leitura física.
        # Guarda o total de fotos selecionadas pelo usuário.
        total = len(self.caminhos_fotos)

        # Varre sequencialmente cada imagem da lista (iniciando do índice 1) para processar seus dados.
        for index, caminho in enumerate(self.caminhos_fotos, start=1):
            # Atualiza o progresso visual da barra de progresso (entre 0.0 e 1.0).
            self.progress_bar.set(index / total)
            # Atualiza o texto informando qual imagem está sendo analisada no momento.
            self.lbl_status_processo.configure(text=f"Processando ({index}/{total}): {os.path.basename(caminho)}")
            # Força a interface visual a se redesenhar para atualizar as legendas informadas acima.
            self.update_idletasks()

            # Extrai o nome do arquivo.
            nome_foto = os.path.basename(caminho)
            # Tenta realizar a leitura e redimensionamento da imagem de forma isolada de erros.
            try:
                # Abre o arquivo de imagem em formato JPG em modo de leitura binária ('rb').
                with open(caminho, 'rb') as f:
                    # Inicializa o leitor de metadados EXIF para ler as propriedades de coordenadas da imagem.
                    img_exif = ExifImage(f)
                    
                    # Se a imagem possuir metadados de EXIF declarados e tiver tags de latitude e longitude registradas nela.
                    if img_exif.has_exif and hasattr(img_exif, 'gps_latitude') and hasattr(img_exif, 'gps_longitude'):
                        # Converte as coordenadas lidas em DMS para graus decimais de Latitude.
                        lat = self.converter_para_decimal(img_exif.gps_latitude, img_exif.gps_latitude_ref)
                        # Converte as coordenadas lidas em DMS para graus decimais de Longitude.
                        lon = self.converter_para_decimal(img_exif.gps_longitude, img_exif.gps_longitude_ref)
                        
                        # Se as coordenadas convertidas forem nulas por falha matemática.
                        if lat is None or lon is None:
                            # Adiciona o nome da foto à lista de fotos sem georreferenciamento e passa para a próxima imagem.
                            fotos_sem_gps.append(nome_foto)
                            continue
                        
                        # Processamento físico da imagem (redimensionamento e orientação).
                        # Se configurado para manter a resolução original das fotos.
                        if manter_original:
                            # Reposiciona o ponteiro de leitura do arquivo no início.
                            f.seek(0)
                            # Lê o conteúdo em bytes brutos da foto original por completo.
                            bytes_finais = f.read()
                        # Caso configurado para compactar ou otimizar a imagem para o mapa.
                        else:
                            # Abre a imagem usando a biblioteca de processamento Pillow.
                            with PILImage.open(caminho) as pil_img:
                                # Corrige a orientação da imagem física baseando-se nas propriedades EXIF de rotação (garante que fotos em pé não fiquem deitadas).
                                pil_img = ImageOps.exif_transpose(pil_img)
                                # Redimensiona a imagem mantendo a sua proporção física de aspecto até a largura máxima de pixels definida.
                                pil_img.thumbnail((tamanho_max, tamanho_max))
                                # Cria um reservatório temporário de dados (buffer de memória) na memória RAM (BytesIO).
                                buffer = BytesIO()
                                # Salva os pixels da imagem em formato comprimido JPEG com qualidade de 82% direto na memória de dados temporária (buffer).
                                pil_img.save(buffer, format="JPEG", quality=82)
                                # Obtém o conjunto de bytes da imagem tratada a partir do buffer criado.
                                bytes_finais = buffer.getvalue()

                        # Cria uma rota interna virtual única para a foto dentro do arquivo ZIP do KMZ (ex: "imagens/foto_1_fazenda.jpg").
                        nome_interno = f"imagens/foto_{index}_{nome_foto}"
                        # Guarda todas as informações tratadas desta foto em um dicionário.
                        dados_fotos.append({
                            'nome': nome_foto, 
                            'nome_interno': nome_interno,
                            'lat': lat, 
                            'lon': lon, 
                            'bytes': bytes_finais
                        })
                    # Se a foto não possuir cabeçalho EXIF ou dados de GPS.
                    else:
                        # Guarda o nome na lista de fotos sem dados GPS.
                        fotos_sem_gps.append(nome_foto)
            # Se ocorrer alguma falha durante a leitura da imagem ou no processamento de Pillow.
            except Exception as e:
                # Registra a falha no console e armazena o nome do arquivo para relatório.
                print(f"Erro ao ler imagem {nome_foto}: {e}")
                fotos_erro.append(nome_foto)

        # Montagem do arquivo final comprimido KMZ caso tenhamos fotos válidas com dados geográficos de GPS.
        if dados_fotos:
            # Inicializa a criação do documento KML a partir da biblioteca simplekml.
            kml = simplekml.Kml()
            # Cria um estilo personalizado para os ícones do mapa.
            style = kml.newstyle(id="iconeCamera")
            # Configura o endereço padrão da imagem de ícone que aparecerá no Google Earth (uma pequena câmera azul/cinza).
            style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/camera.png"
            # Define o tamanho de escala visual do ícone de câmera no mapa (escala de 1.2).
            style.iconstyle.scale = 1.2

            # Varre cada uma das fotos salvas com coordenadas válidas.
            for foto in dados_fotos:
                # Adiciona um ponto geográfico (Placemark) no mapa nas coordenadas correspondentes da foto (X, Y).
                pnt = kml.newpoint(name=foto['nome'], coords=[(foto['lon'], foto['lat'])])
                # Atribui o estilo de ícone de câmera configurado anteriormente ao ponto.
                pnt.style = style
                
                # Estrutura visual em HTML referenciando o caminho da foto dentro do arquivo compactado do mapa.
                # Quando o usuário clicar no ícone de câmera no mapa, abrirá uma janela pop-up flutuante com a foto e as coordenadas exatas.
                pnt.description = f"""
                <div style='width:{largura_balao}px; font-family: sans-serif; padding: 10px; text-align: center;'>
                    <h3 style='margin: 0 0 10px 0; color: #1f538d; font-size: 15px;'>{foto['nome']}</h3>
                    <img src='{foto['nome_interno']}' style='max-width:100%; border-radius:8px; box-shadow: 0 4px 8px rgba(0,0,0,0.25);'><br>
                    <div style='margin-top: 10px; font-size: 11px; color: #555; text-align: left; background-color: #f5f5f5; padding: 6px; border-radius: 4px;'>
                        <b>Latitude (Y):</b> {foto['lat']:.7f}<br>
                        <b>Longitude (X):</b> {foto['lon']:.7f}
                    </div>
                </div>
                """

            # Tenta gerar e compactar o arquivo KMZ definitivo.
            try:
                # Cria fisicamente o arquivo ZIP com compressão DEFLATED no caminho definido pelo usuário.
                with zipfile.ZipFile(self.caminho_saida, 'w', zipfile.ZIP_DEFLATED) as kmz:
                    # 1. Grava os dados do mapa geográfico KML criados na memória em um arquivo interno chamado 'doc.kml'.
                    kmz.writestr("doc.kml", kml.kml())
                    # 2. Grava todas as fotos processadas (bytes) em suas respectivas rotas internas dentro do arquivo comprimido.
                    for foto in dados_fotos:
                        kmz.writestr(foto['nome_interno'], foto['bytes'])

                # Sinaliza que o processamento terminou com sucesso em verde.
                self.lbl_status_processo.configure(text="✅ Processamento Concluído!", text_color="green")
                
                # Monta a mensagem final sintetizada resumindo os resultados de todo o processo de conversão de fotos.
                res_mensagem = f"Arquivo KMZ gerado com sucesso!\n• Fotos no mapa: {len(dados_fotos)}"
                # Se houveram fotos sem GPS identificadas.
                if fotos_sem_gps:
                    # Adiciona contagem na mensagem final.
                    res_mensagem += f"\n• Ignoradas (Sem GPS): {len(fotos_sem_gps)}"
                # Se houveram erros de leitura.
                if fotos_erro:
                    res_mensagem += f"\n• Erros de leitura: {len(fotos_erro)}"
                
                # Exibe caixinha clássica com o resumo total de sucesso da exportação de fotos.
                messagebox.showinfo("Sucesso", res_mensagem)
                
                # Se existirem fotos ignoradas por falta de dados GPS.
                if fotos_sem_gps:
                    # Junta o nome das primeiras 15 fotos sem GPS separadas por quebra de linha.
                    lista_sem_gps = "\n".join(fotos_sem_gps[:15])
                    # Se forem mais do que 15, adiciona uma linha indicando que existem outras.
                    if len(fotos_sem_gps) > 15:
                        lista_sem_gps += "\n... e outras."
                    # Mostra caixinha de aviso listando as fotos ignoradas pelo sistema.
                    messagebox.showwarning(
                        "Fotos sem Georreferenciamento", 
                        f"As seguintes fotos foram ignoradas por não conter metadados de GPS:\n\n{lista_sem_gps}"
                    )

                # Tenta abrir automaticamente o arquivo KMZ no computador usando o programa associado (ex: Google Earth Pro).
                os.startfile(self.caminho_saida)
            # Captura falha física de gravação de arquivo no computador (ex: arquivo KMZ aberto em outro programa ou pasta bloqueada).
            except Exception as e:
                # Exibe pop-up informando o erro específico.
                messagebox.showerror("Erro", f"Erro ao gerar ou salvar o arquivo KMZ:\n{str(e)}")
        # Se nenhuma das fotos continha coordenadas de geolocalização válidas.
        else:
            # Exibe aviso informando a impossibilidade de gerar o arquivo.
            self.lbl_status_processo.configure(text="❌ Falha na geração do KMZ.", text_color="red")
            messagebox.showwarning("Aviso", "Nenhuma das fotos selecionadas continha coordenadas GPS válidas.")
        
        # Reativa o botão de geração para permitir novos processamentos.
        self.btn_gerar.configure(state="normal")
        # Zera a barra de progresso visual.
        self.progress_bar.set(0)
