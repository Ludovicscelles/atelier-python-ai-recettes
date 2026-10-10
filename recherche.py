# recherche.py : retrouver les recettes les plus proches d'une question
import re
import unicodedata
from recettes import charger

MOTS_VIDES = {"les", "des", "une", "est", "pour", "avec", "dans", "comment", "combien",
              "faire", "quoi", "que", "qui", "mon", "mes", "peux", "faut", "sans", "temps"}


def mots(texte):
    """Rend l'ensemble des mots utiles d'un texte, sans accents ni majuscules"""
    texte = unicodedata.normalize('NFD', texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c)) 
    return {m for m in re.findall(r"[a-z]+", texte) if len(m) >= 3 and m not in MOTS_VIDES}

def chercher(question, recettes, k=3):
    """Rend au plus k recettes , de la plus proche à la moins proche"""
    q = mots(question)
    notes = []
    for r in recettes:
        score = len(q & mots(r["titre"] + " " + " ".join(r["ingredients"])))
        if score > 0:
            notes.append((score, r))
    notes.sort(key=lambda pair: pair[0], reverse=True)
    return [r for _, r in notes[:k]]

def fiche(recette):
    """Met une recette au format texte que le modèle lira."""
    return (f"### {recette['titre']}\n"
            f"temps : {recette['temps_min']}\n"
            f"ingredients : {', '.join(recette['ingredients'])}")

if __name__ == "__main__":
    toutes = charger()
    print(mots("Combien de temps pour faire Crêpes ?"))
    for question in ["J'ai des champignons et du riz", 
                     "Combien de temps pour les crêpes ?",
                     "Vous livrez à Lyon ?",
                     "Quelles sont les recettes vegan ?"
                     ]:
        print(question, "=>", [r["titre"] for r in chercher(question, toutes)])
    print(fiche(toutes[12]))