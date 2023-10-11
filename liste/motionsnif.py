#! /usr/bin/python3
# par github.com/BG47510/

import requests
from random import randint
from time import sleep

# l’User-Agent et le Referer dans l’en-tête de la requête.
# Pour imiter une session de navigation d’un utilisateur humain.
headers = {
    "User-Agent": "QwantMobile/2.0 (Android 5.1; Tablet; rv:61.0) Gecko/61.0 Firefox/59.0 QwantBrowser/61.0",
    "Referer": "https://www.qwant.com/",
}

erreur = 'https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8'

def snif(line):
    cible = "https://www.dailymotion.com/player/metadata/video/"
    source = line.split('/')[4]
    retour = requests.get(cible + source, headers=headers, timeout=15).json()
    m3u8 = retour["qualities"]["auto"][0]["url"]
    if '.m3u8' not in m3u8:
        print(erreur)
    else:
        print(m3u8)
    # time.sleep(15) # 15 secondes
    sleep(randint(15,25))

print('#EXTM3U')
with open('liste/motionsource.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('##'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            chnom = line[0].strip()
            grp = line[1].strip().title()
            tvgname = line[2].strip()
            idepg = line[3].strip()
            print(f'#EXTINF:-1 tvg-id="{idepg}" tvg-name="{tvgname}" group-title="{grp}", {chnom}')
        else:
            snif(line)

        
