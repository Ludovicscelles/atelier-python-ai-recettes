"""Lire le fichier de recettes et y chercher"""

import json
from pathlib import Path

FICHIER = Path(__file__).parent / "donnees" / "recettes.json"

def charger(chemin=FICHIER):
    """Renvoie la liste des recettes lue dans le fichier JSON"""
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)

def filtrer_par_temps(recettes, maxi):
    """Rend les recettes prêtes en maxi minutes ou moins"""
    if maxi <= 0:
        raise ValueError(f"maxi doit être positif, reçu {maxi}")
    return [r for r in recettes if r["temps_min"] <= maxi]

def chercher_ingredient(recettes, ingredient):
    """Rend les recettes dont un ingrédient contient le mot cherché"""
    cherche = ingredient.lower()
    trouvees = []
    for r in recettes:
        for i in r["ingredients"]:
            if cherche in i.lower():
                trouvees.append(r)
                break
    return trouvees

def resumer(recette):
    """Rend une ligne courte : titre et temps"""
    return f"{recette['titre']} ({recette['temps_min']} min)"

def par_categorie(recettes, categorie):
    """Rend les recettes de la catégorie donnée"""
    categorie = categorie.lower()
    return [r for r in recettes if r["categorie"] == categorie]



if __name__ == "__main__":
    toutes = charger()
    print(len(toutes), "recettes chargées") 
    for r in filtrer_par_temps(toutes, 20):
        print(" ", resumer(r))
    print("Avec des champignons :", [resumer(r) for r in chercher_ingredient(toutes, "Champignons")])


