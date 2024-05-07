# Utiliser un réseau privé virtuel (VPN)

# Contribution - Contributing

Merci de l’intérêt que vous portez à ce projet ! Votre aide pour améliorer ce projet est la bienvenue.
Thank you for your interest in this project! Your help to improve this project is welcome.

Cette action GitHub prend en charge un fichier de configuration ovpn, des informations d’identification et l’adresse IP attendue du VPN. Elle installe l’interface de ligne de commande ovpn, s’y connecte et exécute une boucle pour confirmer la connectivité.

Ceci est particulièrement utile pour une adresse IP bloquée géographiquement.


Pour ajouter une connexion VPN, transférez d’abord le fichier de configuration OpenVPN (.ovpn) de votre client OpenVPN dans votre dépôt. Il doit contenir les certificats nécessaires à l’installation.
Ensuite, vous devez personnaliser les entrées suivantes : vpn_id, vpn_mp et vpn_client dans le fichier openconnect.yml. Le nom d’utilisateur VPN est défini dans vpn_id, le mot de passe VPN est spécifié par vpn_mp et le chemin d'accès au fichier .ovpn est transmis avec vpn_client.


```yml
inputs:
      vpn_id:
        description: 'votre identifiant'
        required: true
        default: ''
      vpn_mp:
        description: 'votre mp'
        required: true
        default: ''
      vpn_client:
        description: 'votre chemin d'accès'
        required: true
        default: '.github/vpn/client.ovpn'
```



Si vous avez besoin de générer une nouvelle configuration ovpn à partir d’une connexion de viscosité. [Il s’agit d’un résumé utile](https://gist.github.com/vinicius795/e975688fa8ffcba549d8240ecf0a7f9f)

## General

### Usage

```yml
steps:
    - uses: actions/labeler@v4
      with:
        configuration-path: ${{ inputs.vpn_id }}
        configuration-path: ${{ inputs.vpn_mp }}
        configuration-path: ${{ inputs.vpn_client }}
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
