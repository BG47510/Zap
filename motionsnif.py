#! /usr/bin/python3
# par github.com/BG47510
import requests
import sys

erreur = 'https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8'
def snif(line):
    try:
        idvideo = line.split('/')[4]
        url = f'https://www.dailymotion.com/player/metadata/video/{idvideo}'
        response = requests.get(url).json()
        m3u8 = response["qualities"]["auto"][0]["url"]
    except Exception as e:
        m3u8 = erreur
    finally:
        print(m3u8)

print('#EXTM3U')
with open('motionsource.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            nom = line[0].strip()
            grp = line[1].strip().title()
            logo = line[2].strip()
            idepg = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp}" tvg-logo="{logo}" tvg-id="{idepg}", {nom}')
        else:
            snif(line)
        
