# assistant.py : répondre à une question en s'appuyant sur les fiches de recettes
import argparse
from openai import OpenAI
import config
from recettes import charger
from recherche import chercher, fiche

client = OpenAI(base_url=config.URL, api_key=config.CLE)

def repondre(question, recettes):
    """Rend la réponse à du modèle et les titres des fiches qu'on lui a données."""
    trouvees = chercher(question, recettes)
    if not trouvees:
        return "Aucune fiche ne correspond à votre question", []
    contexte = "CONTEXTE\n" + "\n\n".join(fiche(r) for r in trouvees)
    reponse = client.chat.completions.create(
        model=config.NOM,
        temperature=0,
        messages=[
            {"role": "system", "content": "Réponds uniquement à partir des fiches suivantes.\n" + contexte},
            {"role": "user", "content": question}
        ]
    )
    return reponse.choices[0].message.content, [r["titre"] for r in trouvees]

if __name__ == "__main__":
    parseur = argparse.ArgumentParser(description="Assistant de recette appuyé sur les fiches")
    parseur.add_argument("question", help="La question, entre guillemets")
    parseur.add_argument("--sources", action="store_true", help="affiche les fiches utilisées")
    args = parseur.parse_args()
    texte, titres = repondre(args.question, charger())
    print(texte)
    if args.sources:
      print("Fiches utilisées :", ", ".join(titres) or "aucune")