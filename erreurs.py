# erreurs.py : provoquer une erreur, lire le message, puis le rattraper
import json
import recettes

try:
  toutes = recettes.charger("donnees/recette.json")
except FileNotFoundError as err:
  print("Fichier introuvable :", err.filename)
  toutes = recettes.charger()
print(len(toutes), "recettes chargées")

premiere = toutes[0]
try:
  print(premiere["difficulte"])
except KeyError as err:
  print("Clé manquante :", err)

texte_recu = '{"intention": "conservation", "confiance": 0.9,}'

try:
    donnees = json.loads(texte_recu)
except json.JSONDecodeError as err:
    print("JSON invalide :", err.msg, "à la position", err.pos)

try:
    recettes.filtrer_par_temps(toutes, -5)
except ValueError as err:
    print("Valeur refusée :", err)


try:
    int("trente")
except ValueError as err:
    print("Nombre illisible :", err)