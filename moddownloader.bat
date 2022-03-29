@echo off
echo 'welcom to jack mod install' 
echo 'the script now uses python.'
echo 'please wait while we install python + needed libraries.'
::check if python v3 is installed 
if not exist "C:\Python37\python.exe" goto python_install
echo 'python v3 is not installed, installing now.'
::install python v3
::download pythonv3.7
::check for chocolatey
if not exist "C:\ProgramData\chocolatey\bin\choco.exe" goto choco_install
:choco_install
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))