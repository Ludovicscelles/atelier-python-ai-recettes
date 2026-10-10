# appel_sdk.py : le même appel avec le SDK officiel openai

from openai import OpenAI
import config

client = OpenAI(base_url=config.URL, api_key=config.CLE)

reponse = client.chat.completions.create(
    model=config.NOM,
    messages=[
      {"role": "system", "content": "Tu es l'assistant d'un site de recettes."},
      {"role": "user", "content": "Combien de jours garder une soupe au frigo ?"},
    ],
    temperature=0,
)
print("Type de l'objet", type(reponse).__name__ )
print("Réponse :", reponse.choices[0].message.content)
print("Jetons :", reponse.usage.prompt_tokens, "+", reponse.usage.completion_tokens, "=", reponse.usage.total_tokens)

print()
historique = [{"role": "system", "content": "Tu es l'assistant d'un site de recettes."}]
for question in [
    "Je n'ai plus de crème, je mets quoi ?", 
    "Et pour la conserver ?", 
    "Et si un invité est allergique aux arachides ?"
    ]:
    historique.append({"role": "user", "content": question})
    rep = client.chat.completions.create(
        model=config.NOM,
        messages=historique,
    )
    texte = rep.choices[0].message.content
    historique.append({"role": "assistant", "content": texte})
    print(f"Vous : {question}")
    print(f"Modèle : {texte}")
print("Messages envoyés au dernier appel :", len(historique) -1, "messages")

# A la question "Et si un invité est allergique aux arachides ?" 
# le modèle répond
# "Vous pouvez remplacer les arachides par des noix de cajou, des amandes ou des graines de tournesol."
# 6 messages sont partis au dernier appel :
# 1 message système + 3 questions + 2 réponses précédentes du modèle.