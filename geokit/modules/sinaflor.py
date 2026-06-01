# A linha abaixo importa o módulo 'os' da biblioteca padrão para gerenciar caminhos de arquivos e pastas no computador.
import os

# A linha abaixo importa o módulo 'zipfile' para criar e compactar o arquivo final em formato .kmz (que é um ZIP renomeado).
import zipfile

# A linha abaixo importa a biblioteca 'pandas' sob o apelido de 'pd'. Ela é a ferramenta mais famosa para ler e manipular tabelas de dados em Python.
import pandas as pd

# A linha abaixo importa a biblioteca 'customtkinter' sob o apelido 'ctk' para podermos desenhar janelas e botões modernos.
import customtkinter as ctk

# A linha abaixo importa ferramentas de diálogo de arquivos ('filedialog') e janelas de alerta ('messagebox') da biblioteca básica tkinter.
from tkinter import filedialog, messagebox

# A linha abaixo define uma classe chamada 'FrameSinaFlor'.
# Ela herda de 'ctk.CTkFrame', o que significa que ela é um painel ou tela secundária que será desenhada dentro do contêiner do programa.
class FrameSinaFlor(ctk.CTkFrame):
    # A linha abaixo define o construtor da tela. O parâmetro 'master' indica quem é o pai (onde esta tela será desenhada).
    def __init__(self, master, **kwargs):
        # A linha abaixo chama o construtor do painel original (classe pai) configurando sua cor de fundo como transparente.
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # A linha abaixo define uma variável 'df_global' inicializada como 'None' (nula).
        # Ela guardará os dados da nossa planilha Excel ou CSV depois que ela for aberta na memória.
        self.df_global = None

        # As linhas abaixo criam o título principal da tela "Conversor de Coordenadas SinaFlor" em negrito com tamanho 22.
        ctk.CTkLabel(
            self, 
            text="Conversor de Coordenadas SinaFlor", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(15, 10))

        # As linhas abaixo criam o botão para carregar a planilha Excel ou arquivo CSV.
        self.btn_carregar = ctk.CTkButton(
            self, 
            text="1. Carregar Planilha (Excel/CSV)", 
            command=self.carregar_arquivo,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        # A linha abaixo posiciona o botão na tela com um espaçamento vertical (pady).
        self.btn_carregar.pack(pady=10)

        # A linha abaixo cria um texto de status que indica se há algum arquivo aberto ou não.
        self.lbl_arquivo = ctk.CTkLabel(self, text="Nenhum arquivo carregado", text_color="gray")
        # A linha abaixo posiciona o texto de status na tela.
        self.lbl_arquivo.pack()

        # As linhas abaixo criam uma instrução para avisar ao usuário que ele deve selecionar as colunas de Latitude e Longitude da sua planilha.
        ctk.CTkLabel(
            self, 
            text="Selecione as colunas correspondentes à Latitude e Longitude:", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(20, 5))

        # A linha abaixo cria um mini-painel invisível (Frame) para alinhar os seletores de Latitude e Longitude lado a lado.
        self.frame_menus = ctk.CTkFrame(self, fg_color="transparent")
        # A linha abaixo posiciona o mini-painel na tela com espaçamento vertical.
        self.frame_menus.pack(pady=10)

        # ---------------- MENU DE LATITUDE ----------------
        # A linha abaixo cria um pequeno painel para organizar a legenda e o menu de seleção da Latitude.
        self.frame_lat = ctk.CTkFrame(self.frame_menus, fg_color="transparent")
        # Posiciona este painel à esquerda dentro do painel de alinhamento.
        self.frame_lat.pack(side="left", padx=15)
        # Cria a legenda do menu: "Latitude (Y):".
        ctk.CTkLabel(self.frame_lat, text="Latitude (Y):", font=ctk.CTkFont(size=11, weight="bold")).pack()
        # Cria o menu de seleção de opções (OptionMenu) onde as colunas da planilha aparecerão. Inicialmente contém "Selecione...".
        self.menu_lat = ctk.CTkOptionMenu(self.frame_lat, values=["Selecione..."], width=180)
        # Posiciona o menu de seleção de Latitude.
        self.menu_lat.pack(pady=5)

        # ---------------- MENU DE LONGITUDE ----------------
        # A linha abaixo cria um pequeno painel para organizar a legenda e o menu de seleção da Longitude.
        self.frame_lon = ctk.CTkFrame(self.frame_menus, fg_color="transparent")
        # Posiciona este painel à esquerda, ficando ao lado do painel de Latitude.
        self.frame_lon.pack(side="left", padx=15)
        # Cria a legenda do menu: "Longitude (X):".
        ctk.CTkLabel(self.frame_lon, text="Longitude (X):", font=ctk.CTkFont(size=11, weight="bold")).pack()
        # Cria o menu de seleção da Longitude.
        self.menu_lon = ctk.CTkOptionMenu(self.frame_lon, values=["Selecione..."], width=180)
        # Posiciona o menu de seleção de Longitude.
        self.menu_lon.pack(pady=5)

        # ---------------- BOTÕES DE AÇÃO ----------------
        # A linha abaixo cria um painel invisível para alinhar os botões de ação final.
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        # Posiciona o painel na tela.
        self.frame_botoes.pack(pady=15)

        # As linhas abaixo criam o botão de converter as coordenadas e copiar o resultado direto para o clipboard (área de transferência).
        self.btn_converter = ctk.CTkButton(
            self.frame_botoes, 
            text="2. Converter e Copiar", 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            command=self.converter,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        # Posiciona o botão à esquerda dentro do painel de botões.
        self.btn_converter.pack(side="left", padx=10)

        # As linhas abaixo criam o botão para gerar o mapa geográfico KMZ contendo os pontos da planilha para abrir no Google Earth.
        self.btn_kmz = ctk.CTkButton(
            self.frame_botoes, 
            text="3. Gerar e Abrir KMZ", 
            fg_color="#C85A17", 
            hover_color="#a04812",
            command=self.gerar_kmz,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        # Posiciona o botão à esquerda, ao lado do botão de conversão.
        self.btn_kmz.pack(side="left", padx=10)

        # ---------------- CAIXA DE TEXTO DE RESULTADO ----------------
        # As linhas abaixo criam um aviso didático informando o significado dos cabeçalhos Lat_G e Lon_G em conformidade com o IBAMA.
        self.lbl_aviso_cabecalho = ctk.CTkLabel(
            self,
            text="* Nota: O resultado abaixo utiliza as colunas 'Lat_G', 'Lat_M', 'Lat_S' (Graus, Minutos e Segundos) conforme exigido pelo sistema SinaFlor do IBAMA.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#1f538d",
            wraplength=650
        )
        self.lbl_aviso_cabecalho.pack(pady=(5, 5))

        # As linhas abaixo criam um texto de ajuda indicando que a caixa de texto abaixo exibirá o resultado em Graus, Minutos e Segundos (DMS - Graus, Minutos, Segundos).
        ctk.CTkLabel(self, text="Resultado da conversão (DMS):", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(anchor="w", padx=45, pady=(5, 2))
        # Cria a caixa de texto de múltiplas linhas para exibir as coordenadas convertidas. Ela usa fonte Monoespaçada 'Consolas' para alinhar colunas.
        self.txt_saida = ctk.CTkTextbox(self, height=280, width=680, font=ctk.CTkFont(family="Consolas", size=11))
        # Posiciona a caixa de texto na tela de forma que ela se expanda para preencher todo o espaço vertical livre.
        self.txt_saida.pack(pady=(0, 15), padx=20, fill="both", expand=True)

    # A linha abaixo define o método responsável por abrir o explorador de arquivos e carregar a planilha selecionada pelo usuário.
    def carregar_arquivo(self):
        # Abre o explorador de arquivos do Windows configurando os tipos de formatos suportados (.xlsx, .csv, .xls).
        caminho = filedialog.askopenfilename(
            title="Selecionar Planilha",
            filetypes=[("Planilhas do Excel ou CSV", "*.xlsx *.csv *.xls")]
        )
        # Verifica se o usuário não escolheu nenhum arquivo (clicou em cancelar).
        if not caminho: 
            # Interrompe a execução do método imediatamente.
            return
        
        # Abre um bloco para tentar ler a planilha de forma segura contra falhas de formatação.
        try:
            # Se o caminho do arquivo terminar com as extensões do Microsoft Excel (.xlsx ou .xls).
            if caminho.endswith(('.xlsx', '.xls')): 
                # Usa a biblioteca Pandas para ler o arquivo Excel e armazena na nossa variável global.
                self.df_global = pd.read_excel(caminho)
            # Se o arquivo for um arquivo de texto separado por vírgulas (.csv).
            else: 
                # Usa a biblioteca Pandas para ler o arquivo CSV.
                self.df_global = pd.read_csv(caminho)
            
            # Obtém apenas o nome base do arquivo (exemplo: "dados.xlsx") descartando a rota de pastas completa.
            nome_arquivo = os.path.basename(caminho)
            # Atualiza o texto da tela informando que o arquivo foi carregado com sucesso em verde.
            self.lbl_arquivo.configure(text=f"Planilha carregada: {nome_arquivo}", text_color="green")
            
            # Extrai os nomes de todas as colunas existentes na planilha e transforma em uma lista.
            colunas = list(self.df_global.columns)
            # Atualiza as opções dos menus suspensos de Latitude com as colunas reais da planilha.
            self.menu_lat.configure(values=colunas)
            # Define o texto padrão inicial do menu como "Selecione...".
            self.menu_lat.set("Selecione...")
            # Atualiza as opções do menu suspenso da Longitude.
            self.menu_lon.configure(values=colunas)
            # Define o texto padrão inicial do menu como "Selecione...".
            self.menu_lon.set("Selecione...")
            
            # As linhas abaixo executam uma busca inteligente automática para tentar adivinhar e pré-selecionar as colunas corretas.
            for col in colunas:
                # Converte o nome da coluna para letras minúsculas para facilitar a comparação flexível.
                col_lower = str(col).lower()
                # Se a palavra for parecida com termos usados para Latitude (lat, y, lat_dec).
                if col_lower in ['latitude', 'lat', 'lat_dec', 'lat_y', 'y']:
                    # Configura o menu da Latitude automaticamente com essa coluna identificada.
                    self.menu_lat.set(col)
                # Se a palavra for parecida com termos usados para Longitude (lon, long, x, lon_dec).
                if col_lower in ['longitude', 'lon', 'long', 'lon_dec', 'lon_x', 'x']:
                    # Configura o menu da Longitude automaticamente com essa coluna identificada.
                    self.menu_lon.set(col)
                    
        # Se ocorrer algum erro durante a leitura da planilha (ex: arquivo corrompido ou aberto no Excel bloqueando leitura).
        except Exception as e:
            # Exibe uma caixa de diálogo clássica com o erro detalhado.
            messagebox.showerror("Erro", f"Falha ao ler o arquivo:\n{str(e)}")

    # A linha abaixo define a função matemática que converte coordenadas em Graus Decimais (ex: -30.0158) para GMS (Graus, Minutos e Segundos).
    def formatar_gms(self, valor):
        """Converte um valor decimal em Graus, Minutos e Segundos."""
        # Obtém o valor absoluto do número (descarta o sinal de menos se houver).
        decimal = abs(valor)
        # Os Graus correspondem à parte inteira do número (antes do ponto decimal).
        g = int(decimal)
        # Multiplica a parte decimal por 60 para descobrir a parte inteira dos Minutos.
        m = int((decimal - g) * 60)
        # Multiplica a sobra decimal por 60 para obter os Segundos e arredonda para 4 casas decimais.
        s = round(((decimal - g) * 60 - m) * 60, 4)
        # Se o valor original for negativo (exemplo: sul ou oeste), define o Grau final como negativo.
        grau_final = -g if valor < 0 else g
        # Retorna o resultado final estruturado em três variáveis.
        return grau_final, m, s

    # A linha abaixo define o método acionado ao clicar no botão "2. Converter e Copiar".
    def converter(self):
        # Verifica se o usuário não carregou nenhuma planilha de dados ainda.
        if self.df_global is None:
            # Exibe um alerta na tela avisando que a planilha precisa ser selecionada.
            messagebox.showwarning("Aviso", "Por favor, carregue uma planilha primeiro!")
            # Interrompe a execução do método.
            return
        
        # Obtém os nomes das colunas de latitude e longitude que estão ativas nos menus suspensos.
        col_lat = self.menu_lat.get()
        col_lon = self.menu_lon.get()
        
        # Verifica se o usuário deixou algum dos seletores com o texto "Selecione...".
        if col_lat == "Selecione..." or col_lon == "Selecione...":
            # Exibe um aviso pedindo para configurar as colunas corretamente.
            messagebox.showwarning("Aviso", "Selecione as colunas de Latitude e Longitude!")
            # Interrompe a execução.
            return

        # Limpa todo o conteúdo atual que porventura exista dentro da caixa de texto de resultado.
        self.txt_saida.delete("1.0", "end")
        # Define a linha de cabeçalho da tabela separada por tabulação (tab) padrão do formato SinaFlor.
        header = "Lat_G\tLat_M\tLat_S\tLon_G\tLon_M\tLon_S\n"
        # Insere a linha de cabeçalho no início da caixa de texto.
        self.txt_saida.insert("end", header)

        # Inicializa uma lista vazia para armazenar as linhas que forem convertidas com sucesso.
        linhas_convertidas = []
        # Inicia um laço de repetição que varre cada uma das linhas da planilha carregada (iterrows).
        for _, row in self.df_global.iterrows():
            # Inicia o tratamento de erro individual para a linha atual (para evitar que uma coordenada inválida interrompa todas as outras).
            try:
                # Obtém o valor cru da célula correspondente à Latitude e Longitude na linha atual.
                val_lat = row[col_lat]
                val_lon = row[col_lon]
                
                # Se a célula estiver vazia (NaN - Not a Number), ignora e pula para a próxima linha de dados.
                if pd.isna(val_lat) or pd.isna(val_lon):
                    continue
                    
                # Converte os valores textuais para números decimais (float) e calcula o GMS correspondente.
                lat_g, lat_m, lat_s = self.formatar_gms(float(val_lat))
                lon_g, lon_m, lon_s = self.formatar_gms(float(val_lon))
                
                # Monta a linha de texto alinhada com tabulações (\t) para fácil colagem direta no Microsoft Excel.
                linha = f"{lat_g}\t{lat_m}\t{lat_s}\t{lon_g}\t{lon_m}\t{lon_s}\n"
                # Insere a linha convertida no final da caixa de texto gráfica.
                self.txt_saida.insert("end", linha)
                # Adiciona a linha de texto na nossa lista de controle.
                linhas_convertidas.append(linha)
            # Se ocorrer qualquer erro na conversão dos dados (exemplo: texto digitado onde deveria haver um número).
            except Exception:
                # Apenas ignora e segue para a próxima coordenada.
                continue

        # Se conseguimos converter pelo menos uma linha de coordenadas com sucesso.
        if linhas_convertidas:
            # Obtém todo o texto gerado na caixa de texto do início ao fim (removendo quebras de linhas extras no final).
            conteudo = self.txt_saida.get("1.0", "end-1c")
            # Limpa o conteúdo atual da área de transferência do Windows (memória de cópia temporária).
            self.clipboard_clear()
            # Copia o texto estruturado para a área de transferência do Windows.
            self.clipboard_append(conteudo)
            # Força o aplicativo a sincronizar as alterações com o sistema operacional imediatamente.
            self.update()
            # Mostra mensagem informando que os dados foram copiados e podem ser colados no Excel com Ctrl+V.
            messagebox.showinfo(
                "Sucesso", 
                "Conversão concluída!\nO resultado foi copiado automaticamente para a área de transferência."
            )
        # Se nenhuma linha pôde ser processada.
        else:
            # Exibe um alerta de aviso informando a falta de dados convertidos.
            messagebox.showwarning("Aviso", "Nenhum dado válido de coordenada pôde ser convertido.")

    # A linha abaixo define o método acionado ao clicar no botão "3. Gerar e Abrir KMZ".
    def gerar_kmz(self):
        # Verifica se o usuário não carregou planilha.
        if self.df_global is None:
            # Alerta a necessidade de carregar um arquivo.
            messagebox.showwarning("Aviso", "Por favor, carregue uma planilha primeiro!")
            # Interrompe execução.
            return
        
        # Obtém os nomes selecionados para as colunas.
        col_lat = self.menu_lat.get()
        col_lon = self.menu_lon.get()
        
        # Confirma se as colunas foram selecionadas.
        if col_lat == "Selecione..." or col_lon == "Selecione...":
            # Alerta o usuário se a configuração estiver pendente.
            messagebox.showwarning("Aviso", "Selecione as colunas de Latitude e Longitude primeiro!")
            # Interrompe execução.
            return

        # Define uma lista com possíveis nomes de colunas que podem representar o nome ou identificação do ponto geográfico.
        colunas_candidatas = ['nome', 'name', 'ponto', 'point', 'id', 'identificador', 'codigo', 'código', 'local']
        # Inicializa a variável como nula.
        col_nome = None
        # Varre as colunas reais da planilha.
        for c in self.df_global.columns:
            # Se encontrar alguma coluna parecida com os termos candidatos na lista.
            if str(c).lower() in colunas_candidatas:
                # Armazena o nome oficial da coluna identificada.
                col_nome = c
                # Encerra o laço de busca imediato.
                break

        # A linha abaixo começa a montar o arquivo XML do KML estruturado que define os pontos geográficos e estilos.
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Pontos Convertidos SinaFlor</name>
    <Style id="pontoEstilo">
      <IconStyle>
        <scale>1.1</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
        </Icon>
        <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
      </IconStyle>
    </Style>
"""
        
        # Inicializa o contador de quantos pontos geográficos foram processados com sucesso.
        pontos_adicionados = 0
        # Varre cada linha da planilha para extrair os pontos.
        for index, row in self.df_global.iterrows():
            # Abre o bloco de segurança individual para a linha atual.
            try:
                # Obtém os valores de latitude e longitude.
                val_lat = row[col_lat]
                val_lon = row[col_lon]
                
                # Ignora células vazias.
                if pd.isna(val_lat) or pd.isna(val_lon):
                    continue

                # Converte os textos lidos para ponto flutuante (decimal).
                lat_bruta = float(val_lat)
                lon_bruta = float(val_lon)
                
                # Garante coordenadas negativas correspondentes ao hemisfério do Brasil (Sul e Oeste).
                lat_corrigida = -abs(lat_bruta)
                lon_corrigida = -abs(lon_bruta)
                
                # Define o nome do ponto. Se houver coluna de nome, usa-a; caso contrário, gera o nome incremental: "Ponto X".
                nome_ponto = str(row[col_nome]) if col_nome else f"Ponto {index + 1}"
                
                # Cria uma tabela formatada em HTML para aparecer dentro da caixinha de descrição (popup) do ponto no Google Earth.
                desc_html = "<table border='1' style='border-collapse: collapse; font-family: sans-serif; font-size: 11px;'>\n"
                # Para cada coluna existente na tabela da planilha.
                for col in self.df_global.columns:
                    # Adiciona uma linha na tabela HTML contendo o nome da coluna e o valor correspondente da célula.
                    desc_html += f"  <tr><th>{col}</th><td>{row[col]}</td></tr>\n"
                # Fecha a tabela em HTML.
                desc_html += "</table>"

                # Cria o marcador KML do ponto geográfico (Placemark) com nome, descrição, estilo de ícone e coordenadas geográficas (X, Y).
                placemark = f"""    <Placemark>
      <name>{nome_ponto}</name>
      <description><![CDATA[{desc_html}]]></description>
      <styleUrl>#pontoEstilo</styleUrl>
      <Point>
        <coordinates>{lon_corrigida},{lat_corrigida},0</coordinates>
      </Point>
    </Placemark>
"""
                # Soma o marcador textual à estrutura de texto principal do arquivo KML.
                kml_content += placemark
                # Incrementa o número de pontos criados.
                pontos_adicionados += 1
            # Se houver erro de formatação na linha atual, pula para a próxima coordenada.
            except Exception:
                continue
                
        # Fecha as tags do documento e arquivo KML.
        kml_content += "  </Document>\n</kml>\n"
        
        # Se nenhum ponto válido foi adicionado no processo.
        if pontos_adicionados == 0:
            # Exibe mensagem de aviso e interrompe o processo.
            messagebox.showwarning("Aviso", "Nenhum ponto válido encontrado para gerar o KMZ.")
            return

        # Abre a caixa para o usuário escolher o nome e local onde quer salvar o arquivo KMZ final.
        caminho_salvar = filedialog.asksaveasfilename(
            defaultextension=".kmz", 
            filetypes=[("Arquivo KMZ (Google Earth)", "*.kmz")], 
            initialfile="Pontos_SinaFlor.kmz",
            title="Salvar arquivo KMZ"
        )
        # Se o usuário cancelou a janela de salvar arquivo.
        if not caminho_salvar: 
            return
        
        # Tenta criar e compactar o arquivo KMZ no computador.
        try:
            # Cria o arquivo ZIP comprimido no caminho selecionado pelo usuário.
            with zipfile.ZipFile(caminho_salvar, 'w', zipfile.ZIP_DEFLATED) as kmz:
                # Escreve os dados textuais do KML criados na memória dentro de um arquivo chamado 'doc.kml' contido dentro do ZIP.
                kmz.writestr("doc.kml", kml_content)
            
            # Exibe uma caixa de diálogo informando o sucesso da criação.
            messagebox.showinfo("Sucesso", f"Arquivo KMZ gerado com sucesso:\n{os.path.basename(caminho_salvar)}")
            # Tenta abrir o arquivo KMZ automaticamente com o visualizador padrão configurado no Windows (ex: Google Earth Pro).
            os.startfile(caminho_salvar)
        # Captura possíveis erros de salvamento ou falta de permissão de escrita de pasta.
        except Exception as e:
            # Exibe pop-up de erro.
            messagebox.showerror("Erro", f"Erro ao gerar o arquivo KMZ:\n{str(e)}")
