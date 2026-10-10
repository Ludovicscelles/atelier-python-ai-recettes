# explorer.py : lire le fichier de recettes et en tirer des chiffres.

import json
from pathlib import Path

chemin = Path("donnees") / "recettes.json"
print("Chemin du fichier :", chemin)
print("Le fichier existe ?", chemin.exists())

with open(chemin, encoding="utf-8") as fichier:
    recettes = json.load(fichier)

print("Type lu", type(recettes).__name__)
print("Nombre de recettes :", len(recettes))
print("Première recette :", recettes[0])

print("Additionner dans un boucle")

total = 0
for r in recettes:
    total = total + r["temps_min"]

print(f"Temps moyen : {total / len(recettes):.1f} minutes")


print("Les compréhensions de liste")
print()

temps = [r["temps_min"] for r in recettes]
print("Plus court :", min(temps), "min, plus long :", max(temps), "min")

rapides = [r["titre"] for r in recettes if r["temps_min"] <= 20]
print("Prêtes en 20 minutes ou moins :", rapides)

print("Corriger le filtre, compter, trier")

vegetariennes = [r["titre"] for r in recettes
                if "vegetarien" in r["tags"] or "vegan" in r["tags"]]

print("Recettes végétariennes :", len(vegetariennes), (vegetariennes))

par_categorie = {}
for r in recettes:
    categorie = r["categorie"]
    par_categorie[categorie] = par_categorie.get(categorie, 0) + 1
print("Recettes par catégorie :", par_categorie)

def duree(recette):
    return recette["temps_min"]

triees = sorted(recettes, key=duree)
print("Les trois recettes les plus rapides :", [r["titre"] for r in triees[:3]])

"""
À vous (E6)
Dans explorer.py , 
affichez : la liste des recettes portant l'étiquette sans_gluten et leur nombre ; 
les desserts triés du plus rapide au plus long, avec leur temps ; 
le titre de la recette la plus longue, en une ligne, avec max et son paramètre key

"""

print()


sans_gluten = [r["titre"] for r in recettes if "sans_gluten" in r["tags"]]
print("Recettes sans gluten :", len(sans_gluten), sans_gluten)

desserts = sorted(
    [r for r in recettes if r["categorie"] == "dessert"], 
    key=lambda r: r["temps_min"]
    )
print("Desserts triés du plus rapide au plus long :", [(r["titre"], r["temps_min"]) for r in desserts])

print(max(recettes, key=lambda r: r["temps_min"])["titre"], "est la recette la plus longue à réaliser")

