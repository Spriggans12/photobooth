# Photobooth pour le mariage

Okay.

Voici donc la doc sur le Photobooth (PB) qu'on va utiliser pour notre mariage.

Donc, le PB fonctionne sur un Raspberry pi (PI), qui est reli� � une cam�ra, et � un �cran.

Ici, je vais essayer de tous lister pour pouvoir s'en sortir sans probl�mes.


## Architecture du projet


Comme une image vaut mieux qu'un long discours :

![schema global](images-for-doc/schema_global.png)


Donc, il y a quelques composants dans le projet. On va se faire toute la cha�ne pour tous les pr�senter :

### La t�l�commande (Remote)

En d�but de cha�ne, la Remote (c'est le petit machin noir en bas � gauche). C'est la t�l�commande qui permet de lancer une photo.

Il faut l'allumer (sur sa droite, il y a un petit bouton on/off).

Elle parle au PI en Bluetooth.


### Le PI

Il fait tourner un programme pyhton : *camera.py* 

Ce prgm �coute les inputs de la Remote, et quand on appuie sur un boutton, il parle � la cam�ra pour prendre des photos.

Le PI est aussi connect� sur la TV pour afficher les images.

Le PI doit �tre branch� au secteur.


### La cam�ra

Rien � expliquer ici. Juste que la cam�ra est connect�e physiquement au PI, et qu'il n'y a rien � faire de sp�cial vu qu'on ne peut pas les d�connecter.


### La TV

La sortie HDMI du PI est mise sur la TV. Donc, quand on prend une photo, le prgm python envoie la sortie vid�o que lui donne la cam�ra sur l'HDMI.

La TV est allum�e via sa t�l�commande (car les boutons de la t�l� choisie sont cass�s... ). Il faut r�gler l'input de la TV sur "HDMI".

La TV doit �tre branch�e au secteur.


### Le PC

Finalement, il faut bien pouvoir lancer le programme python !

Donc pour �a, on se branche au PI par Ethernet. Il y a donc une connection Ethernet entre un PC et le PI.

Le PC doit �tre branch� au secteur.


## La r�alit� sur le photobooth

OKAY ! Un sch�ma c'est bien, mais en r�alit�, on a condens� tout dans une jolie grosse bo�te.

Cette jolie grosse boite, on appelle �a un Photobooth (PB) !

C'est une grosse boite dans laquelle on peut faire glisser l'�cran, dans laquelle le PI est bien emboit�, et la cam�ra bien mise.

Tous les fils tout moches sont cach�s, et en plus, la bo�te est d�cor�e !

Ensuite, on pose cette jolie bo�te sur une table (ou autre), pour qu'elle soit un peu en hauteur. Sur la table, on aura mis une nappe, toujours pour faire plus joli !

Et l� o� la cam�ra pointe, on ajoutera le d�cor (des genres de guirlandes par exemple).



(**TODO :** ajouter photos de l'int�rieur de la boite)



## Proc�dure � suivre pour l'installation

Okay. Voici la proc�dure � suivre point par point pour lancer le machin : 


### Installation physique du PB

(**TODO :** Ajouter des photos !)


* Placer la table sur laquelle on va mettre le PB.
* Mettre la nappe sur la table.
* Mettre la grosse bo�te sur la nappe.
* Prendre l'�cran, et le mettre � l'int�rieur de la bo�te
* Prendre le cable HDMI.
* Relier le HDMI entre la TV et le PI.
* Prendre l'alim de la TV.
* Brancher l'alim de la TV sur la TV, puis sur la ralonge.
* Poser le PC Windows quelque part pas trop loin.
* Prendre l'alim du PC, et la brancher au PC et � la ralonge.
* Prendre le cable Ethernet.
* Relier le PI et le PC par Ethernet.
* Brancher l'�xtr�mit� de la ralonge au secteur.
* Allumer la t�l� avec la t�l�commande
* Prendre l'alim du PI
* Brancher l'alim du PI sur le PI, puis sur la ralonge.

### V�rifications

* Le petit voyant du PI est allum�.
* La TV est allum�e, elle affiche le Desktop du PI.


### Allumer la remote
* Allumer la remote... (bouton on/off sur la droite vers le haut).

### V�rification
* Le voyant bleu s'affiche, et puis disparait apr�s quelques secondes.


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

### V�rifications

* Si le programme tourne, l'�cran de TV devrait afficher quelque chose.
* Si l'�cran est noir, v�rifier que la TV est bien allum�e, et est bien sur l'input HDMI.
* Si l'�cran est toujours noir, v�rifier la sortie du programme...
  
  - Solutions possibles : la remote n'est pas allum�e : allumer la.
  
  - O� bien celle-ci a �t� desynchronis�e : Lancer "bluetoothctl"...

