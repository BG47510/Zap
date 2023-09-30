#!/usr/bin/python3
import requests
import sys


# idvideo (str): L'ID de la vidéo Dailymotion.
def dailymotion(idvideo: str):
    # Récupère les flux Dailymotion en fonction de l'ID vidéo.
    try:
        url = f"https://www.dailymotion.com/player/metadata/video/{idvideo}"
        response = requests.get(url).json()
        flux = response["qualities"]["auto"][0]["url"]
        m3u8 = requests.get(flux).text
        print(m3u8)
    # Exception: si une erreur se produit lors de la récupération des flux.
    except Exception as m3u8:
        m3u8 = "https://raw.githubusercontent.com/BG47510/Zap/main/assets/error.m3u8"
        print(m3u8)


if __name__ == "__main__":
    idvideo = "x2lefik"
    dailymotion(idvideo)

