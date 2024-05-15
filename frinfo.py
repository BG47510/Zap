#! /usr/bin/python3

import requests
import random

ua = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Android 12; Mobile; rv:100.0) Gecko/100.0 Firefox/100.0',
    'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.7.2) Gecko/20040804',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Dalvik/2.1.0 (Linux; U; Android 13; POCO F1 Build/TQ3A.230805.001)',
    'Mozilla/5.0 (X11; Linux x86_64; rv:5.1) Goanna/20220721 PaleMoon/31.1.1',
]

# l’User-Agent et le Referer dans l’en-tête de la requête.
headers = {
    "User-Agent": random.choice(ua),
}


https ='https://api.proxyscrape.com/?request=displayproxies&proxytype=https'
yui = requests.get(https).text.strip().split('\n')


http ='https://api.proxyscrape.com/?request=displayproxies&proxytype=http'
aze = requests.get(http).text.strip().split('\n')

# proxy > Country:China

proxy = '117.146.231.40:9002'




site = 'https://hdfauth.ftven.fr/esi/TA?url=https://simulcast-p.ftven.fr/simulcast/France_Info/hls_monde_frinfo/index.m3u8'

response = requests.get(site, headers=headers, proxies={"http": proxy}, timeout=15).text



lien = response.replace("index", "France_Info-avc1_2500000=10001")

lien2 = response.replace("index", "France_Info-mp4a_96000_fra=20000")
#print(f'#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-96",LANGUAGE="fr",NAME="Francais",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="{lien2}"')


# Les f-string permettent d’insérer des variables ou expressions à l'intérieur d'une chaine de caractères.


flux = (f'\n#EXTM3U\n#EXT-X-VERSION:5\n#EXT-X-STREAM-INF:BANDWIDTH=3032655,AVERAGE-BANDWIDTH=2756959,CODECS="avc1.64001f,mp4a.40.2",RESOLUTION=1280x720,FRAME-RATE=25.000,AUDIO="audio-AACL-96",SUBTITLES="text"\n{lien}')

flux2 = (f'\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-96",LANGUAGE="fr",NAME="Francais",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="{lien2}"')

m3u8 = (flux + flux2)

print(m3u8)


#if 'temp.txt' in os.listdir():
 #   os.system('rm temp.txt')
  #  os.system('rm watch*')

#fichier = open("frinfo.m3u8", "w")
#fichier.write(m3u8)
#fichier.close()
