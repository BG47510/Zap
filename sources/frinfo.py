#!/usr/bin/env python

import requests
#import os
#import sys


#headers = {'User-Agent': 'QwantMobile/2.0 (Android 5.1; Tablet; rv:61.0) Gec \
#ko/61.0 Firefox/59.0 QwantBrowser/61.0'}


s = requests.Session()
response = s.get('https://hdfauth.ftven.fr/esi/TA?url=https://simulcast-p.ftven.fr/simulcast/France_Info/hls_monde_frinfo/index.m3u8')
#print(response.text)

source = response.text

lien = source.replace("index", "France_Info-avc1_2500000=10001")

lien2 = source.replace("index", "France_Info-mp4a_96000_fra=20000")


flux = ('\n#EXTM3U\n#EXT-X-VERSION:'
        '5\n#EXT-X-STREAM-INF:BANDWIDTH=3032655,'
        'AVERAGE-BANDWIDTH=2756959,CODECS="avc1.64001f,mp4a.40.2",'
        'RESOLUTION=1280x720,FRAME-RATE=25.000,AUDIO="audio-AACL-96",SUBTITLES="text"\n'
        + lien)


#flux2 = (f'\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-96",LANGUAGE="fr",'
#'NAME="Francais",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="'
#+ lien2
#'\"')

flux2 = (f'\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-96", \
LANGUAGE="fr",NAME="Francais",DEFAULT=YES,AUTOSELECT=YES, \
CHANNELS="2",URI="{lien2}"')


m3u8 = (flux + flux2)

print(m3u8)


#if 'temp.txt' in os.listdir():
    #os.system('rm temp.txt')
    #os.system('rm watch*')

fichier = open("frinfo.m3u8", "w")
fichier.write(m3u8)
fichier.close()
