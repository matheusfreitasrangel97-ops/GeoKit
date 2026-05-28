# GeoKit — Caixa de Ferramentas Geográficas

O **GeoKit** é um aplicativo desktop de código aberto desenvolvido em Python com interface moderna (`customtkinter`), projetado especificamente para auxiliar profissionais e estudantes da área de geotecnologias no Brasil a automatizarem rotinas geoespaciais comuns.

---

## 🚀 Funcionalidades Principais

O aplicativo conta com três módulos integrados e independentes:

### 1. 🌲 SinaFlor (Decimais para GMS)
- **Objetivo:** Facilita a tabulação de coordenadas geográficas decimais para o formato de Graus, Minutos e Segundos (GMS) exigido pelo sistema SinaFlor (IBAMA).
- **Recursos:**
  - Carregamento ágil de planilhas Excel (`.xlsx`, `.xls`) ou CSV (`.csv`).
  - Detecção inteligente de colunas de coordenadas.
  - Cópia direta do resultado convertido para a área de transferência do Windows (pronto para colar no Excel).
  - Geração de arquivos KMZ contendo todos os dados e tabelas descritivas.

### 2. 📋 Norma FEPAM 07/2015 (Padronizador de CRS)
- **Objetivo:** Reprojeta e padroniza a projeção de arquivos de dados vetoriais (.shp, .gpkg) para o Sistema de Referência Geocêntrico para as Américas (SIRGAS 2000) no formato Geográfico (EPSG:4674), de acordo com a norma do órgão ambiental.
- **Recursos:**
  - Seleção em lote (múltiplos arquivos).
  - Diagnóstico em tempo real da projeção atual e indicação de inconformidade.
  - Reprojeção automática segura de sistemas projetados (ex: UTM) ou geográficos incompatíveis (ex: WGS84).
  - Criação de pasta organizada com os dados redefinidos.

### 3. 📸 Fotos -> KMZ (Georreferenciamento de Imagens)
- **Objetivo:** Varre metadados EXIF de fotografias tiradas em campo com GPS habilitado e gera um arquivo KMZ compacto.
- **Recursos:**
  - Extração automática de latitude e longitude das fotos.
  - Redimensionamento inteligente opcional para reduzir drasticamente o tamanho do arquivo KMZ final (imagens são salvas no zip do KMZ e linkadas localmente, sem base64, garantindo 100% de compatibilidade com QGIS e Google Earth).
  - Rotação automática baseada no EXIF de orientação (fotos verticais não ficam deitadas).
  - Popups customizados e estilizados com a imagem e coordenadas.

---

## 🛠️ Como Executar

### Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado no computador ou utilize o interpretador Python do QGIS (que já possui a maior parte das dependências geográficas instaladas).

### Opção A: Execução via Interpretador Padrão do Python
1. Clone o repositório:
   ```bash
   git clone https://github.com/matheusfreitasrangel97-ops/GeoKit.git
   cd GeoKit
   ```
2. Instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   python main.py
   ```

### Opção B: Execução utilizando o QGIS (Recomendado para usuários sem Python na máquina)
Caso você tenha o QGIS instalado, você pode executar o GeoKit diretamente usando o terminal do QGIS. No PowerShell do Windows, execute:
```powershell
& "C:\Program Files\QGIS 4.0.1\bin\python-qgis.bat" main.py
```
*(Nota: Certifique-se de instalar as dependências adicionais como `customtkinter`, `simplekml` e `exif` usando o pip do QGIS antes de iniciar).*

---

## 📦 Como Compilar/Gerar Executável (.exe)

Para distribuir o GeoKit como um aplicativo independente (`Standalone`), você pode usar o **PyInstaller**.

1. Instale o PyInstaller no ambiente desejado:
   ```bash
   pip install pyinstaller
   ```
2. Execute o comando de compilação:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --name "GeoKit" main.py
   ```
   *(Ou aponte para o batch script do QGIS caso compile a partir dele).*
3. O executável final estará disponível na pasta `dist/GeoKit/GeoKit.exe`.

---

## 🔄 Sistema de Atualizações

O GeoKit possui um sistema inteligente de verificação de versão assíncrono. Ao iniciar, ele consulta um arquivo de configuração remoto hospedado no GitHub para verificar se novas melhorias estão disponíveis. Se encontrar uma versão superior à atual, uma notificação amigável é exibida permitindo ao usuário abrir a página do projeto para fazer o download.

---

## ✒️ Créditos e Contato

- **Desenvolvedor:** Matheus Rangel
- **Telefone:** (51) 99790-3841
- **Licença:** Livre para distribuição, modificação e uso comercial/educacional.
