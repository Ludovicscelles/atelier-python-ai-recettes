# test/test_classer.py : tester classer() sans appeler le modèle
from types import SimpleNamespace
import classer

class FauxClient:
    """Imite le client openai : rend des textes écrits d'avance et compte les appels."""

    def __init__(self, textes):
        self.textes = list(textes)
        self.appels = 0
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.appels += 1
        message = SimpleNamespace(content=self.textes.pop(0))
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

BON = '{"intention": "autre", "confiance": 0.5, "reponse": "ok"}'

def test_nettoyer_retirer_les_balises():
    assert classer.nettoyer("```json\n" + BON + "\n```") == BON

def test_une_reponse_valide_suffit():
    faux = FauxClient([BON])
    assert classer.classer("Bonjour", client=faux).intention == "autre"
    assert faux.appels == 1

def test_relance_apres_une_reponse_invalide():
    faux = FauxClient(["pas du JSON", BON])
    assert classer.classer("Bonjour", client=faux).intention == "autre"
    assert faux.appels == 2

def test_abandon_apres_trop_echecs():
    faux = FauxClient(["x", "y", "z"])
    assert classer.classer("Bonjour", client=faux) is None
    assert faux.appels == 3