# evaluer.py : mesurer le classment sur des questions dont on connaît la réponse
import csv
from collections import Counter
from classer import classer

with open("donnees/questions.csv", encoding="utf-8", newline="") as f:
    lignes = list(csv.DictReader(f, delimiter=";"))
print(len(lignes), "questions lues")

resultats = []
for ligne in lignes:
    c = classer(ligne["question"])
    obtenue = c.intention if c else "echec"
    resultats.append({
        "question": ligne["question"],
        "attendue": ligne["intention_attendue"],
        "obtenue": obtenue,
        "juste": obtenue == ligne["intention_attendue"],
    })

justes = sum(1 for r in resultats if r["juste"])
print(f"Exactitude : {justes}/{len(resultats)} = {justes/len(resultats):.0%}")

erreurs = Counter(r["attendue"] for r in resultats if not r["juste"])
print("Erreurs par intention attendue :", dict(erreurs))
for r in resultats:
    if not r["juste"]:
        print(f" {r['question']}\n   attendu {r['attendue']}, obtenu {r['obtenue']}")

with open("donnees/resultats.csv", "w", encoding="utf-8", newline="") as f:
    ecrivain = csv.DictWriter(f, fieldnames=["question", "attendue", "obtenue", "juste"], delimiter=";")
    ecrivain.writeheader()
    ecrivain.writerows(resultats)
print("Détails écrits dans donnees/resultats.csv")