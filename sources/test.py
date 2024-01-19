#! /usr/bin/python3
# par github.com/BG47510

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Referer": "https://www.lequipe.fr/tv/"
}

error = "https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8"
erreur = requests.get(error).text


video = f"https://www.dailymotion.com/video/x2j4lj9"
code = requests.get(video, headers=headers).json()
cle = "qualities"

if cle in code:
    flux = code["qualities"]["auto"][0]["url"]
    m3u8 = requests.get(flux).text
    print(m3u8)
else:
    print(erreur)


