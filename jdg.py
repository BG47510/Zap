#! /usr/bin/python3
import httpx
import os
import sys


headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}

proxies = {}
if len(sys.argv) == 2:
    proxies = {
                'http' : sys.argv[1],
                'https' : sys.argv[1]
              }

url = "https://www.dailymotion.com/player/metadata/video/k5VKYQn5hAE4vfry927?embedder=https://www.journaldugolf.fr"
erreur = httpx.get("https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8")

def snif(url):
    # Sérialisation d'une requête GET avec .json()
    lien = httpx.get(url, headers=headers, proxies=proxies).json()
    cle = 'qualities'
    if cle in lien:
        retour = lien["qualities"]["auto"][0]["url"]
        # .text renvoie le contenu converti en chaîne de caractères UTF-8.
        flux = httpx.get(retour)
        print(flux.text)
    else:
        print(erreur.text)


snif(url)



