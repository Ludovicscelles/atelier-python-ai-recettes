# bases.py : les types de base de Python, sur une recette

# variables de base
print()
print("Début des variables base")

titre = "Crêpes"
temps_min = 30
note = 4.5
vegetarien = True

print("Début des variables base")

print(titre, "se prépare en", temps_min, "minute.")
print(type(titre), type(temps_min), type(note), type(vegetarien))
print(f"Note : {note} sur 5, végétarien : {vegetarien}")

print("Fin des variables base")
print()

# liste d'ingrédients

print("Début des ingrédients")


ingredients = ["farine", "lait", "oeufs", "sucre", "beurre"]
print("Nombre d'ingrédients :", len(ingredients))
print("Premier ingrédient :", ingredients[0], "dernier ingrédient :", ingredients[-1])
ingredients.append("sucre vanillé")
print("Après ajout d'un ingrédient :", ingredients)
print("Les deux premiers ingrédients :", ingredients[:2])
print("Du lait dedans ?", "lait" in ingredients)

print("Fin des ingrédients")
print()
# dictionnaire d'ingrédients


print("Début Recette")
print()


recette = {
    "titre": "Crêpes",
    "temps_min": temps_min,
    "note": note,
    "vegetarien": vegetarien,
    "ingredients": ingredients,
    "difficulte": "facile"
  
}
print()
print("Clé :", list(recette.keys()))
print("Temps lu dans le dictionnaire :", recette["temps_min"])
recette["portions"] = 4
print("Après ajout d'une clé :", recette)
print("Portions :", recette["portions"])
print("Difficulté :", recette.get("difficulte", "non renseignée"))

# Conditions et boucles

print("Début des conditions et boucles")
print()

if temps_min <= 20:
    rythme = "express"
elif temps_min <= 45:
    rythme = "rapide"
else:
    rythme = "long"
print("Rythme :", rythme)

for numero, ingredient in enumerate(ingredients, start=1):
    print(f"{numero} - {ingredient}")

print("Fin des conditions et boucles")
print()




print()

def resumer(titre, temps_min, portions=4):
    """Rend une ligne de présentation de la recette"""
    return f"{titre} ({temps_min} min, {portions} portions)"

print("Résumé :", resumer(titre, temps_min))
print(resumer("Glace", 15))
print(resumer("Cheesecake", 90, portions=8))

def est_rapide(temps_min, seuil=20):
    return temps_min <= seuil

print("Est rapide ?", est_rapide(15))
print("Est rapide ?", est_rapide(30))
print("Est rapide ?", est_rapide(30, seuil=45))


print("Difficulté :", recette.get("difficulte", "non renseignée"))
