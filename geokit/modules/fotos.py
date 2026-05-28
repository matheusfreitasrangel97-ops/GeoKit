import os
import base64
import zipfile
from io import BytesIO
import customtkinter as ctk
from tkinter import filedialog, messagebox
from exif import Image as ExifImage
from PIL import Image as PILImage, ImageOps
import simplekml

class FrameFotosKMZ(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.caminhos_fotos = []
        self.caminho_saida = ""

        # Título
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="Conversor de Fotos com GPS para KMZ", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # Descrição
        self.lbl_desc = ctk.CTkLabel(
            self,
            text="Gere mapas interativos contendo fotos no local exato onde foram tiradas. O sistema lê os metadados de GPS das imagens e cria popups elegantes.",
            font=ctk.CTkFont(size=12),
            wraplength=700,
            text_color="gray"
        )
        self.lbl_desc.pack(pady=(0, 15))

        # Frame Entrada
        self.frame_entrada = ctk.CTkFrame(self)
        self.frame_entrada.pack(pady=10, padx=20, fill="x")

        self.lbl_entrada = ctk.CTkLabel(self.frame_entrada, text="Fotos de Origem:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_entrada.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.txt_entrada = ctk.CTkEntry(self.frame_entrada, width=450, placeholder_text="Nenhum arquivo selecionado...")
        self.txt_entrada.grid(row=1, column=0, padx=10, pady=(0, 12), sticky="we")

        self.btn_selecionar = ctk.CTkButton(
            self.frame_entrada, 
            text="Procurar Fotos...", 
            width=120, 
            command=self.selecionar_fotos
        )
        self.btn_selecionar.grid(row=1, column=1, padx=10, pady=(0, 12))

        # Frame Saída
        self.frame_saida = ctk.CTkFrame(self)
        self.frame_saida.pack(pady=10, padx=20, fill="x")

        self.lbl_saida_tit = ctk.CTkLabel(self.frame_saida, text="Destino do Arquivo KMZ:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_saida_tit.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.txt_saida = ctk.CTkEntry(self.frame_saida, width=450, placeholder_text="Defina o local e nome para salvar o KMZ...")
        self.txt_saida.grid(row=1, column=0, padx=10, pady=(0, 12), sticky="we")

        self.btn_saida = ctk.CTkButton(
            self.frame_saida, 
            text="Definir Destino...", 
            width=120, 
            command=self.definir_saida
        )
        self.btn_saida.grid(row=1, column=1, padx=10, pady=(0, 12))

        # Frame Configurações
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(pady=10, padx=20, fill="x")

        self.lbl_opcao_tamanho = ctk.CTkLabel(self.frame_config, text="Dimensão / Qualidade das Fotos no Mapa:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_opcao_tamanho.pack(side="left", padx=15, pady=12)
        
        self.combo_tamanho = ctk.CTkComboBox(self.frame_config, width=280, values=[
            "Compacto (300px) - Arquivo leve", 
            "Médio (600px) - Recomendado", 
            "Grande (1200px) - Alta Definição", 
            "Original - Mantém resolução padrão"
        ])
        self.combo_tamanho.set("Médio (600px) - Recomendado")
        self.combo_tamanho.pack(side="right", padx=15, pady=12)

        # Barra de Progresso
        self.frame_progresso = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_progresso.pack(pady=10, padx=20, fill="x")

        self.lbl_status_processo = ctk.CTkLabel(
            self.frame_progresso, 
            text="Aguardando definições para iniciar...", 
            font=ctk.CTkFont(size=12, slant="italic"), 
            text_color="gray"
        )
        self.lbl_status_processo.pack(pady=2)

        self.progress_bar = ctk.CTkProgressBar(self.frame_progresso, width=540)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(
            self, 
            text="GERAR ARQUIVO KMZ", 
            command=self.validar_e_gerar, 
            fg_color="#2b712b", 
            hover_color="#1e521e", 
            height=48, 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_gerar.pack(pady=15)

    def converter_para_decimal(self, coords, ref):
        """Converte coordenadas EXIF (Graus, Minutos, Segundos) para Decimal."""
        try:
            d = float(coords[0])
            m = float(coords[1])
            s = float(coords[2])
            decimal = d + (m / 60.0) + (s / 3600.0)
            if ref in ['S', 'W']: 
                decimal = -decimal
            return decimal
        except Exception:
            return None

    def selecionar_fotos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione as fotos (JPEG)", 
            filetypes=[("Imagens JPEG", "*.jpg *.jpeg"), ("Todos os Arquivos", "*.*")]
        )
        if arquivos:
            self.caminhos_fotos = list(arquivos)
            self.txt_entrada.delete(0, "end")
            self.txt_entrada.insert(0, f"{len(self.caminhos_fotos)} fotos selecionadas em: {os.path.dirname(self.caminhos_fotos[0])}")
            self.lbl_status_processo.configure(text=f"📂 {len(self.caminhos_fotos)} foto(s) carregada(s).", text_color="#1f538d")

    def definir_saida(self):
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".kmz", 
            filetypes=[("Arquivo Google Earth KMZ", "*.kmz")],
            title="Salvar arquivo KMZ"
        )
        if arquivo:
            self.caminho_saida = arquivo
            self.txt_saida.delete(0, "end")
            self.txt_saida.insert(0, self.caminho_saida)

    def validar_e_gerar(self):
        if not self.caminhos_fotos:
            messagebox.showwarning("Atenção", "Selecione as fotos que deseja converter.")
            return
        if not self.caminho_saida:
            messagebox.showwarning("Atenção", "Defina o destino do arquivo KMZ.")
            return
        self.processar_conversao()

    def processar_conversao(self):
        self.btn_gerar.configure(state="disabled")
        escolha = self.combo_tamanho.get()
        tamanho_max = 300 if "Compacto" in escolha else 600 if "Médio" in escolha else 1200
        largura_balao = 350 if "Compacto" in escolha else 600 if "Médio" in escolha else 750
        manter_original = "Original" in escolha

        dados_fotos = []
        fotos_sem_gps = []
        fotos_erro = []
        total = len(self.caminhos_fotos)

        for index, caminho in enumerate(self.caminhos_fotos, start=1):
            self.progress_bar.set(index / total)
            self.lbl_status_processo.configure(text=f"Processando ({index}/{total}): {os.path.basename(caminho)}")
            self.update_idletasks()

            nome_foto = os.path.basename(caminho)
            try:
                with open(caminho, 'rb') as f:
                    img_exif = ExifImage(f)
                    
                    if img_exif.has_exif and hasattr(img_exif, 'gps_latitude') and hasattr(img_exif, 'gps_longitude'):
                        lat = self.converter_para_decimal(img_exif.gps_latitude, img_exif.gps_latitude_ref)
                        lon = self.converter_para_decimal(img_exif.gps_longitude, img_exif.gps_longitude_ref)
                        
                        if lat is None or lon is None:
                            fotos_sem_gps.append(nome_foto)
                            continue
                        
                        # Processa a imagem para salvar no KMZ
                        if manter_original:
                            f.seek(0)
                            bytes_finais = f.read()
                        else:
                            with PILImage.open(caminho) as pil_img:
                                # Corrige a orientação EXIF automática
                                pil_img = ImageOps.exif_transpose(pil_img)
                                pil_img.thumbnail((tamanho_max, tamanho_max))
                                buffer = BytesIO()
                                pil_img.save(buffer, format="JPEG", quality=82)
                                bytes_finais = buffer.getvalue()

                        # Identificador interno único no ZIP
                        nome_interno = f"imagens/foto_{index}_{nome_foto}"
                        dados_fotos.append({
                            'nome': nome_foto, 
                            'nome_interno': nome_interno,
                            'lat': lat, 
                            'lon': lon, 
                            'bytes': bytes_finais
                        })
                    else:
                        fotos_sem_gps.append(nome_foto)
            except Exception as e:
                print(f"Erro ao ler imagem {nome_foto}: {e}")
                fotos_erro.append(nome_foto)

        # Montagem do arquivo KMZ
        if dados_fotos:
            kml = simplekml.Kml()
            # Adiciona estilo personalizado para o ícone de câmera
            style = kml.newstyle(id="iconeCamera")
            style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/camera.png"
            style.iconstyle.scale = 1.2

            for foto in dados_fotos:
                pnt = kml.newpoint(name=foto['nome'], coords=[(foto['lon'], foto['lat'])])
                pnt.style = style
                
                # HTML elegante e otimizado referenciando o arquivo relativo dentro do ZIP do KMZ
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

            try:
                # Escreve o ZIP real
                with zipfile.ZipFile(self.caminho_saida, 'w', zipfile.ZIP_DEFLATED) as kmz:
                    # 1. Grava o arquivo de mapa doc.kml
                    kmz.writestr("doc.kml", kml.kml())
                    # 2. Grava todas as fotos correspondentes
                    for foto in dados_fotos:
                        kmz.writestr(foto['nome_interno'], foto['bytes'])

                self.lbl_status_processo.configure(text="✅ Processamento Concluído!", text_color="green")
                
                # Relatório final
                res_mensagem = f"Arquivo KMZ gerado com sucesso!\n• Fotos no mapa: {len(dados_fotos)}"
                if fotos_sem_gps:
                    res_mensagem += f"\n• Ignoradas (Sem GPS): {len(fotos_sem_gps)}"
                if fotos_erro:
                    res_mensagem += f"\n• Erros de leitura: {len(fotos_erro)}"
                
                messagebox.showinfo("Sucesso", res_mensagem)
                
                # Exibe detalhes de fotos sem GPS se necessário
                if fotos_sem_gps:
                    lista_sem_gps = "\n".join(fotos_sem_gps[:15])
                    if len(fotos_sem_gps) > 15:
                        lista_sem_gps += "\n... e outras."
                    messagebox.showwarning(
                        "Fotos sem Georreferenciamento", 
                        f"As seguintes fotos foram ignoradas por não conter metadados de GPS:\n\n{lista_sem_gps}"
                    )

                os.startfile(self.caminho_saida)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar ou salvar o arquivo KMZ:\n{str(e)}")
        else:
            self.lbl_status_processo.configure(text="❌ Falha na geração do KMZ.", text_color="red")
            messagebox.showwarning("Aviso", "Nenhuma das fotos selecionadas continha coordenadas GPS válidas.")
        
        self.btn_gerar.configure(state="normal")
        self.progress_bar.set(0)
