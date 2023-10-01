#! /usr/bin/python3

import requests
# import os
import sys

#proxies = {}
#if len(sys.argv) == 2:
  #  proxies = {
              #  'http' : sys.argv[1],
               # 'https' : sys.argv[1]
            #  }

na = 'https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8'
def grab(line):
    try:
        _id = line.split('/')[4]
        url = f'https://www.dailymotion.com/player/metadata/video/{_id}' # .json()['qualities']['auto'][0]['url']
        response = requests.get(url).json()
        m3u = response["qualities"]["auto"][0]["url"]
       # print(m3u)
      #  m3u = requests.get(flux).text
       # m3u = liens.split()[-1]
       # m3u = m3u.strip().split('\n')[1:]
      #  m3u = m3u.strip().split(',')[2].split('=')[1]
        #d = {}
        #cnd = True
        #for item in m3u:
            #if cnd:
               # resolution = item.strip().split(',')[2].split('=')[1]
               # if resolution not in d:
                   # d[resolution] = []
           # else:
               # d[resolution]= item
          #  cnd = not cnd
        #print(m3u)
      #  m3u = d[max(d, key=int)]    
    except Exception as e:
        m3u = na
    finally:
        print(m3u)

print('#EXTM3U')
#s = requests.Session()
with open('motionsource.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)
        
