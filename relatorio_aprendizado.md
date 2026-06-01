# Relatório Didático: Arquitetura do GeoKit e Glossário de Programação

Este documento foi elaborado especialmente para você, leitor de telas, e está escrito 100% na língua portuguesa do Brasil. Ele explica detalhadamente a estrutura do projeto **GeoKit**, ensina conceitos de programação utilizando exemplos do próprio programa e apresenta um glossário completo para traduzir e desmistificar qualquer termo técnico em inglês encontrado no desenvolvimento do software.

---

## 📂 1. Estrutura e Arquitetura do Projeto

Pense em um software como um edifício comercial. O edifício é dividido em salas e departamentos, cada um com uma função específica. No GeoKit, esses "departamentos" são as pastas e arquivos de código.

Abaixo está o mapa de como o projeto está organizado e estruturado no computador:

*   **`FerramentasGeo/`** (Pasta Principal do Projeto)
    *   `main.py` (O interruptor inicial do programa)
    *   `requirements.txt` (A lista de bibliotecas necessárias para rodar o programa)
    *   `version.json` (Arquivo que guarda o número da versão atual do software)
    *   `build_spec.py` (Script que comanda a compilação do executável)
    *   `GeoKit.spec` (Arquivo de especificações técnicas do PyInstaller)
    *   `build.bat` (Arquivo de automação em lote do Windows)
    *   `make_release.py` (Script para publicação de nova versão na internet)
    *   `geokit/` (A fábrica do programa)
        *   `__init__.py` (Certidão de registro da pasta como um pacote)
        *   `app.py` (A moldura visual e painel de navegação da janela principal)
        *   `updater.py` (O gerenciador de atualizações automáticas)
        *   `modules/` (O setor de ferramentas de trabalho)
            *   `__init__.py` (Registro da subpasta de ferramentas)
            *   `sinaflor.py` (Conversor de planilhas para o padrão do SinaFlor do IBAMA)
            *   `fepam.py` (Reprojetor de arquivos de mapa para o padrão da FEPAM)
            *   `fotos.py` (Conversor de fotos com GPS em mapas do Google Earth)

---

## 📖 2. Glossário Didático de Termos e Jargões em Inglês

Abaixo está a lista de termos em inglês usados no código do GeoKit e suas respectivas explicações didáticas em português:

1.  **Try e Except (Tentar e Capturar)**: Uma estrutura de código que tenta executar comandos perigosos no bloco `try`. Se ocorrer alguma falha, ele desvia o programa para o bloco `except`, evitando que o programa feche de repente.
2.  **Main Loop (Laço Principal)**: O motor visual de um aplicativo de janela. É um ciclo contínuo que roda centenas de vezes por segundo esperando você interagir com a tela (como clicar em um botão).
3.  **Frame (Moldura ou Painel)**: Um contêiner retangular invisível que serve para organizar botões e textos juntos em uma mesma área da janela.
4.  **Grid (Grelha)**: Sistema de layout que organiza os elementos visuais na janela como se fossem células de uma tabela (divididos em linhas e colunas).
5.  **Padding (Espaçamento Interno/Externo)**: Margem de distância em pixels adicionada nas laterais ou acima/abaixo de um botão para que ele não fique colado nas bordas.
6.  **Daemon (Tarefa em Segundo Plano)**: Um processo secundário executado de forma paralela ao programa principal, usado para tarefas como verificar atualizações de rede sem congelar a janela principal.
7.  **Callback (Retorno de Chamada)**: Uma função que você passa como argumento para outra tarefa, instruindo-a a ser executada somente após a conclusão daquela tarefa (por exemplo, avisar a tela principal quando o download terminar).
8.  **Buffer (Reservatório Temporário)**: Área da memória RAM do computador que armazena pedaços de arquivos (como fotos sendo redimensionadas) antes de salvá-las no disco rígido.
9.  **Timeout (Tempo Limite de Espera)**: Período máximo em segundos que o programa esperará para se conectar à internet antes de desistir e exibir uma mensagem de erro de conexão.
10. **User-Agent (Identificação do Navegador)**: Um pequeno cabeçalho de texto que o programa envia à internet para se identificar e provar para os sites que ele é um aplicativo seguro.
11. **Payload (Carga de Dados Úteis)**: O conteúdo principal de informações transmitidas durante uma conexão na rede (como as notas de versão do software enviadas em formato de texto).
12. **Token (Chave Secreta de Acesso)**: Uma senha de segurança muito longa gerada no GitHub para permitir que o script `make_release.py` envie atualizações ao repositório de forma automatizada.
13. **Commit (Registro de Versão)**: Ação de salvar permanentemente o estado do seu código na linha do tempo do sistema Git (controle de versão local).
14. **Push (Empurrar/Enviar)**: Enviar os arquivos que você registrou localmente no Git para o repositório remoto online (hospedado no GitHub).
15. **Upload (Carregamento na Rede)**: O ato de enviar um arquivo que está no seu computador local para um servidor distante na internet.
16. **Release (Lançamento Oficial)**: A publicação oficial de uma nova versão do software que está pronta para ser baixada pelos usuários.
17. **Asset (Recurso Anexo)**: Arquivo complementar anexado a um lançamento na internet, no nosso caso, o arquivo `GeoKit.zip` contendo o programa compilado.
18. **Zip (Arquivo Comprimido)**: Formato de compressão que junta vários arquivos e pastas dentro de um único pacote leve.
19. **Exe (Executável Standalone)**: Arquivo que roda o programa de forma independente em computadores Windows, sem exigir que o Python esteja instalado na máquina.
20. **EXIF (Metadados da Imagem)**: Dados técnicos invisíveis que ficam gravados dentro dos arquivos de fotos gerados por celulares ou câmeras (como data, hora, modelo do celular e coordenadas geográficas de GPS).
21. **CRS (Sistema de Referência de Coordenadas)**: O modelo matemático utilizado para localizar e projetar pontos geográficos tridimensionais do globo terrestre sobre uma superfície plana de mapa.
22. **Shapefile e GeoPackage (Arquivos de Mapa)**: Os formatos de arquivo mais populares da área de geoprocessamento para salvar polígonos, linhas e pontos geográficos no computador.
23. **Pop-up (Caixa de Diálogo Flutuante)**: Uma pequena janela temporária que aparece no centro da tela para exibir uma mensagem de sucesso, alerta ou erro.
24. **Modal (Janela Exclusiva)**: Uma janela de aviso que bloqueia e impede que o usuário interaja com a janela principal atrás até que ele leia a mensagem e clique em fechar.

