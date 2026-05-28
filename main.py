import sys
import customtkinter as ctk
from geokit.app import GeoKitApp

# Configuração padrão do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def main():
    try:
        app = GeoKitApp()
        app.mainloop()
    except Exception as e:
        # Se falhar ao abrir a janela customtkinter (ex: falha de temas), tenta alertar via tkinter básico
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Erro de Inicialização", 
                f"Ocorreu um erro fatal ao iniciar o GeoKit:\n\n{str(e)}\n\n"
                "Verifique se o seu ambiente Python possui suporte a interfaces gráficas (Tcl/Tk)."
            )
        except Exception:
            print(f"Erro fatal ao iniciar GeoKit: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
