import os
import zipfile
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox

class FrameSinaFlor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.df_global = None

        # Título
        ctk.CTkLabel(
            self, 
            text="Conversor de Coordenadas SinaFlor", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(15, 10))

        # Botão Carregar
        self.btn_carregar = ctk.CTkButton(
            self, 
            text="1. Carregar Planilha (Excel/CSV)", 
            command=self.carregar_arquivo,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_carregar.pack(pady=10)

        self.lbl_arquivo = ctk.CTkLabel(self, text="Nenhum arquivo carregado", text_color="gray")
        self.lbl_arquivo.pack()

        # Seleção de Colunas
        ctk.CTkLabel(
            self, 
            text="Selecione as colunas correspondentes à Latitude e Longitude:", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(20, 5))

        self.frame_menus = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_menus.pack(pady=10)

        # Menu Lat
        self.frame_lat = ctk.CTkFrame(self.frame_menus, fg_color="transparent")
        self.frame_lat.pack(side="left", padx=15)
        ctk.CTkLabel(self.frame_lat, text="Latitude (Y):", font=ctk.CTkFont(size=11, weight="bold")).pack()
        self.menu_lat = ctk.CTkOptionMenu(self.frame_lat, values=["Selecione..."], width=180)
        self.menu_lat.pack(pady=5)

        # Menu Lon
        self.frame_lon = ctk.CTkFrame(self.frame_menus, fg_color="transparent")
        self.frame_lon.pack(side="left", padx=15)
        ctk.CTkLabel(self.frame_lon, text="Longitude (X):", font=ctk.CTkFont(size=11, weight="bold")).pack()
        self.menu_lon = ctk.CTkOptionMenu(self.frame_lon, values=["Selecione..."], width=180)
        self.menu_lon.pack(pady=5)

        # Botões de Ação
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=15)

        self.btn_converter = ctk.CTkButton(
            self.frame_botoes, 
            text="2. Converter e Copiar", 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            command=self.converter,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_converter.pack(side="left", padx=10)

        self.btn_kmz = ctk.CTkButton(
            self.frame_botoes, 
            text="3. Gerar e Abrir KMZ", 
            fg_color="#C85A17", 
            hover_color="#a04812",
            command=self.gerar_kmz,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_kmz.pack(side="left", padx=10)

        # Caixa de Texto de Saída
        ctk.CTkLabel(self, text="Resultado da conversão (DMS):", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(anchor="w", padx=45, pady=(10, 2))
        self.txt_saida = ctk.CTkTextbox(self, height=280, width=680, font=ctk.CTkFont(family="Consolas", size=11))
        self.txt_saida.pack(pady=(0, 15), padx=20, fill="both", expand=True)

    def carregar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar Planilha",
            filetypes=[("Planilhas do Excel ou CSV", "*.xlsx *.csv *.xls")]
        )
        if not caminho: 
            return
        
        try:
            if caminho.endswith(('.xlsx', '.xls')): 
                self.df_global = pd.read_excel(caminho)
            else: 
                self.df_global = pd.read_csv(caminho)
            
            nome_arquivo = os.path.basename(caminho)
            self.lbl_arquivo.configure(text=f"Planilha carregada: {nome_arquivo}", text_color="green")
            
            colunas = list(self.df_global.columns)
            self.menu_lat.configure(values=colunas)
            self.menu_lat.set("Selecione...")
            self.menu_lon.configure(values=colunas)
            self.menu_lon.set("Selecione...")
            
            # Tentar pré-selecionar colunas de latitude/longitude caso encontre nomes óbvios
            for col in colunas:
                col_lower = str(col).lower()
                if col_lower in ['latitude', 'lat', 'lat_dec', 'lat_y', 'y']:
                    self.menu_lat.set(col)
                if col_lower in ['longitude', 'lon', 'long', 'lon_dec', 'lon_x', 'x']:
                    self.menu_lon.set(col)
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler o arquivo:\n{str(e)}")

    def formatar_gms(self, valor):
        """Converte um valor decimal em Graus, Minutos e Segundos."""
        decimal = abs(valor)
        g = int(decimal)
        m = int((decimal - g) * 60)
        s = round(((decimal - g) * 60 - m) * 60, 4)
        # Se for no hemisfério Sul ou Oeste (valores originais negativos), o Grau é negativo
        grau_final = -g if valor < 0 else g
        return grau_final, m, s

    def converter(self):
        if self.df_global is None:
            messagebox.showwarning("Aviso", "Por favor, carregue uma planilha primeiro!")
            return
        
        col_lat = self.menu_lat.get()
        col_lon = self.menu_lon.get()
        
        if col_lat == "Selecione..." or col_lon == "Selecione...":
            messagebox.showwarning("Aviso", "Selecione as colunas de Latitude e Longitude!")
            return

        self.txt_saida.delete("1.0", "end")
        header = "Lat_G\tLat_M\tLat_S\tLon_G\tLon_M\tLon_S\n"
        self.txt_saida.insert("end", header)

        linhas_convertidas = []
        for _, row in self.df_global.iterrows():
            try:
                val_lat = row[col_lat]
                val_lon = row[col_lon]
                
                if pd.isna(val_lat) or pd.isna(val_lon):
                    continue
                    
                lat_g, lat_m, lat_s = self.formatar_gms(float(val_lat))
                lon_g, lon_m, lon_s = self.formatar_gms(float(val_lon))
                
                linha = f"{lat_g}\t{lat_m}\t{lat_s}\t{lon_g}\t{lon_m}\t{lon_s}\n"
                self.txt_saida.insert("end", linha)
                linhas_convertidas.append(linha)
            except Exception:
                continue

        if linhas_convertidas:
            # Copia real para a Área de Transferência
            conteudo = self.txt_saida.get("1.0", "end-1c")
            self.clipboard_clear()
            self.clipboard_append(conteudo)
            self.update()
            messagebox.showinfo(
                "Sucesso", 
                "Conversão concluída!\nO resultado foi copiado automaticamente para a área de transferência."
            )
        else:
            messagebox.showwarning("Aviso", "Nenhum dado válido de coordenada pôde ser convertido.")

    def gerar_kmz(self):
        if self.df_global is None:
            messagebox.showwarning("Aviso", "Por favor, carregue uma planilha primeiro!")
            return
        
        col_lat = self.menu_lat.get()
        col_lon = self.menu_lon.get()
        
        if col_lat == "Selecione..." or col_lon == "Selecione...":
            messagebox.showwarning("Aviso", "Selecione as colunas de Latitude e Longitude primeiro!")
            return

        # Procura coluna de nome/código para identificar os pontos
        colunas_candidatas = ['nome', 'name', 'ponto', 'point', 'id', 'identificador', 'codigo', 'código', 'local']
        col_nome = None
        for c in self.df_global.columns:
            if str(c).lower() in colunas_candidatas:
                col_nome = c
                break

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
        
        pontos_adicionados = 0
        for index, row in self.df_global.iterrows():
            try:
                val_lat = row[col_lat]
                val_lon = row[col_lon]
                
                if pd.isna(val_lat) or pd.isna(val_lon):
                    continue

                lat_bruta = float(val_lat)
                lon_bruta = float(val_lon)
                
                # Garante coordenadas negativas (Brasil: Hemisfério Sul e Oeste)
                lat_corrigida = -abs(lat_bruta)
                lon_corrigida = -abs(lon_bruta)
                
                # Define nome do ponto inteligente
                nome_ponto = str(row[col_nome]) if col_nome else f"Ponto {index + 1}"
                
                # Cria a descrição com tabela contendo os dados da planilha
                desc_html = "<table border='1' style='border-collapse: collapse; font-family: sans-serif; font-size: 11px;'>\n"
                for col in self.df_global.columns:
                    desc_html += f"  <tr><th>{col}</th><td>{row[col]}</td></tr>\n"
                desc_html += "</table>"

                placemark = f"""    <Placemark>
      <name>{nome_ponto}</name>
      <description><![CDATA[{desc_html}]]></description>
      <styleUrl>#pontoEstilo</styleUrl>
      <Point>
        <coordinates>{lon_corrigida},{lat_corrigida},0</coordinates>
      </Point>
    </Placemark>
"""
                kml_content += placemark
                pontos_adicionados += 1
            except Exception:
                continue
                
        kml_content += "  </Document>\n</kml>\n"
        
        if pontos_adicionados == 0:
            messagebox.showwarning("Aviso", "Nenhum ponto válido encontrado para gerar o KMZ.")
            return

        caminho_salvar = filedialog.asksaveasfilename(
            defaultextension=".kmz", 
            filetypes=[("Arquivo KMZ (Google Earth)", "*.kmz")], 
            initialfile="Pontos_SinaFlor.kmz",
            title="Salvar arquivo KMZ"
        )
        if not caminho_salvar: 
            return
        
        try:
            with zipfile.ZipFile(caminho_salvar, 'w', zipfile.ZIP_DEFLATED) as kmz:
                kmz.writestr("doc.kml", kml_content)
            
            messagebox.showinfo("Sucesso", f"Arquivo KMZ gerado com sucesso:\n{os.path.basename(caminho_salvar)}")
            os.startfile(caminho_salvar)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o arquivo KMZ:\n{str(e)}")