---

## 💻 3. Aprendendo a Programar com o GeoKit

Vamos entender os conceitos mais importantes da programação usando exemplos reais do código do GeoKit:

### A. O que são Variáveis?
Variáveis são como gavetas etiquetadas na memória do computador. Você coloca um dado lá dentro e dá um nome para a gaveta para poder utilizá-lo depois.

*   **Exemplo prático no GeoKit (`geokit/__init__.py`):**
    ```python
    __version__ = "1.1.0"
    ```
    Aqui, criamos uma gaveta chamada `__version__` e guardamos o texto `"1.1.0"` dentro dela. Sempre que o programa precisar saber a versão, ele olha dentro dessa gaveta.

### B. O que são Importações (`import`)?
Ninguém programa tudo do zero. As importações trazem ferramentas adicionais criadas por outros programadores para dentro do seu código.

*   **Exemplo prático (`main.py`):**
    ```python
    import sys
    import customtkinter as ctk
    ```
    *   `sys` é uma caixa de ferramentas nativa do Python para interagir com o sistema operacional.
    *   `customtkinter` é uma biblioteca moderna usada para desenhar janelas e botões. Nós a importamos com o apelido de `ctk` para ficar mais fácil e curto de digitar no código.

### C. O que são Funções (`def`)?
Uma função é uma receita de bolo ou uma máquina. Ela recebe ingredientes (dados de entrada), executa passos lógicos e devolve um resultado (retorno). Definimos funções com a palavra `def`.

*   **Exemplo prático (`geokit/modules/sinaflor.py`):**
    ```python
    def formatar_gms(self, valor):
        decimal = abs(valor)
        g = int(decimal)
        ...
        return grau_final, m, s
    ```
    Essa função chama-se `formatar_gms`. Ela recebe um número em formato decimal (o ingrediente `valor`), faz contas de divisão e multiplicação por 60 para descobrir os Graus, Minutos e Segundos, e devolve (com o `return`) os três números organizados.

### D. Estruturas de Decisão (`if`, `elif`, `else`)
São desvios no caminho do código baseados em condições. É como decidir: "Se estiver chovendo, levo guarda-chuva. Senão, não levo."

*   **Exemplo prático (`geokit/app.py`):**
    ```python
    if tema_selecionado == "Claro":
        ctk.set_appearance_mode("Light")
    elif tema_selecionado == "Escuro":
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("System")
    ```
    O programa verifica o texto guardado na variável `tema_selecionado`:
    *   `if` (se) for igual a `"Claro"`, muda o visual para Light.
    *   `elif` (senão se) for igual a `"Escuro"`, muda o visual para Dark.
    *   `else` (senão / caso contrário), segue a configuração padrão do Windows.

---

## 🛠️ 4. As Três Super-Bibliotecas Usadas no GeoKit

O GeoKit utiliza três grandes bibliotecas especializadas que você deve conhecer:

1.  **CustomTkinter (`ctk`)**: É quem desenha a tela gráfica moderna. Ela cria caixas de texto com cantos arredondados, botões com efeitos de clique e altera cores dinamicamente ao mudar de tema escuro para claro.
2.  **Pandas (`pd`)**: É uma planilha eletrônica virtual na memória. Ela abre arquivos de Excel em milissegundos e nos deixa pesquisar colunas, filtrar linhas em branco e extrair dados sem precisar abrir o programa Excel.
3.  **GeoPandas (`gpd`)**: É o irmão geográfico do Pandas. Além de ler dados tabulares, ele sabe ler coordenadas espaciais, desenhar polígonos (como o mapa de municípios) e converter projeções cartográficas inteiras (ex: transformar dados em metros do sistema UTM para graus do sistema SIRGAS 2000).
