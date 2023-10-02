#! /usr/bin/python3

from urllib.parse import unquote
import requests
import re
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

erreur = 'https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8'


def snif(url):
    lien = s.get(url, timeout=15).text
    retour = re.findall(r'\"hlsManifestUrl\":\"(.*?)\"\}', lien)
    tri = unquote(''.join(retour))
    flux = requests.get(tri).text
    if '.m3u8' not in tri:
        print(erreur)
    else:
        print(flux)

s = requests.Session()
result = snif(str(sys.argv[1]))
print(result)
