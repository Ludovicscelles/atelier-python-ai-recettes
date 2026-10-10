"""Le format attendu d'une réponse de classement"""
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

Intention = Literal[
  "recette_frigo",
  "substitution", 
  "cuisson_technique", 
  "conservation", 
  "allergie_sante", 
  "compte_abonnement", 
  "autre"
  ]

class Classement(BaseModel):
    intention: Intention
    confiance: float = Field(ge=0, le=1)
    reponse: str

if __name__ == "__main__":
    bon = Classement(intention="conservation", confiance=0.88, reponse="Trois jours au frais.")
    print("Valide :", bon)
    print("Confiance :", bon.confiance, type(bon.confiance).__name__)
    try:
        Classement(intention="dessert", confiance=1.4, reponse="?")
    except ValidationError as err:
        print(err)