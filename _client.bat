@echo off
setlocal

cd /d %~dp0

set msg=%3
set port=%2
set pip_pythonpath=%1
set pip_pythonpath=%pip_pythonpath:"=%


"%pip_pythonpath%\python" _client.py %port% %msg%

:end
timeout 5
