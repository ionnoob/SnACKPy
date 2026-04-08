# SnACKPy
codes basiques pour simuler deux utilisateurs qui s'échange des message avec verif SNACK

Rapport :
Exercice 1.
Dans cet exercice nous avons utilisé wireshark afin d’observer un échange de paquet
entre deux « peer » utilisant le protocole UDP.
En effet nous pouvons voir grâce à wireshark que le premier « peer » que nous
nommerons « peer1 » a envoyé un paquet de length 46, depuis l’adresse
127.0.0.1(Loopback) et le port 60234 vers le port 5005.
Le paquet était de 4 bytes.
Le deuxième peer(peer2) a envoyé un paquet de length 46, depuis l’adresse 127.0.0.1 et
le port 5005 vers 60234, en ayant pris 13 secondes pour répondre. Le paquet était aussi
de 4 bytes.
La length 46 peux être expliquée par le protocole utilisé (UDP) qui contient 42 bytes
sans les données qui ici sont à 4.
Il n’y a pas de carte réseau car nous utilisons le loopback et donc nous n’avons pas de
destination mac.
On peut clairement lire le message avec le wireshark, nous indiquant que le protocole
UDP ne chiffre rien, ce qui ajoute un risque de sniffing.
Exercice 2 .
Chaque message envoyé contient le texte du message (DATA), un numéro de séquence
(SN) et la longueur du message (LEN). Le récepteur envoie un ACK avec le SN
correspondant au message reçu.
Logique côté émetteur (Peer1) :
Le peer initialise un numéro de séquence aléatoire.
Lorsqu’un utilisateur saisit un message, le peer crée un paquet DATA incluant le
message, le SN actuel et la longueur.
Le peer envoie ce paquet au pair destinataire.
Après envoi, le peer attend un ACK correspondant au SN envoyé.
Si l’ACK est correct, le peer affiche « ACK correct » et incrémente le SN pour le prochain
message.
Si l’ACK est incorrect, le peer affiche « ACK incorrect ».
Logique côté récepteur (Peer2) :
Le peer écoute en permanence sur son socket UDP.
Lorsqu’un paquet DATA est reçu, il extrait le SN et la longueur et affiche le message reçu
avec ces informations.
Il vérifie si le SN correspond au numéro attendu. Si correct, le message est accepté et
affiché ; sinon, il peut être ignoré.
Le peer envoie un ACK correspondant au SN reçu.
Le SN attendu pour le prochain message est incrémenté.
Exercice 3.
Le protocole implémenté est de type Stop-and-Wait ARQ.
Le fonctionnement est le suivant :
• un pair envoie un paquet DATA
• il attend un accusé de réception ACK
• si l’ACK est reçu, il envoie le paquet suivant
• sinon, il retransmet le même paquet
Chaque paquet contient un numéro de séquence (SN), la longueur du message et les
données.
Lors de l’envoi d’un message, le pair crée un paquet de la forme
DATA|SN|LEN|MESSAGE. Il envoie ce paquet, puis il le stocke en mémoire et démarre
un timer. Le programme passe alors en attente d’un ACK.
Lors de la réception d’un message DATA, le pair affiche le message puis envoie un ACK
contenant le numéro de séquence reçu.
Lors de la réception d’un ACK, le pair vérifie si le numéro correspond à celui du paquet
envoyé. Si c’est le cas, l’ACK est validé, le numéro de séquence est incrémenté et le
programme peut envoyer un nouveau message. Sinon, l’ACK est ignoré.
Un timer de 5 secondes est utilisé.
Si aucun ACK n’est reçu avant la fin du timer, le paquet est retransmis. Le timer est alors
relancé. Ce mécanisme permet de garantir que les messages finissent toujours par être
reçus, même en cas de perte.
Exercice 4.
1)
Google a créé QUIC pour améliorer les performances du web, notamment en réduisant
la latence des connexions. Les protocoles classiques comme TCP et TLS nécessitent
plusieurs échanges avant de commencer à transmettre les données, ce qui ralentit le
chargement des pages.
QUIC utilise UDP et intègre directement la sécurité et la gestion de la connexion, ce qui
permet d’établir une connexion beaucoup plus rapidement. Il a donc été conçu pour
accélérer le web tout en conservant un haut niveau de sécurité.
2)
Ce TP est similaire à QUIC car il reconstruit, au-dessus d’UDP, des mécanismes
normalement présents dans TCP.
Comme QUIC, on utilise UDP mais on ajoute :
• un système de numéros de séquence
• des accusés de réception (ACK)
• une retransmission en cas de perte (timeout)
Cela correspond à l’idée principale de QUIC : rendre UDP fiable en implémentant soi-
même les mécanismes de transport.
3)
Le TP reste une version très simplifiée. Il manque plusieurs éléments essentiels
présents dans QUIC :
• gestion de plusieurs paquets en parallèle (pas seulement Stop-and-Wait)
• contrôle de congestion et adaptation au réseau
• chiffrement des données (sécurité intégrée)
• multiplexage de plusieurs flux en même temps
• correction d’erreurs avancée
• optimisation des performances et du débit
QUIC est un protocole complet qui intègre tous ces mécanismes, alors que le TP n’en
implémente qu’une petite partie.
4)
Ce TP permet de comprendre concrètement comment fonctionne la fiabilité dans les
réseaux.
Il montre que UDP seul n’est pas fiable, et qu’il faut ajouter des mécanismes comme
les ACK et les timeouts pour garantir la transmission.
Il permet aussi de comprendre comment des protocoles modernes comme QUIC ou
TCP fonctionnent en interne, et que ces protocoles ne font finalement qu’automatiser
des mécanismes que l’on peut implémenter soi-même.
Enfin, ce TP donne une vision pratique des problèmes réels des réseaux, comme la
perte de paquets et la nécessité de retransmission.
