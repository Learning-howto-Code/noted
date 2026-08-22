# needs to create .plist command
# needs to install dependencies
#add mcp server to claude?
import os
import plistlib
from pathlib import Path
import subprocess
import shutil

root = Path(__file__).resolve().parent
print(root)
#checks for nowplaying-cli, installs if not found
if not Path("/opt/homebrew/bin/nowplaying-cli").exists():
    #brew installs now playing-cli
    r = subprocess.run(
    ["brew", "install", "nowplaying-cli"],
        text=True,
        check=True,
)
    print("installed nowplaying-cli")
else:
    print("nowplaying-cli already installed")
#checks for venv, makes one otherwise
if not (root / "venv").is_dir():
    r = subprocess.run(
        ["python3", "-m", "venv", "venv"],
            capture_output=True,
            text=True,
            check=True,
    )
venv = root / "venv"
print(venv)
#installs python libs
r = subprocess.run(
    ["venv/bin/python", "-m", "pip", "install", "-r", "requirements.txt"],
        text=True,
        check=True,
)
print("installed python libs")

#gets python path
r = subprocess.run(
    ["which", "python3"],
        capture_output=True,
        text=True,
        check=True,
)
# python and logs paths
python = os.path.join(root, "venv/bin/python")
logs = root / "logs"
logs.mkdir(exist_ok=True)

# adds api key to .env file
with open(".env", "a")as f:
    f.write(f"HCAI={input('Enter your Hackclub AI api key here: ')}\n")
#creates .plist file
LABEL = "local.jake.musictracker"
# creates plist file, than dumps to it
plist_path = Path.home() / "Library/LaunchAgents" / f"{LABEL}.plist"
plist = {
    "Label": LABEL,
    "ProgramArguments": [str(python), "-u", str(root / "main.py")],
    "WorkingDirectory": str(root),   # so main.py's relative allowlist.txt etc. work
    "RunAtLoad": True,               # start now + at login
    "KeepAlive": True,               # restart on crash
    "ThrottleInterval": 10,          # min 10s between restarts
    "StandardOutPath": str(logs / "out.log"),
    "StandardErrorPath": str(logs / "err.log"),
}
plist_path.parent.mkdir(parents=True, exist_ok=True)
with plist_path.open("wb") as f:     # binary mode — plistlib writes bytes
    plistlib.dump(plist, f)
print("created launchd service")
#makes sure no other instance of daemon are running
uid = os.getuid()
domain = f"gui/{uid}"
for label in (LABEL, "local.jake.noted"):   # kill this + the old ghost label
    subprocess.run(["launchctl", "bootout", f"{domain}/{label}"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run(["launchctl", "bootstrap", domain, str(plist_path)], check=True)
print("everything should be installed")
