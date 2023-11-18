
## Script Python tri de Fichier

Voici mon script python qui permet de trier les fichier en fonction des extensions de fichier et de créer un log qui conserve un historique des tris 

## **Utiliser le script:**
```
usage: main.py [-h] --dir DIR [--list-files] [--sort-files]

FileSorter | Version: 2023.10#v1

optional arguments:
  -h, --help         show this help message and exit

Scan Methods:
  --list-files, -lf  List files of the specified path
  --sort-files, -sf  Sort files from categories (see data.json)

Main options:
  --dir DIR, -d DIR  Specify a PATH
```
## **exemple d'utilisation**
 python3 main.py -d . -sf --> tri les fichiers du directory actuel <br>
 python3 main.py -d . -lf --> affichage des fichiers du directory actuel
