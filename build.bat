@echo off
echo =======================================================
echo Compilador GeoKit (Distribuicao Standalone)
echo =======================================================
echo.

echo [1/3] Limpando arquivos de builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

echo [2/3] Iniciando empacotamento com PyInstaller...
echo Isso pode levar alguns minutos. Aguarde...
call "%USERPROFILE%\AppData\Local\miniconda3\python.exe" -m PyInstaller --noconfirm --onedir --windowed --name "GeoKit" main.py
echo.

echo [3/3] Processo finalizado!
echo =======================================================
echo O seu aplicativo pronto para uso esta localizado na pasta:
echo %CD%\dist\GeoKit
echo.
echo Para abrir o programa, basta entrar nessa pasta e dar um
echo clique duplo no arquivo GeoKit.exe
echo =======================================================
pause
