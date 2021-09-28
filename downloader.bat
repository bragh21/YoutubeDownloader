@echo off
color 30

set baseDir=%~dp0
set envPython="%baseDir:"=%.venv\Scripts\python.exe"
set script="%baseDir:"=%main.py"

%envPython% %script%
pause