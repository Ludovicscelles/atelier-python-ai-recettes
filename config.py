"""Lit la configuration du projet depuis le fichier .env, jamais dans le code"""

import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("MODELE_URL", "http://127.0.0.1:8000/v1")
CLE = os.getenv("MODELE_CLE")
NOM = os.getenv("MODELE_NOM", "modele-local")
TEMPERATURE = float(os.getenv("MODELE_TEMPERATURE", 0.7))

if __name__ == "__main__":
    print("URL :", URL)
    print("Nom :", NOM)
    print("Clé :", CLE[:6] + "..." if CLE else "absente")
    print("Température :", TEMPERATURE, "type", type(TEMPERATURE).__name__)