import os
import sys
import json
import shutil
import zipfile
import tempfile
import subprocess
import urllib.request
import urllib.error
import threading
from distutils.version import LooseVersion

VERSION_URL = "https://raw.githubusercontent.com/matheusfreitasrangel97-ops/GeoKit/main/version.json"

def check_for_updates(current_version: str, callback):
    """
    Checks for updates in a background thread.
    If a new version is available, calls the callback with (new_version, url, notes) in the main thread.
    """
    def thread_target():
        try:
            req = urllib.request.Request(
                VERSION_URL, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoKitUpdater'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                remote_version = data.get("version")
                update_url = data.get("url", "https://github.com/matheusfreitasrangel97-ops/GeoKit")
                notes = data.get("notes", "")

                if remote_version:
                    try:
                        is_newer = LooseVersion(remote_version) > LooseVersion(current_version)
                    except Exception:
                        is_newer = tuple(map(int, remote_version.split('.'))) > tuple(map(int, current_version.split('.')))

                    if is_newer:
                        callback(remote_version, update_url, notes)
        except Exception:
            pass

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()


def download_and_install_update(download_url: str, progress_callback, completion_callback, error_callback):
    """
    Downloads the update zip file in a background thread, reports progress,
    unzips it, generates the replacement batch file, spawns it, and triggers completion.
    """
    def thread_target():
        try:
            req = urllib.request.Request(
                download_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoKitUpdater'}
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                content_length = response.getheader('Content-Length')
                total_size = int(content_length) if content_length else 0
                
                downloaded_size = 0
                block_size = 16384 # 16KB blocks
                
                temp_dir = tempfile.gettempdir()
                zip_path = os.path.join(temp_dir, "GeoKit_update.zip")
                
                with open(zip_path, 'wb') as f:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        f.write(buffer)
                        downloaded_size += len(buffer)
                        
                        if total_size > 0:
                            percent = downloaded_size / total_size
                            progress_callback(percent, downloaded_size / (1024 * 1024), total_size / (1024 * 1024))
                        else:
                            progress_callback(-1, downloaded_size / (1024 * 1024), 0.0)
                
                # Extraction
                extract_dir = os.path.join(temp_dir, "GeoKit_extracted")
                if os.path.exists(extract_dir):
                    shutil.rmtree(extract_dir)
                os.makedirs(extract_dir, exist_ok=True)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                # Check running environment (Python source vs Compiled Executable)
                if getattr(sys, 'frozen', False):
                    app_executable = sys.executable
                    app_dir = os.path.dirname(app_executable)
                    exe_name = os.path.basename(app_executable)
                    is_frozen = True
                else:
                    app_executable = sys.executable
                    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                    exe_name = None
                    is_frozen = False
                
                # Generate installation batch script
                bat_path = os.path.join(temp_dir, "geokit_install.bat")
                
                with open(bat_path, 'w', encoding='utf-8') as bat_file:
                    bat_file.write("@echo off\n")
                    bat_file.write("chcp 65001 > nul\n")
                    bat_file.write("echo =======================================================\n")
                    bat_file.write("echo Instalando Atualização do GeoKit...\n")
                    bat_file.write("echo =======================================================\n")
                    bat_file.write("echo Aguardando o GeoKit fechar completamente...\n")
                    
                    if is_frozen and exe_name:
                        # Process checking loop for compiled EXE
                        bat_file.write(f":wait_loop\n")
                        bat_file.write(f"tasklist /fi \"IMAGENAME eq {exe_name}\" 2>NUL | find /I /N \"{exe_name}\" >NUL\n")
                        bat_file.write(f"if \"%ERRORLEVEL%\"==\"0\" (\n")
                        bat_file.write(f"    timeout /t 1 /nobreak >nul\n")
                        bat_file.write(f"    goto wait_loop\n")
                        bat_file.write(f")\n")
                    else:
                        bat_file.write("timeout /t 2 /nobreak > nul\n")
                        
                    bat_file.write("echo Copiando novos arquivos...\n")
                    # Overwrite and preserve structure
                    bat_file.write(f"xcopy /y /e /s /i \"{extract_dir}\\*.*\" \"{app_dir}\\\" >nul\n")
                    
                    bat_file.write("echo Reiniciando o GeoKit...\n")
                    if is_frozen:
                        bat_file.write(f"start \"\" \"{app_executable}\"\n")
                    else:
                        main_py_path = os.path.join(app_dir, "main.py")
                        bat_file.write(f"start \"\" \"{app_executable}\" \"{main_py_path}\"\n")
                        
                    bat_file.write("echo Limpando arquivos temporarios...\n")
                    bat_file.write(f"rd /s /q \"{extract_dir}\"\n")
                    bat_file.write(f"del /q \"{zip_path}\"\n")
                    bat_file.write("echo Concluido com sucesso!\n")
                    bat_file.write("del \"%~f0\"\n")
                
                # Spawns batch process
                subprocess.Popen(
                    [bat_path], 
                    shell=True, 
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                
                completion_callback()
                
        except Exception as e:
            error_callback(str(e))

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()
