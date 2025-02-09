@echo off
setlocal

cd /d %~dp0

set script_file=%2
set pip_pythonpath=%1
set pip_pythonpath=%pip_pythonpath:"=%

if not exist %script_file% (
    echo %script_file% does not exist
    goto end
)

if exist "%pip_pythonpath%\scripts\activate.bat" (
    goto activate
) else (
    goto python
)

:activate

echo Activating Python environment ...
call "%pip_pythonpath%\scripts\activate.bat" "%pip_pythonpath%"
echo python %script_file%
python %script_file%

goto end

:python

if not exist "%pip_pythonpath%\python.exe" (
    echo "%pip_pythonpath%\python.exe" does not exist
    goto end
)

echo Connecting to Python script ...
echo "%pip_pythonpath%\python.exe" %script_file%
"%pip_pythonpath%\python.exe" %script_file%

goto end


:end
if %ERRORLEVEL%==0 (timeout 10) else (Pause)