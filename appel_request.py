# appel_requests.py : parler au modèle avec de simples requêtes HTTP
import requests
import config

# r = requests.get(f"{config.URL}/models",
#                  headers={"Authorization": f"Bearer {config.CLE}"}, 
#                  timeout=10)

# r = requests.get(f"{config.URL}/models", timeout=10)
# print("Code HTTP :", r.status_code)
# print("Corps :", r.json())

def demander(question, temperature=0.7):
  """Envoie une question au modèle et rend le JSON de sa réponse."""
  r = requests.post(
    f"{config.URL}/chat/completions",
    headers={"Authorization": f"Bearer {config.CLE}"},
    json={
      "model": config.NOM,
      "messages": [{"role": "user", "content": question}],
      "temperature": temperature,
      },
      timeout=10,
      )
  r.raise_for_status()
  return r.json()

if __name__ == "__main__":
  try:
    donnees = demander("Par quoi remplacer le beurre dans une tarte ?")
    print("Réponse :", donnees["choices"][0]["message"]["content"])
    print("Jetons :", donnees["usage"])

    donnees = demander("Est-ce que le gratin se congèle ?", temperature=0)
    print("Réponse :", donnees["choices"][0]["message"]["content"])
    print("Jetons :", donnees["usage"])

  except requests.ConnectionError:
    print("Le modèle ne répond pas : est-il lancé dans l'autre terminal ?")
  except requests.HTTPError as err:
    print("Le modèle a refusé la requête :", err.response.status_code, err.response.json()["error"]["message"])


# La question "Est-ce que le gratin se congèle ?" a coûté 8 jetons et la réponse 20 jetons.