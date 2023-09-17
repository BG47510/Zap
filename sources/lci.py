#! /usr/bin/python3
import requests
import json


headers = {'User-Agent': 'QwantMobile/2.0 (Android 5.1; Tablet; rv:61.0) Gecko/61.0 Firefox/59.0 QwantBrowser/61.0'}

# L’objet Session vous permet de conserver des paramètres entre plusieurs requêtes.
# Il permet également de conserver les cookies entre toutes les requêtes de la même instance Session.
# Il peut aussi être utilisés pour fournir des valeurs par défaut aux requêtes (auth, headers)

session = requests.Session()

response = session.get('https://mediainfo.tf1.fr/mediainfocombo/L_LCI?format=hls', headers=headers).json()

source = response["delivery"]["url"]

lien = source.replace("index", "index_1")

lien2 = source.replace("index", "index_6_0")


# Les f-string permettent d’insérer des variables ou expressions à l'intérieur d'une chaine de caractères.

# flux video
flux = (f'\n#EXTM3U\n#EXT-X-VERSION:6\n#EXT-X-INDEPENDENT-SEGMENTS\n#EXT-X-STREAM-INF:BANDWIDTH=3412864,AVERAGE-BANDWIDTH=2891084,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.4D401F,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"\n{lien}')

# flux audio
flux2 = (f'\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio_0",CHANNELS="2",NAME="français",LANGUAGE="fra",DEFAULT=YES,AUTOSELECT=YES,URI="{lien2}"')

m3u8 = (flux + flux2)

print(m3u8)
