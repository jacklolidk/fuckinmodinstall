echo 'welcom to jack mod install' 
echo 'the script now uses python.'
echo 'please wait while we install python + needed libraries.'
python --version >NUL
if errorlevel 0 goto python2_installed
echo 'python 2 not found. trying to find python 3'
python3 --version >NUL
if errorlevel 0 goto python3_installed
echo 'python not installed. installing..'
powershell cd \jacktempfolder\py; start-Bitstransfer https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe
cd \jacktempfolder\py
python-3.10.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
:python2_installed
echo 'needed python3. installing..'
powershell cd \jacktempfolder\py; start-Bitstransfer https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe
cd \jacktempfolder\py
python-3.10.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
python3 --version >NUL
if errorlevel 0 goto python3_installed
:python3_installed
echo 'python3 installed.'
pip3 install paramiko
cd \jacktempfolder
::check if python script exists
if exist moddownloader.py (
echo 'python script found. skipping download.'
else
echo 'python script not found.'
echo 'downloading python script..'
powershell cd \jacktempfolder; start-Bitstransfer https://raw.githubusercontent.com/jack-team/jack-mod-installer/master/moddownloader.py
fi