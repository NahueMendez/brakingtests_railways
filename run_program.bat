@echo off
echo Verificando e instalando librerías necesarias...

REM Obtiene la ruta actual donde está el archivo .bat
set "ruta_actual=%~dp0"

REM Verifica si numpy está instalado, si no, lo instala
pip show numpy >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando numpy...
    pip install numpy >nul 2>&1
)

REM Verifica si pandas está instalado, si no, lo instala
pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pandas...
    pip install pandas >nul 2>&1
)

REM Verifica si matplotlib está instalado, si no, lo instala
pip show matplotlib >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando matplotlib...
    pip install matplotlib >nul 2>&1
)

REM Solicita la ruta de datos al usuario
set /p ruta_datos=Ingrese la ruta de la carpeta de datos: 

echo Ejecutando script...
REM Ejecuta el script Python pasando la ruta de datos como argumento
start "" /B pythonw "%ruta_actual%gmrt2045.py" "%ruta_datos%"

echo Script completado. Revisa la imagen GMRT2045_plot.png en la carpeta actual.
pause