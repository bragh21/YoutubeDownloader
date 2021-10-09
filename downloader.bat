@echo off
color 30

set baseDir=%~dp0
set envPython="%baseDir:"=%.venv\Scripts\python.exe"
set script="%baseDir:"=%mainv0.2.py"

%envPython% %script%
pause