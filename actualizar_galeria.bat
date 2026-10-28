@echo off
echo ==============================================
echo   Sincronizando Galería Digital - EduArt
echo ==============================================
cd /d "%~dp0"
echo.
echo [1/2] Sincronizando obras nuevas y actualizando datos...
py herramientas_mantenimiento\sincronizar_galeria.py
echo.
echo [2/2] Inyectando firma de autor (E. Ramirez / EduArt)...
py herramientas_mantenimiento\inject_author_metadata.py
echo.
echo ==============================================
echo   COMPLETADO. Galeria actualizada y firmada.
echo ==============================================
echo.
pause
