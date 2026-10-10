""""
À vous (E14)
Le jeu de questions est-il équilibré ? Dans un nouveau fichier compter.py , lisez donnees/questions.csv et
affichez, avec Counter , le nombre de questions par intention attendue. Quelle intention est la moins
représentée ?

"""

import csv
from collections import Counter

with open("donnees/questions.csv", encoding="utf-8", newline="") as f:
    lignes = list(csv.DictReader(f, delimiter=";"))
print(Counter(ligne["intention_attendue"] for ligne in lignes))

# L'intention la moins représentée est 'autre' avec 2 questions sur 20.
