import os
import geopandas as gpd
import customtkinter as ctk
from tkinter import filedialog, messagebox

class FrameFepam(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.arquivos_para_processar = []
        self.caminho_saida = ""

        # Título
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="Reprojetor SIRGAS 2000 - Norma FEPAM 07/2015", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # Descrição da Norma
        self.lbl_desc = ctk.CTkLabel(
            self,
            text="Esta ferramenta padroniza arquivos geográficos (.shp, .gpkg) para o Sistema de Referência Geocêntrico para as Américas (SIRGAS 2000) no formato Geográfico (Graus Decimais, EPSG:4674), atendendo às especificações da FEPAM.",
            font=ctk.CTkFont(size=12),
            wraplength=700,
            text_color="gray"
        )
        self.lbl_desc.pack(pady=(0, 15))

        # Frame de Entrada
        self.frame_entrada = ctk.CTkFrame(self)
        self.frame_entrada.pack(pady=5, fill="x", padx=40)

        self.btn_carregar = ctk.CTkButton(
            self.frame_entrada, 
            text="SELECIONAR ARQUIVOS (.SHP / .GPKG)", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            command=self.selecionar_multiplos_arquivos, 
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.btn_carregar.pack(pady=12, padx=20, fill="x")

        # Relatório de CRS
        self.lbl_titulo_txt = ctk.CTkLabel(
            self, 
            text="Relatório de Diagnóstico de CRS:", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="gray"
        )
        self.lbl_titulo_txt.pack(anchor="w", padx=45, pady=(10, 2))

        self.txt_relatorio = ctk.CTkTextbox(
            self, 
            height=160, 
            activate_scrollbars=True, 
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.txt_relatorio.pack(fill="x", padx=40, pady=2)
        self.txt_relatorio.insert("0.0", "Nenhum arquivo carregado para análise.")
        self.txt_relatorio.tag_config("erro_vermelho", foreground="#E53935")
        self.txt_relatorio.tag_config("ok_verde", foreground="#2E7D32")
        self.txt_relatorio.tag_config("aviso_amarelo", foreground="#E65100")
        self.txt_relatorio.configure(state="disabled")

        # Frame de Saída
        self.frame_saida = ctk.CTkFrame(self)
        self.frame_saida.pack(pady=15, fill="x", padx=40)

        self.btn_destino = ctk.CTkButton(
            self.frame_saida, 
            text="Definir Pasta de Destino", 
            command=self.selecionar_destino
        )
        self.btn_destino.pack(pady=10)

        self.lbl_status_saida = ctk.CTkLabel(self, text="Nenhum destino definido.", text_color="gray")
        self.lbl_status_saida.pack(pady=3)

        # Botão Executar
        self.btn_processar = ctk.CTkButton(
            self, 
            text="EXECUTAR REPROJEÇÃO PARA SIRGAS 2000", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            command=self.processar_dados, 
            height=45
        )
        self.btn_processar.pack(pady=15, ipadx=20)

    def selecionar_multiplos_arquivos(self):
        tipos = [
            ("Arquivos Geográficos", "*.shp *.gpkg"), 
            ("Shapefiles ESRI", "*.shp"), 
            ("GeoPackage", "*.gpkg")
        ]
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos geográficos para análise", 
            filetypes=tipos
        )
        if not arquivos: 
            return

        self.arquivos_para_processar = list(arquivos)
        self.txt_relatorio.configure(state="normal")
        self.txt_relatorio.delete("0.0", "end")
        self.txt_relatorio.insert(
            "end", 
            f"TOTAL DE ARQUIVOS CARREGADOS: {len(self.arquivos_para_processar)}\n{'-'*75}\n"
        )

        for i, caminho in enumerate(self.arquivos_para_processar, 1):
            nome_arq = os.path.basename(caminho)
            try:
                gdf_schema = gpd.read_file(caminho, rows=1)
                self.txt_relatorio.insert("end", f"[{i}] Arquivo: {nome_arq}\n")
                
                if gdf_schema.crs is None:
                    self.txt_relatorio.insert("end", "    Projeção atual: Sem CRS definido\n    Situação: ")
                    self.txt_relatorio.insert("end", "Incompatível (Sem Projeção - Requer definição manual)\n\n", "erro_vermelho")
                else:
                    epsg = gdf_schema.crs.to_epsg()
                    crs_name = gdf_schema.crs.name
                    
                    self.txt_relatorio.insert("end", f"    Projeção atual: {crs_name} (EPSG:{epsg if epsg else 'Não identificado'})\n    Situação: ")
                    
                    if epsg == 4674:
                        self.txt_relatorio.insert("end", "Em conformidade com a Norma 07/2015 FEPAM (SIRGAS 2000)\n\n", "ok_verde")
                    else:
                        self.txt_relatorio.insert("end", "Incompatível (Será reprojetado para SIRGAS 2000)\n\n", "aviso_amarelo")
            except Exception as e:
                self.txt_relatorio.insert(
                    "end", 
                    f"[{i}] Arquivo: {nome_arq}\n    Erro ao ler metadados: {str(e)}\n\n", 
                    "erro_vermelho"
                )

        self.txt_relatorio.configure(state="disabled")

    def selecionar_destino(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta onde salvar os arquivos corrigidos")
        if pasta:
            self.caminho_saida = pasta
            self.lbl_status_saida.configure(text=f"Pasta de Destino: {pasta}", text_color="#1f538d")

    def processar_dados(self):
        if not self.arquivos_para_processar:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo de entrada primeiro.")
            return
        if not self.caminho_saida:
            messagebox.showwarning("Aviso", "Defina a pasta de destino dos arquivos convertidos.")
            return

        reprojecoes = 0
        mantidos = 0
        erros = 0
        
        pasta_final = os.path.join(self.caminho_saida, "dados_sirgas2000")
        os.makedirs(pasta_final, exist_ok=True)

        for arquivo_path in self.arquivos_para_processar:
            nome_arq = os.path.basename(arquivo_path)
            try:
                gdf = gpd.read_file(arquivo_path)
                
                if gdf.crs is None:
                    # Não podemos reprojetar sem saber a origem
                    self.txt_relatorio.configure(state="normal")
                    self.txt_relatorio.insert("end", f"⚠️ Falha no arquivo {nome_arq}: Não possui CRS definido para reprojeção.\n", "erro_vermelho")
                    self.txt_relatorio.configure(state="disabled")
                    erros += 1
                    continue

                # Cria o nome final preservando a extensão
                ext = os.path.splitext(nome_arq)[1]
                nome_base = os.path.splitext(nome_arq)[0]
                novo_nome = f"sirgas_{nome_base}{ext}"
                caminho_final = os.path.join(pasta_final, novo_nome)

                # Verifica se já está em SIRGAS 2000 (EPSG:4674)
                epsg_code = gdf.crs.to_epsg()
                
                if epsg_code == 4674:
                    # Apenas salva no destino
                    gdf.to_file(caminho_final)
                    mantidos += 1
                else:
                    # Reprojeta para SIRGAS 2000 geográfico (EPSG:4674)
                    gdf_sirgas = gdf.to_crs(epsg=4674)
                    gdf_sirgas.to_file(caminho_final)
                    reprojecoes += 1
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao processar o arquivo {nome_arq}:\n{str(e)}")
                erros += 1
                continue

        # Mensagem final resumida
        mensagem = f"Processamento concluído com sucesso!\n\nSalvos em: {pasta_final}\n"
        mensagem += f"• Arquivos reprojetados para SIRGAS 2000 (EPSG:4674): {reprojecoes}\n"
        mensagem += f"• Arquivos copiados (já estavam em conformidade): {mantidos}"
        if erros > 0:
            mensagem += f"\n• Arquivos com erro (não processados): {erros}"
            
        messagebox.showinfo("Sucesso", mensagem)
