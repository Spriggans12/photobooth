# Photobooth pour le mariage

Okay.

Voici donc la doc sur le Photobooth (PB) qu'on va utiliser pour notre mariage.

Donc, le PB fonctionne sur un Raspberry pi (PI), qui est relié à une caméra, et à un écran.

Ici, je vais essayer de tous lister pour pouvoir s'en sortir sans problèmes.


## Architecture du projet


Comme une image vaut mieux qu'un long discours :

![schema global](images-for-doc/schema_global.png)


Donc, il y a quelques composants dans le projet. On va se faire toute la chaîne pour tous les présenter :

### La télécommande (Remote)

En début de chaîne, la Remote (c'est le petit machin noir en bas à gauche). C'est la télécommande qui permet de lancer une photo.

Il faut l'allumer (sur sa droite, il y a un petit bouton on/off).

Elle parle au PI en Bluetooth.


### Le PI

Il fait tourner un programme pyhton : *camera.py* 

Ce prgm écoute les inputs de la Remote, et quand on appuie sur un boutton, il parle à la caméra pour prendre des photos.

Le PI est aussi connecté sur la TV pour afficher les images.

Le PI doit être branché au secteur.


### La caméra

Rien à expliquer ici. Juste que la caméra est connectée physiquement au PI, et qu'il n'y a rien à faire de spécial vu qu'on ne peut pas les déconnecter.


### La TV

La sortie HDMI du PI est mise sur la TV. Donc, quand on prend une photo, le prgm python envoie la sortie vidéo que lui donne la caméra sur l'HDMI.

La TV est allumée via sa télécommande (car les boutons de la télé choisie sont cassés... ). Il faut régler l'input de la TV sur "HDMI".

La TV doit être branchée au secteur.


### Le PC

Finalement, il faut bien pouvoir lancer le programme python !

Donc pour ça, on se branche au PI par Ethernet. Il y a donc une connection Ethernet entre un PC et le PI.

Le PC doit être branché au secteur.


## La réalité sur le photobooth

OKAY ! Un schéma c'est bien, mais en réalité, on a condensé tout dans une jolie grosse boîte.

Cette jolie grosse boite, on appelle ça un Photobooth (PB) !

C'est une grosse boite dans laquelle on peut faire glisser l'écran, dans laquelle le PI est bien emboité, et la caméra bien mise.

Tous les fils tout moches sont cachés, et en plus, la boîte est décorée !

Ensuite, on pose cette jolie boîte sur une table (ou autre), pour qu'elle soit un peu en hauteur. Sur la table, on aura mis une nappe, toujours pour faire plus joli !

Et là où la caméra pointe, on ajoutera le décor (des genres de guirlandes par exemple).



(**TODO :** ajouter photos de l'intérieur de la boite)



## Procédure à suivre pour l'installation

Okay. Voici la procédure à suivre point par point pour lancer le machin : 


### Installation physique du PB

(**TODO :** Ajouter des photos !)


* Placer la table sur laquelle on va mettre le PB.
* Mettre la nappe sur la table.
* Mettre la grosse boîte sur la nappe.
* Prendre l'écran, et le mettre à l'intérieur de la boîte
* Prendre le cable HDMI.
* Relier le HDMI entre la TV et le PI.
* Prendre l'alim de la TV.
* Brancher l'alim de la TV sur la TV, puis sur la ralonge.
* Poser le PC Windows quelque part pas trop loin.
* Prendre l'alim du PC, et la brancher au PC et à la ralonge.
* Prendre le cable Ethernet.
* Relier le PI et le PC par Ethernet.
* Brancher l'éxtrémité de la ralonge au secteur.
* Allumer la télé avec la télécommande
* Prendre l'alim du PI
* Brancher l'alim du PI sur le PI, puis sur la ralonge.

### Vérifications

* Le petit voyant du PI est allumé.
* La TV est allumée, elle affiche le Desktop du PI.


### Allumer la remote
* Allumer la remote... (bouton on/off sur la droite vers le haut).

### Vérification
* Le voyant bleu s'affiche, et puis disparait après quelques secondes.


### Lancer le programme

** TODO :** IPScanner ou autre pour avoir l'IP du Ethernet si celle-ci est dynamique

** TODO :** Images

* Allumer le Windows.
* Sur le Windows, lancer WinSCP.
* Se connecter au PI (user : pi / mdp : raspi)
* Lancer un putty (raccourci : ctrl + p dans WinSCP).
* Aller dans le dossier photobooth.
```
cd photobooth
```
* Lancer le programme
```
python camera.py
```
* Bravo !

### Vérifications

* Si le programme tourne, l'écran de TV devrait afficher quelque chose.
* Si l'écran est noir, vérifier que la TV est bien allumée, et est bien sur l'input HDMI.
* Si l'écran est toujours noir, vérifier la sortie du programme...
  
  - Solutions possibles : la remote n'est pas allumée : allumer la.
  
  - Où bien celle-ci a été desynchronisée : Lancer "bluetoothctl"...

