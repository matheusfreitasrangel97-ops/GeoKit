@echo off
echo =======================================================
echo Compilador GeoKit (Distribuicao Executavel Unico)
echo =======================================================
echo.

echo [1/3] Limpando arquivos de builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GeoKit.spec del /q GeoKit.spec
echo.

echo [2/3] Iniciando empacotamento baseado no build_spec.py...
echo Isso pode levar alguns minutos. Aguarde...
call "%USERPROFILE%\AppData\Local\miniconda3\python.exe" build_spec.py
echo.

echo [3/3] Processo finalizado!
echo =======================================================
echo O seu aplicativo pronto para uso esta localizado na pasta:
echo %CD%\dist
echo.
echo Para abrir o programa, basta executar o arquivo:
echo %CD%\dist\GeoKit.exe
echo =======================================================
pause
