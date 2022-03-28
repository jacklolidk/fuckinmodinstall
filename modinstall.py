import paramiko
import sys
import os

host = "192.168.99.45"
port = 6101
transport = paramiko.Transport((host, port))
usr = "pi"
passwd = "raspberry"
transport.connect(username = usr, password = passwd)
sftp = paramiko.SFTPClient.from_transport(transport)

path = currentdir + "/output.txt"
sftp.get("/home/pi/modlist/output.txt")

sftp.close()
transport.close()
print("\033[97m=>done.")