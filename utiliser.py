# utiliser.py : se servir du module recettes depuis un autre fichier
import recettes

toutes = recettes.charger()
choix = recettes.chercher_ingredient(toutes, "oeufs")
print(len(choix), "recettes avec des oeufs :")
for r in choix:
    print(" ", recettes.resumer(r))

from recettes import filtrer_par_temps, resumer, par_categorie


for r in filtrer_par_temps(choix, 20):
    print("Rapide et avec des oeufs :", resumer(r))

for r in recettes.par_categorie(toutes, "entree"):
    print("Entrée :", recettes.resumer(r))

for r in par_categorie(toutes, "entree"):
    print("Entrée :", resumer(r))


