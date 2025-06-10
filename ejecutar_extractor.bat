@echo off
REM -- Script para ejecutar el extractor de datos de Facebook --

REM Paso 1: Cambiar al directorio del script
REM La variable %~dp0 es una magia que significa "la carpeta donde este archivo .bat se encuentra".
REM Esto hace que el script funcione sin importar a dónde muevas la carpeta del proyecto.
cd /d "%~dp0"

echo.
echo =============================================================
echo      INICIANDO EXTRACTOR DE DATOS DE FACEBOOK ADS
echo =============================================================
echo.
echo Directorio actual: %cd%
echo.

REM Paso 2: Activar el entorno virtual de Python
echo Activando entorno virtual (venv)...
call .\venv\Scripts\activate.bat

REM Comprobar si la activación fue exitosa
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo activar el entorno virtual.
    echo Asegurate de que la carpeta 'venv' existe en este directorio.
    pause
    exit /b
)

echo Entorno virtual activado.
echo.

REM Paso 3: Ejecutar el script de Python
echo Ejecutando el script 'extractor.py'...
echo ---------------------------------------
python extractor.py
echo ---------------------------------------
echo.

REM Paso 4: Finalización del script
echo =============================================================
echo      PROCESO DE EXTRACCION FINALIZADO
echo =============================================================
echo Los archivos CSV han sido actualizados.
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause