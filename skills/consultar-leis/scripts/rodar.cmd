@echo off
REM Atalho do consultar-leis: fixa o acervo e usa o Python que funciona nesta maquina.
REM Uso: rodar.cmd buscar --numero 10406 --ano 2002
setlocal
set "ACERVO=H:\acervo\leis"
set "PY=C:\Users\victo\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"
if not exist "%ACERVO%" (
  echo Acervo nao encontrado em %ACERVO%
  exit /b 1
)
"%PY%" "%~dp0consultar.py" --acervo "%ACERVO%" %*
