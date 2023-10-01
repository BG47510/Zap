#! /usr/bin/python3
# par github.com/BG47510


from urllib.parse import unquote
import requests
import re


print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

s = requests.Session()

erreur = "https://raw.githubusercontent.com/naveenland4/UTLive/main/assets/info.m3u8"

url = "https://www.youtube.com/watch?v=Z-Nwo-ypKtM"

source = s.get(url, timeout=15).text

flux = re.findall(r"\"hlsManifestUrl\":\"(.*?)\"\}", source)

m3u8 = unquote("".join(flux))

if "m3u8" in m3u8:
    print(m3u8)
else:
    print(erreur)

