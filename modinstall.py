import paramiko
import sys
import os
currentdir = os.getcwd()
currentline = 0

host = "221.124.104.230"
port = 6101
transport = paramiko.Transport((host, port))
usr = "pi"
passwd = "raspberry"
transport.connect(username = usr, password = passwd)
sftp = paramiko.SFTPClient.from_transport(transport)

path = currentdir + "/output.txt"
sftp.get("/home/pi/modlist/output.txt", path)


sftp.close()
transport.close()
print("downloaded modlist.\ninstalling..")
##echo each line for each line in modlist
with open("output.txt") as f:
    for line in f:
        currentline += 1
        ##last line is version + modloader, so ignore it while downloading
        if currentline == len(f):
            break
        else:
            print(f"installing mod {currentline}/{len(f)}")
            os.system(f"powershell cd ~\Appdata\Roaming\.minecraft\mods; Start-BitsTransfer {line}")