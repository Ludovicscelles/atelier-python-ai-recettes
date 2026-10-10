# tests/test_recettes.py : vérifier le module recettes sans rien afficher
import pytest
from recettes import charger, filtrer_par_temps, chercher_ingredient

EXEMPLE = [
  {"titre": "A", "temps_min": 10, "ingredients": ["Oeufs", "lait"]},
  {"titre": "B", "temps_min": 40, "ingredients": ["farine"]}
]

def test_le_fichier_contient_15_recettes():
    assert len(charger()) == 15

def test_filtrer_garde_les_rapides():
    assert [r["titre"] for r in filtrer_par_temps(EXEMPLE, 20)] == ["A"]

def test_filtrer_inclut_la_limite():
    assert len(filtrer_par_temps(EXEMPLE, 40)) == 2

def test_filtrer_refuse_un_temps_negatif():
    with pytest.raises(ValueError):
        filtrer_par_temps(EXEMPLE, -1)

def test_chercher_ignore_les_majuscules():
    assert [r["titre"] for r in chercher_ingredient(EXEMPLE, "oeufs")] == ["A"]

def test_chercher_sans_resultat():
    assert chercher_ingredient(EXEMPLE, "chocolat") == []