import requests
import re

# par github.com/BG47510/


"# idmotion = ligne.split('/')[4]
idmotion = 'x2lefik'

erreur = "https://raw.githubusercontent.com/naveenland4/UTLive/main/assets/info.m3u8"


def snif(ligne):
    try:
        url = f"https://www.dailymotion.com/player/metadata/video/{idmotion}"
        response = requests.get(url).json()
        flux = response["qualities"]["auto"][0]["url"]
        liens = requests.get(flux).text
m3u = liens.strip().split('\n')[1:]
			#for lines in liens :
   		#	if lines.split()[0]:
				  # print lines.split()[1]
     #   m3u8 = liens[1]
 #       print(m3u8)
    except Exception as e:
        m3u8 = erreur
        print(m3u8)
print(snif)
snif()
print("#EXTM3U")

#s = requests.Session()

#with open("motionsource.txt") as f:
    #for ligne in f:
       # ligne = ligne.strip()
       # if not ligne or ligne.startswith("~~"):
           # continue
       # if not ligne.startswith("https:"):
           # ligne = ligne.split("|")
         #   nom = ligne[0].strip()
           # grtitre = ligne[1].strip().title()
           # logo = ligne[2].strip()
            #id = ligne[3].strip()
          #  print(
          #      f'\n#EXTINF:-1 group-title="{grtitre}" tvg-logo="{logo}" tvg-id="{id}", {nom}'
       #     )
      #  else:
           # snif(ligne)

