import requests
import re

# par github.com/BG47510/


idmotion = ligne.split("/")[4]
# idmotion = 'x5gv5v0' # cstar

erreur = "https://raw.githubusercontent.com/naveenland4/UTLive/main/assets/info.m3u8"


url = f"https://www.dailymotion.com/player/metadata/video/{idmotion}"
response = requests.get(url).json()
flux = response["qualities"]["auto"][0]["url"]
liens = requests.get(flux).text
m3u8 = liens.split()[-1]
print(m3u8)

print("#EXTM3U")

s = requests.Session()

with open("motionsource.txt") as f:
    for ligne in f:
        ligne = ligne.strip()
        if not ligne or ligne.startswith("~~"):
            continue
        if not ligne.startswith("https:"):
            ligne = ligne.split("|")
            nom = ligne[0].strip()
            grtitre = ligne[1].strip().title()
            logo = ligne[2].strip()
            idvideo = ligne[3].strip()
            print(
                f'\n#EXTINF:-1 group-title="{grtitre}" tvg-logo="{logo}" tvg-id="{idvideo}", {nom}'
            )
        else:
            print(m3u8)
