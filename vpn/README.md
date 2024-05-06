# OVPN connection

Cette action GitHub prend en charge un fichier de configuration ovpn, des informations d’identification et l’adresse IP attendue du VPN. Elle installe l’interface de ligne de commande ovpn, s’y connecte et exécute une boucle pour confirmer la connectivité.


Si vous avez besoin de générer une nouvelle configuration ovpn à partir d’une connexion de viscosité. [Il s’agit d’un résumé utile](https://gist.github.com/vinicius795/e975688fa8ffcba549d8240ecf0a7f9f)

## General

### Usage

```yml
- uses: principlesos/actions/ovpn-connection@v1.5.0
  with:
    ovpn-config: ${{ secrets.VPN_CONFIG }}
    vpn-creds: ${{ secrets.VPN_CREDS }}
    vpn-ip: ${{ secrets.VPN_IP }}
```

### Cleanup

C’est une bonne pratique de couper la connexion VPN une fois que vous avez terminé les opérations nécessaires.
Vous pouvez utiliser une étape comme celle ci-dessous pour arrêter la connexion et conserver l’accès au journal

```yml
- name: Kill VPN connection
  if: always()
  run: |
    sudo chmod 777 vpn.log
    sudo killall openvpn
```
