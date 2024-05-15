#! /usr/bin/python3
import sys
import requests

headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}
proxies = {}
if len(sys.argv) == 2:
    proxies = {
                'http' : sys.argv[1],
                'https' : sys.argv[1]
              }

video = "https://www.dailymotion.com/player/metadata/video/k5VKYQn5hAE4vfry927?"
site = "embedder=https://www.journaldugolf.fr"
base = video + site
erreur = "https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8"

def snif(base):
    # Sérialisation d'une requête GET avec .json()
    lien = s.get(base, headers=headers, proxies=proxies).json()
    cle = 'qualities'
    if cle in lien:
        retour = lien["qualities"]["auto"][0]["url"]
        # .text renvoie le contenu converti en chaîne de caractères UTF-8.
        flux = requests.get(retour)
        print(flux.text)
    else:
        echec = requests.get(erreur)
        print(echec.text)

s = requests.session()
snif(base)



