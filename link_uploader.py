from asyncore import write
from imghdr import what
import paramiko
import os
import requests as rq
import json
import time
import sys
tries = 1
temp1 = ' '
manifestask = ' '
manifestfile = ' '
jsonreal = 'false'
filenotfoundmsg = False
##much cool functions
def askfile():
    global tries
    global manifestask
    if tries > 10:
        print('\033[91m=>[FATAL] time was wasted.')
        exit()
    manifestask = input(f'\033[91m=>where the fuck is the file? [{tries}/10] (type exit to leave)\033[90m\n==> ')
    if manifestask == 'exit':
        exit()
    tries = tries + 1
def jsoncheck(file):
    global jsonreal
    with file as f:
        try:
            return json.load(f) # put JSON-data to a variable
        except json.decoder.JSONDecodeError:
            jsonreal = 'false'
        else:
            jsonreal = 'true'

##start normal code
currentdir = os.getcwd()
##delete output.txt if it exists
if os.path.exists(currentdir + '/output.txt'):
    os.remove('output.txt')

##make sure the loop isnt exitable unless manifest.json is found
while True:
    ##try finding file in current directory
    try:
        manifestfile = open(currentdir + '/manifest.json')
        manifestfile = currentdir + '/manifest.json'
        print('\033[92m=>[SUCCESS] manifest.json found!')
        break
    except:FileNotFoundError
    if True == False:
        ifuckedup = True
    else:
        if filenotfoundmsg == False:
            print('\033[93m=>[WARNING] manifest.json not found in current folder.')
            filenotfoundmsg = True
        manifestfile = askfile()
        ##check if file exists
        if not os.path.isfile(manifestask):
            print("\033[93m=>[WARNING] file doesn't fucking exist. try again.")
            askfile()
        else:
            ##check if file is a json formatted file
            jsoncheck(manifestask)
            if jsonreal == 'true':
                print('\033[92m=>[SUCCESS] manifest.json found!')
                ##leave loop
                manifestfile = manifestask
                break
            elif jsonreal == 'false':
                print('\033[91m=>[FATAL] manifest.json is not a json formatted file. try again.')
                askfile()
            else:
                print('\033[91m=>[FATAL] something went very wrong. try again.')
                exit()

manifest = ' '

##open file but make sure the file is there

with open(manifestfile) as f:
    manifest = json.load(f)
    print('\033[92m ')
FILE_IDS = [file["fileID"] for file in manifest["files"]]
PROJECT_IDS = [file["projectID"] for file in manifest["files"]] # Project IDs of the mods, as shown on the mod page
VERSION = manifest["minecraft"]["version"] # Name of the game version
MODLOADER = manifest["minecraft"]["modLoaders"][0]["id"]

for i, id in enumerate(PROJECT_IDS):
    ticker = f"[{i+1}/{len(PROJECT_IDS)}]" # For showing which mod we're on

    # Get mod name, so it looks nice
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}").content) # Put the request's data into a Python-readable format
    modName = data["name"]
    # Get mod's latest version for this game version
    print(f"{ticker} Getting mod download link for mod {modName} (ID: {id})...")
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}/files").content)
    # Get the correct version matching the file ID for this mod
    correctVersion = {}
    try:
        correctVersion = [candidate for candidate in data if FILE_IDS[i] == candidate["id"]][0]
        print(f"=>{ticker} Found correct mod version (File ID: {FILE_IDS[i]} for mod {modName} (ID: {id})!")
    except:
        print(f"=>{ticker} Couldn't find a matching file ID ({FILE_IDS[i]}) for mod {modName} (ID: {id}). Downloading latest version for the current forge version...")
        correctVersion = [candidate for candidate in data if VERSION == candidate["gameVersion"][0]]
    try:
            print(f"=>{ticker} Starting download of mod {modName} (ID: {id})...")
            ##write to output.txt
            ##check if output.txt exists.
            #create output.txt if not exist
            if not os.path.isfile("output.txt"):
                open("output.txt", "w").close()
            with open("output.txt", "a") as f:
                f.write(correctVersion["downloadUrl"] + "\n")
                ##close file because why not
                f.close()
                print(f"=>{ticker} added mod {modName} (ID: {id}) to output.txt!")
    except: # The fileID isn't available
        print(f"\033[93m=>{ticker} {modName} failed processing! (ID: {id})")
        time.wait(1)
        print('\033[92m ')
        ##skip to next mod
        continue

print(f"=>Finished proc all {len(PROJECT_IDS)} mods.")
##add version and fabric info to output.txt at last line
with open("output.txt", "a") as f:
    f.write("\n" + f"minecraft {VERSION} with {MODLOADER}")
    f.close()
print("=>Added version and modloader info to output.txt.")
print("\033[97m=>uploading to server...")

host = "192.168.99.45"
port = 22
transport = paramiko.Transport((host, port))
usr = "pi"
passwd = "raspberry"
transport.connect(username = usr, password = passwd)
sftp = paramiko.SFTPClient.from_transport(transport)

path = currentdir + "/output.txt"
##make sure file exists on server otherwise make it

sftp.put(path, "/home/pi/modlist/output.txt")

sftp.close()
transport.close()
print("\033[97m=>done.")
##delete output.txt to avoid confusion next run
os.remove("output.txt")
print("\033[97m=>deleted output.txt.")