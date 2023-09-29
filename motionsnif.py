import requests


# par github.com/BG47510/


idmotion = line.split("/")[4]
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
        ligne = line.strip()
        if not ligne or line.startswith("~~"):
            continue
        if not line.startswith("https:"):
            ligne = line.split("|")
            nom = line[0].strip()
            grtitre = line[1].strip().title()
            logo = line[2].strip()
            idvideo = line[3].strip()
            print(
                f'\n#EXTINF:-1 group-title="{grtitre}" tvg-logo="{logo}" tvg-id="{idvideo}", {nom}'
            )
        else:
            print(m3u8)
