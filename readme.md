# IMPORTANT  

Le script intitulé "main.py" ne fonctionne plus depuis une récente mise à jour de l'API d'EcoleDirecte.  
Le script intitulé "rewrite.py" est en cours de réecriture, il est adapté à la nouvelle API et fonctionnera donc au moins jusqu'a la prochaine mise a jour de celle-ci.  
Ce fichier est destiné à guider les personnes qui parcoureront cette branche du dépot, il vise à aider à en comprendre les différentes parties.  
Par conséquent il se doit d'être maintenu à jour à chaque modification.  
Pour ce projet on utilisera différentes librairies ainsi qu'une documentation non officielle de l'API d'EcoleDirecte disponible [ici](https://github.com/EduWireApps/ecoledirecte-api-docs).  
Le développement se fera en Python 3.9.  
Les librairies utilisées jusqu'a présent sont :  

- requests  
- json  
- datetime  

## SIMPLIFICATIONS ET TERMES TECHNIQUES  

A des fins de simplification, EcoleDirecte sera à partir de maintenant appelé 'ED'.  
L'ID du compte (appelé userID dans le programme) est un code à 4 chiffres permettant d'identifier l'utilisateur sans son nom, il est récupéré dans la réponse de la requête de connexion et, couplé au token, permet d'acceder aux modules d'ED.  
Les modules d'ED sont en fait les onglets disponibles sur le site officiel ou l'application (exemple : les notes, l'EDT, etc...)  
Termes techniques :  

- API  : L'API est une solution informatique qui permet à des applications de communiquer entre elles et de s'échanger mutuellement des services ou des données.
- JSON : (JavaScript Objet Notation) est un langage léger d'échange de données textuelles. Pour les ordinateurs, ce format se génère et s'analyse facilement. Pour les humains, il est pratique à écrire et à lire grâce à une syntaxe simple et à une structure en arborescence.  
- Parsing : (Anglicisme informatique) Parcourir le contenu d'un texte ou d'un fichier en l'analysant pour vérifier sa syntaxe ou en extraire des éléments.  
- Pretty printing : Afficher du code (dans notre cas du code JSON) d'une façon plus lisible, par exemple en le formatant, en y ajoutant de la couleur ou des retraits.  
- Token : Un token d'authentification (ou token de sécurité) est un dispositif matériel ou logiciel nécessaire à un utilisateur pour accéder à une application ou à un système réseau de manière plus sécurisée. Dans notre cas ce sont des chaînes de caractères longues et aléatoires.  
- Header : Un en-tête HTTP (header) est un champ d’une requête ou d’une réponse HTTP qui transmet un contexte et des métadonnées supplémentaires sur la requête ou la réponse.  
- User-Agent : L'User-Agent est un champ d'en-tête de requête HTTP (header) permettant au serveur, a l'API, ou a tout service receptionnant la requête de savoir quel systeme se trouve derriere celle-ci. Il indique en général, le systeme d'exploitation, la version de celui-ci, le navigateur ainsi que la version de celui-ci, etc...  

## MISE A JOUR DE L'API  

L'API d'ED a récemment été mise à jour, quelques modifications ont été apportées au format requis pour la connexion.  
2 (deux) champs supplémentaires sont désormais obligatoires : 'uuid' ainsi que 'isReLogin'.  
Si ces 2 (deux) champs ne sont pas fournis dans la requête, celle-ci échouera avec le code d'erreur 40129.  
L'API d'ED vérifie maintenant également l'user-agent afin de s'assurer qu'il s'agit d'un navigateur valide qui effectue la requête. Il est possible de contourner cette restriction en précisant un user-agent dans l'en-tête (header) de la requête. Un user-agent sera donc utilisé a chaque requête de l'API, dans le cas ou il est absent, l'API retournera soit le code d'erreur 40129, soit le code d'erreur 520 (constatés jusqu'a présent).  

## CODES D'ERREURS  

Ces codes d'erreurs sont tirés de la documentation non officielle de l'API citée au début de ce document, ils sont inscrits ici afin de faciliter la compréhension de ce document.  
- 505 : Les identifiants donnés à l'api sont erronés.  

- 520 : Le token est invalide.  

- 525 : Le token est expiré.  

- 40129 : Format JSON invalide.  

## MILESTONES  

### GENERALES  

:heavy_check_mark: - Possibilité de se connecter  
:heavy_check_mark: - Données du compte  
:heavy_check_mark: - Parse le JSON  
:heavy_check_mark: - Pretty print le JSON  
:heavy_check_mark: - Stocker le Token dans une variable  
:heavy_check_mark: - Prise en charge des codes d'erreurs HTTP sur la requete de connexion  
:heavy_check_mark: - stocker l'userID dans une variable  
:heavy_check_mark: - renvoyer les requetes web avec le token (dans le header de la requete)  
:heavy_check_mark: - Prise en charge des codes d'erreurs HTTP sur les autres requetes (vers les modules)  
:heavy_check_mark: - Fusionner le fichier de connexion et le fichier d'accès aux modules d'ED  
:x: - Parse le JSON (découper les données de la requete pour les avoir une par une)  
:x: - Afficher sur la page web du projet  

### MODULES  

:heavy_check_mark: - Connexion  
:heavy_check_mark: - Timeline  
:heavy_check_mark: - Emploi du temps  
:heavy_check_mark: - Vie scolaire  
:heavy_check_mark: - Notes  
:x: - Cahier de textes  
:x: - Messagerie  
:x: - Carnet de correspondance  
:x: - Badge cantine  
:x: - Portails E-sidoc  

## UTILISATION DES FONCTIONS (MODULES)  

Cette partie permet d'expliquer comment s'utilisent les modules du script "rewrite.py".  
Certains modules sont décrits dans la documentation non officielle citée plus haut, les autres seront étudiés grace à l'onglet Réseau de l'inspecteur web.  
- connexion(identifiant, motdepasse) : permet de se connecter, de récuperer un userID et un token (indispensables pour la suite).  
- timeline() : permet de récuperer la timeline (liste d'évènements sur le coté de la page d'accueil).  
- EDT(dateDebut, dateFin, avecTrous:bool) : permet de récuperer l'emploi du temps entre les deux dates données. avecTrous=True permet d'afficher un "cours" PERMANENCE sur les heures libres de l'élève, avecTrous=False n'affichera rien sur les heures libres.  
- vieScolaire() : permet d'afficher les absences et sanctions.  
- notes() : permet d'afficher les notes et moyennes par matières.  
- cahierDeTexte() : Ne fonctionne pas pour l'instant, renvoie une page html de chargement car le module utilise plusieurs scripts javascript pour fonctionner.  
Le reste des modules sont soit inutiles, soit inaccessibles a cause de leur fonctionnement / conception.  

## INFORMATIONS SUR LES FICHIERS  

- main.py : ancien script pour l'ancienne API d'ED.    
- readme.md : fichier actuel, permettant la compréhension de cette partie du projet.     
- rewrite.py : réecriture complète du script a des fins d'optimisation et afin qu'il fonctionne avec la nouvelle version de l'API.  

# REMERCIEMENTS  

Un grand merci pour leur aide précieuse dans certains moments critiques à :  
- [florian-lefebvre#1325](https://discordapp.com/users/371564915414007809)  
- [MaitreRouge#6916](https://discordapp.com/users/300910791362740224)  
- [JsonLines#6725](https://discordapp.com/users/295910954305191936)  
- [arossfelder#0454](https://discordapp.com/users/774970245156438066)  
- [El_will64#3283](https://discordapp.com/users/475424371507462145)  
