import requests
import zipfile
import os
import shutil
import json

os.chdir(os.path.dirname(__file__))
if os.path.exists("server.jar"):
    os.remove("server.jar")
if os.path.exists("assets"):
    shutil.rmtree('assets')

r = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
versions = r.json()
version = versions['latest']['release']
url = None
for urls in versions['versions']:
    if urls['id'] == version:
        url = urls['url']
        break

r = requests.get(url)
jar = r.json()['downloads']['server']['url']

r = requests.get(jar, allow_redirects=True)
open('server.jar', 'wb').write(r.content)

with zipfile.ZipFile("server.jar") as z:
    z.extract("assets/minecraft/lang/en_us.json")

with open("assets/minecraft/lang/en_us.json") as f:
    data = json.load(f)

for key,value in data.items():
    if key[:16] == "block.minecraft." and key[:23] != "block.minecraft.banner.":
        print(f"{key[16:]} - {value}")