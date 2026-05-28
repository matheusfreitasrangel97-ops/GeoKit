import os
import sys
import time
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

from geokit import __version__
from geokit.updater import check_for_updates
from geokit.modules.sinaflor import FrameSinaFlor
from geokit.modules.fepam import FrameFepam
from geokit.modules.fotos import FrameFotosKMZ

class UpdateProgressWindow(ctk.CTkToplevel):
    def __init__(self, parent, download_url):
        super().__init__(parent)
        self.title("Atualizando GeoKit")
        self.geometry("420x200")
        self.resizable(False, False)
        self.transient(parent)
        
        # Faz com que a janela bloqueie a principal (modal)
        self.grab_set()
        
        # Centraliza a janela com base na janela principal
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 210
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 100
        self.geometry(f"420x200+{x}+{y}")
        
        self.label_status = ctk.CTkLabel(
            self, 
            text="Preparando download...", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_status.pack(pady=(25, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=340)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=10)
        
        self.label_percent = ctk.CTkLabel(self, text="0% (0.0 MB / 0.0 MB)", text_color="gray")
        self.label_percent.pack(pady=5)
        
        # Inicia o download assíncrono
        from geokit.updater import download_and_install_update
        download_and_install_update(
            download_url,
            self.on_progress,
            self.on_complete,
            self.on_error
        )
        
    def on_progress(self, percent, downloaded_mb, total_mb):
        self.after(0, lambda: self._update_ui(percent, downloaded_mb, total_mb))
        
    def _update_ui(self, percent, downloaded_mb, total_mb):
        if percent == -1:
            self.label_status.configure(text="Baixando atualização...")
            self.label_percent.configure(text=f"{downloaded_mb:.1f} MB baixados")
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
        else:
            self.label_status.configure(text="Baixando arquivos da nova versão...")
            self.progress_bar.set(percent)
            self.label_percent.configure(text=f"{int(percent * 100)}% ({downloaded_mb:.1f} MB / {total_mb:.1f} MB)")
            
    def on_complete(self):
        self.after(0, self._finalize)
        
    def _finalize(self):
        self.label_status.configure(text="Download concluído! Instalando...", text_color="green")
        self.update_idletasks()
        # Aguarda 1 segundo antes de disparar o atualizador e fechar o app
        time.sleep(1.0)
        self.destroy()
        sys.exit(0)
        
    def on_error(self, err_msg):
        self.after(0, lambda: self._show_error(err_msg))
        
    def _show_error(self, err_msg):
        messagebox.showerror(
            "Erro na Atualização", 
            f"Não foi possível baixar ou instalar a atualização:\n\n{err_msg}"
        )
        self.destroy()


class GeoKitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title(f"GeoKit v{__version__} - Caixa de Ferramentas Geográficas")
        self.geometry("1000x720")
        self.minsize(950, 680)

        # Configura o Grid da Janela (1 linha, 2 colunas: Menu e Área Principal)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---------------- MENU LATERAL ----------------
        self.frame_menu = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(6, weight=1) # Empurra rodapé para baixo

        # Logo / Título do App
        self.logo_label = ctk.CTkLabel(
            self.frame_menu, 
            text="GeoKit", 
            font=ctk.CTkFont(size=26, weight="bold", family="Outfit")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        self.sub_logo_label = ctk.CTkLabel(
            self.frame_menu, 
            text="Ferramentas Geográficas", 
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.sub_logo_label.grid(row=1, column=0, padx=20, pady=(0, 25))

        # Botões de Navegação
        self.btn_sinaflor = ctk.CTkButton(
            self.frame_menu, 
            text="🌲  SinaFlor (DMS)", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_sinaflor
        )
        self.btn_sinaflor.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self.btn_fepam = ctk.CTkButton(
            self.frame_menu, 
            text="📋  Norma FEPAM (CRS)", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_fepam
        )
        self.btn_fepam.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        self.btn_fotos = ctk.CTkButton(
            self.frame_menu, 
            text="📸  Fotos -> KMZ", 
            height=44, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w",
            text_color=["#2b2b2b", "#f5f5f5"],
            command=self.mostrar_fotos
        )
        self.btn_fotos.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        # Seletor de Tema
        self.theme_label = ctk.CTkLabel(
            self.frame_menu, 
            text="Aparência do Sistema:", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        )
        self.theme_label.grid(row=7, column=0, padx=20, pady=(10, 2), sticky="w")
        
        self.theme_menu = ctk.CTkOptionMenu(
            self.frame_menu, 
            values=["Sistema", "Claro", "Escuro"],
            command=self.alterar_tema,
            height=28
        )
        self.theme_menu.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.theme_menu.set("Sistema")

        # Créditos no final do menu
        self.lbl_creditos = ctk.CTkLabel(
            self.frame_menu, 
            text="Desenvolvido por:\nMatheus Rangel\n(51) 99790-3841", 
            font=ctk.CTkFont(size=11, slant="italic"), 
            text_color="gray"
        )
        self.lbl_creditos.grid(row=9, column=0, padx=20, pady=(10, 25), sticky="s")

        # ---------------- ÁREAS DE CONTEÚDO ----------------
        # Container da direita com margens internas
        self.frame_container = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        # Instanciação dos Frames
        self.frame_sinaflor_view = FrameSinaFlor(self.frame_container)
        self.frame_fepam_view = FrameFepam(self.frame_container)
        self.frame_fotos_view = FrameFotosKMZ(self.frame_container)

        # Inicia mostrando o SinaFlor por padrão
        self.mostrar_sinaflor()

        # Iniciar verificador de atualizações em segundo plano
        self.after(2000, self.verificar_atualizacoes)

    # --- LÓGICA DE NAVEGAÇÃO ---
    def esconder_tudo(self):
        self.frame_sinaflor_view.grid_forget()
        self.frame_fepam_view.grid_forget()
        self.frame_fotos_view.grid_forget()
        
        # Reseta os botões para transparentes (inativos) com cor de texto adaptativa
        self.btn_sinaflor.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])
        self.btn_fepam.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])
        self.btn_fotos.configure(fg_color="transparent", text_color=["#2b2b2b", "#f5f5f5"])

    def destacar_botao(self, botao):
        # Destaca o botão ativo com a cor azul padrão do tema e texto branco
        botao.configure(fg_color=["#3a7ebf", "#1f538d"], text_color="#ffffff")

    def mostrar_sinaflor(self):
        self.esconder_tudo()
        self.frame_sinaflor_view.grid(row=0, column=0, sticky="nsew")
        self.destacar_botao(self.btn_sinaflor)

    def mostrar_fepam(self):
        self.esconder_tudo()
        self.frame_fepam_view.grid(row=0, column=0, sticky="nsew")
        self.destacar_botao(self.btn_fepam)

    def mostrar_fotos(self):
        self.esconder_tudo()
        self.frame_fotos_view.grid(row=0, column=0, sticky="nsew")
        self.destacar_botao(self.btn_fotos)

    def alterar_tema(self, tema_selecionado):
        if tema_selecionado == "Claro":
            ctk.set_appearance_mode("Light")
        elif tema_selecionado == "Escuro":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System")

    # --- ATUALIZADOR ASSÍNCRONO ---
    def verificar_atualizacoes(self):
        check_for_updates(__version__, self.on_update_found)

    def on_update_found(self, remote_version, url, notes):
        # Agenda a exibição do popup na thread principal do CustomTkinter
        self.after(0, lambda: self.exibir_popup_atualizacao(remote_version, url, notes))

    def exibir_popup_atualizacao(self, remote_version, url, notes):
        mensagem = f"Uma nova versão ({remote_version}) do GeoKit está disponível!\n"
        if notes:
            mensagem += f"\nNotas de atualização:\n{notes}\n"
        mensagem += "\nDeseja baixar e instalar esta nova versão de forma automática?"
        
        resposta = messagebox.askyesno("Atualização Disponível", mensagem, icon="info")
        if resposta:
            UpdateProgressWindow(self, url)
