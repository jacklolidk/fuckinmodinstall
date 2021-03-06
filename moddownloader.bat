@echo off
echo 'welcom to jack mod install' 
echo 'the script now uses python.'
echo 'admin needed.'
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'"
    exit /b
)
echo 'please wait while we install python + needed libraries.'
::check if python v3 is installed 
if not exist "C:\Python37\python.exe" goto python_install
:choco_install
pause
powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
goto return1
:python_install
echo 'python v3 is not installed in default path, installing now.'
pause
set chocoinstalledpy = true
choco install python3 --force --version 3.7.4
echo 'that was a lotta text'
goto return2
:pip_update
pause
pip install --upgrade --user pip
echo 'a few more lines of text later...'
goto return3
:script
pause
::download script from github
::check if script is already downloaded
if not exist "modinstall.py" goto script_download
    :script_download
    echo 'python script not found, downloading..'
    curl https://raw.githubusercontent.com/jacklolidk/fuckinmodinstall/master/modinstall.py > modinstall.py
if python3 == true (
    python3 modinstall.py
else
    if python3 == false (
        python modinstall.py
    )
)
::main script
::download pythonv3.7
::check for chocolatey
choco --version > choco_version.txt
if not "1" in (Get-Content choco_version.txt) goto choco_install
:return1
::make sure downloaded python is version 3.7.4 with the python cli
if chocoinstalledpy == true (
    python3 --version > python_version.txt
    set python3 = true
else
    if chocoinstalledpy == false (
        python --version > python_version.txt
    )
)
::check if python_version.txt contains 3.7.4
if not "3.7.4" in (Get-Content python_version.txt) goto python_install
:return2
echo 'python is installed, now installing needed libraries.'
::check if pip is installed
pip --version > pip_version.txt
::if it isnt atleast v22 update pip
if not "pip 22" in (Get-Content pip_version.txt) goto pip_update
:return3
goto script