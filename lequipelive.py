#!/usr/bin/python3
# par github.com/BG47510

from urllib.parse import unquote
import requests
import re
import sys
import random

# User-Agent laisse des informations dans les logs du site visité.
# Elles permettent de savoir si leur site est crawlé.
# Changer son user-agent :
ua = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Android 12; Mobile; rv:100.0) Gecko/100.0 Firefox/100.0',
    'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.7.2) Gecko/20040804',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Dalvik/2.1.0 (Linux; U; Android 13; POCO F1 Build/TQ3A.230805.001)',
    'Mozilla/5.0 (X11; Linux x86_64; rv:5.1) Goanna/20220721 PaleMoon/31.1.1',
]

# l’User-Agent et le Referer dans l’en-tête de la requête.
headers = {
    "User-Agent": random.choice(ua),
    "Referer": "https://www.lequipe.fr/tv/videos/",
}

url = "https://www.dailymotion.com/player/metadata/video/x2lefik"

erreur = 'https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8'

def snif(url):
    lien = s.get(url, headers=headers, timeout=15).json()
    retour = lien["qualities"]["auto"][0]["url"]
    tri = unquote(''.join(retour))
    flux = requests.get(tri).text
    if '.m3u8' not in tri:
        print(erreur)
    else:
        print(flux)



s = requests.Session()
result = snif(url)
#result = snif(str(sys.argv[1]))
print(result)


