# classer.py : demander un classement au modèle et ne croire que ce qui est valide
import logging
from openai import OpenAI
from pydantic import ValidationError
import config
from schemas import Classement

CONSIGNE = ("Tu classes la question d'un utilisateur de site de recettes."
            "Réponds uniquement en JSON avec les clés 'intention', 'confiance' et 'reponse'.")

journal = logging.getLogger(__name__)
CLIENT = OpenAI(base_url=config.URL, api_key=config.CLE)

def nettoyer(texte):
    """Retire les défauts de forme connus du modèle."""
    texte = texte.strip()
    if texte.startswith("```"):
        texte = texte.strip("`").removeprefix("json").strip()
    return texte.replace(",}", "}")

def classer(question, essais=3, client=None):
    """Rend un Classement valide, ou None après plusieurs essais ratés."""
    client = client or CLIENT
    for essai in range(1, essais + 1):
        reponse = client.chat.completions.create(
            model=config.NOM,
            temperature=0,
            messages=[
                {"role": "system", "content": CONSIGNE},
                {"role": "user", "content": question},
            ]
        )
        brut = reponse.choices[0].message.content
        try:
            return Classement.model_validate_json(nettoyer(brut))
        except ValidationError as err:
            journal.info("Essai %d rejeté (%d erreur) : %s", essai, err.error_count(), brut)
    journal.warning("abandon après %d essais : %s", essais, question)
    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    journal.setLevel(logging.INFO)
    for question in [
        "Est-ce que le gratin se congèle ?",
        "On m'a prélevé deux fois mon abonnement",
        "Je suis allergique aux arachides, je peux faire ce gâteau ?",
        "Comment réchauffer un reste de risotto ?",
        "Vous livrez à Lyon ?",
    ]:
        c = classer(question)
        print(f"{question}\n {c.intention} ({c.confiance}) : {c.reponse}")