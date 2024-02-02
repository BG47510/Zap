#!/usr/bin/python3

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Referer": "http://www.callofliberty.fr/"
}


url = "http://s2.callofliberty.fr/direct/TF1/master.m3u8"
s = requests.session()

response = s.get(url, headers=headers).text





print(response)
