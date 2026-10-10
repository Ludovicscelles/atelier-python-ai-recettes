# verifier.py : dit quel Python tourne et quelles bibliothèques sont installées

import sys
from importlib.metadata import version, PackageNotFoundError

print("Python version:", sys.version.split()[0])
print("Interpréteur:", sys.executable)
print("Environnement virtuel actif:", sys.prefix != sys.base_prefix)

for nom in ["requests", "python-dotenv", "pydantic", "pytest", "openai"]:
    try:
        print(f"  {nom:<14} : {version(nom)}")
    except PackageNotFoundError:
        print(f"  {nom} absent")
