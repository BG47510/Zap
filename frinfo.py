#! /usr/bin/python3
import requests

headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}

base = 'https://hdfauth.ftven.fr/esi/TA?url='
chaine = 'https://simulcast-p.ftven.fr/simulcast/France_Info/hls_monde_frinfo/index.m3u8'
source = base + chaine

response = requests.get(source, headers=headers).text

lien = response.replace("index", "France_Info-avc1_2500000=10001")
lien2 = response.replace("index", "France_Info-mp4a_96000_fra=20000")
# Les f-string permettent d’insérer des variables ou expressions
# à l'intérieur d'une chaine de caractères.
flux = f'\n#EXTM3U\n#EXT-X-VERSION:5\n#EXT-X-STREAM-INF:BANDWIDTH=3032655,\
AVERAGE-BANDWIDTH=2756959,CODECS="avc1.64001f,mp4a.40.2",\
RESOLUTION=1280x720,FRAME-RATE=25.000,AUDIO="audio-AACL-96",SUBTITLES="text"\n\
{lien}'
flux2 = f'\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-96",LANGUAGE="fr",\
NAME="Francais",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",\
URI="{lien2}"'
m3u8 = flux + flux2
print(m3u8)
