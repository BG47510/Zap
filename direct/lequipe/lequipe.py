#! /usr/bin/python3

import requests
import os
import sys

proxies = {}
if len(sys.argv) == 2:
    proxies = {"http": sys.argv[1], "https": sys.argv[1]}

nul = "https://s7.mbahnunungonline.net/live/m3u8/op/7335edf66aba710.m3u8"


def grab(line):
    try:
        _id = line.split("/")[4]
        response = s.get(
            f"https://www.dailymotion.com/player/metadata/video/{_id}", proxies=proxies
        ).json()["qualities"]["auto"][0]["url"]
        m3u8 = s.get(response, proxies=proxies).text
        m3u8 = m3u8.strip().split("\n")[1:]
        d = {}
        cnd = True
        for item in m3u8:
            if cnd:
                resolution = item.strip().split(",")[2].split("=")[1]
                if resolution not in d:
                    d[resolution] = []
            else:
                d[resolution] = item
            cnd = not cnd
        m3u8 = d[max(d, key=int)]
    except Exception as e:
        m3u8 = nul
    finally:
        print(m3u8)


print("#EXTM3U")
print("#EXT-X-VERSION:3")
print("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000")
s = requests.Session()
with open("direct/lequipe/lequipe.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("~~"):
            continue
        if not line.startswith("https:"):
            line = line.split("|")
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
        else:
            grab(line)

if "temp.txt" in os.listdir():
    os.system("rm temp.txt")
    os.system("rm watch*")
