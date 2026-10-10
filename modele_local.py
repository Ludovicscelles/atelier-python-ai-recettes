# -*- coding: utf-8 -*-
"""Modèle local de l'atelier Python, Dev IA appliqué, M1 LDFS.

Il se comporte comme l'API de chat d'un fournisseur (même route, même format
de question, même format de réponse que OpenAI) mais tourne sur votre machine,
sans réseau vers l'extérieur. Vous ne le modifiez jamais.

    python modele_local.py          # écoute sur http://127.0.0.1:8000/v1

Ce qu'il sait faire :
  - refuser un appel sans clé (erreur 401), comme un vrai fournisseur. Il accepte
    n'importe quelle clé qui commence par "sk-" ;
  - classer une question de cuisine et répondre en JSON quand on le lui demande.
    Environ un appel sur cinq, il rate le format exprès (balises ```, virgule
    en trop ou phrase avant le JSON) : c'est à votre programme de valider ;
  - répondre à partir de fiches qu'on lui donne dans un message "system" qui
    contient le mot CONTEXTE (c'est le principe du RAG) ;
  - compter des jetons approximatifs dans le champ usage.
"""
import json, random, time, hashlib, unicodedata, sys, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

NOM_MODELE = "modele-local"

REGLES = [
    ("recette_frigo",     ["frigo", "j'ai des", "je fais quoi", "ce soir", "idee", "diner", "avec quoi", "il me reste"]),
    ("substitution",      ["a la place", "remplacer", "je n'ai pas", "je n'ai plus", "mettre quoi", "substitu", "a defaut"]),
    ("cuisson_technique", ["cuire", "cuisson", "colle", "le cuis", "brule", "combien de temps", "au four", "rate"]),
    ("conservation",      ["congel", "garder", "conserver", "deja cuit", "rechauffer", "combien de jours", "restes"]),
    ("allergie_sante",    ["allerg", "arachide", "gluten", "lactose", "sans risque", "intoleran", "enceinte", "diabet"]),
    ("compte_abonnement", ["abonnement", "preleve", "deux fois", "rembours", "mot de passe", "resilier", "facture", "mon compte"]),
]
REPONSES = {
    "recette_frigo":     "Dites-moi ce qu'il reste dans votre frigo et le temps que vous avez : je vous propose un plat avec ces ingrédients.",
    "substitution":      "La plupart des ingrédients se remplacent : dites-moi lequel manque et dans quelle recette.",
    "cuisson_technique": "Les fiches donnent le temps et la température de cuisson de chaque plat.",
    "conservation":      "La plupart des plats cuits se gardent trois jours au frais, dans une boîte fermée.",
    "allergie_sante":    "Je ne peux pas garantir qu'une recette est sans risque pour une allergie : un humain vous répond.",
    "compte_abonnement": "Une question de compte ou de paiement est traitée par l'équipe du site.",
    "autre":             "Je transmets votre question à l'équipe du site.",
}
SENSIBLES = {"allergie_sante", "compte_abonnement"}


def _jetons(txt):
    return max(1, round(len(txt) / 4))


def _simple(s):
    s = unicodedata.normalize("NFD", s.lower().replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c))


def classer(message, temperature, graine):
    m = _simple(message)
    rng = random.Random(graine)
    meilleur, score = "autre", 0
    for intention, mots in REGLES:
        n = sum(1 for mot in mots if _simple(mot) in m)
        if n > score:
            meilleur, score = intention, n
    base = {0: 0.28, 1: 0.72, 2: 0.88}.get(score, 0.93)
    bruit = rng.uniform(-0.09, 0.09) * (temperature / 0.7 if temperature else 0)
    confiance = round(min(0.99, max(0.05, base + bruit)), 2)
    return meilleur, confiance, REPONSES[meilleur]


def repondre_avec_contexte(question, contexte):
    """Cherche dans les fiches du contexte celle qui partage le plus de mots avec la question."""
    fiches = [f for f in re.split(r"\n(?=### )", contexte) if f.startswith("### ")]
    mots = {w for w in re.findall(r"[a-z]{4,}", _simple(question))}
    meilleure, score = None, 0
    for f in fiches:
        n = len(mots & set(re.findall(r"[a-z]{4,}", _simple(f))))
        if n > score:
            meilleure, score = f, n
    if meilleure is None:
        return "Je ne trouve pas cette information dans les fiches fournies."
    titre = meilleure.split("\n", 1)[0][4:].strip()
    temps = re.search(r"temps\s*:\s*(\d+)", meilleure)
    ingr = re.search(r"ingr[eé]dients\s*:\s*(.+)", meilleure)
    rep = "D'après la fiche « " + titre + " »"
    if temps:
        rep += ", comptez " + temps.group(1) + " minutes"
    if ingr:
        rep += ". Il vous faut : " + ingr.group(1).strip()
    return rep + "."


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        donnees = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)

    def _erreur(self, code, message, type_):
        self._json(code, {"error": {"message": message, "type": type_, "code": code}})

    def _cle_ok(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer sk-"):
            self._erreur(401, "Clé absente ou invalide. Envoyez l'en-tete Authorization: Bearer sk-...",
                         "authentication_error")
            return False
        return True

    def do_GET(self):
        if self.path.rstrip("/") != "/v1/models":
            self._erreur(404, "Route inconnue : " + self.path, "not_found"); return
        if not self._cle_ok():
            return
        self._json(200, {"object": "list", "data": [
            {"id": NOM_MODELE, "object": "model", "created": 1767225600, "owned_by": "atelier"}]})

    def do_POST(self):
        if self.path.rstrip("/") != "/v1/chat/completions":
            self._erreur(404, "Route inconnue : " + self.path, "not_found"); return
        if not self._cle_ok():
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            corps = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            self._erreur(400, "Le corps de la requête n'est pas du JSON valide.", "invalid_request_error"); return
        messages = corps.get("messages", [])
        if not isinstance(messages, list):
            self._erreur(400, "Le champ messages doit être une liste.", "invalid_request_error"); return
        temperature = float(corps.get("temperature", 0.7))
        user = next((x.get("content", "") for x in reversed(messages) if x.get("role") == "user"), "")
        if not user:
            self._erreur(400, "Aucun message de role user.", "invalid_request_error"); return
        systeme = " ".join(x.get("content", "") for x in messages if x.get("role") == "system")
        graine = int(hashlib.sha256(user.encode("utf-8")).hexdigest()[:8], 16)
        if temperature > 0:
            graine ^= int(time.time() * 1000) & 0xffff
        time.sleep(random.uniform(0.03, 0.12))

        if "CONTEXTE" in systeme:
            contenu = repondre_avec_contexte(user, systeme)
        else:
            intention, confiance, reponse = classer(user, temperature, graine)
            veut_json = "json" in systeme.lower() or "json" in user.lower()
            if not veut_json:
                contenu = reponse
            else:
                texte = json.dumps({"intention": intention, "confiance": confiance,
                                    "reponse": reponse}, ensure_ascii=False)
                accident = random.random()
                if accident < 0.10:
                    contenu = "```json\n" + texte + "\n```"
                elif accident < 0.16:
                    contenu = texte[:-1] + ",}"
                elif accident < 0.21:
                    contenu = "Voici le classement demandé : " + texte
                else:
                    contenu = texte
        pt = sum(_jetons(x.get("content", "")) for x in messages)
        ct = _jetons(contenu)
        self._json(200, {
            "id": "chatcmpl-" + format(graine, "x"),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": NOM_MODELE,
            "choices": [{"index": 0, "finish_reason": "stop",
                         "message": {"role": "assistant", "content": contenu}}],
            "usage": {"prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt + ct},
        })


if __name__ == "__main__":
    ThreadingHTTPServer.allow_reuse_address = sys.platform != "win32"
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", 8000), H)
    except OSError:
        print("Le port 8000 est déjà pris : un modèle local tourne sans doute déjà dans un autre terminal.")
        sys.exit(1)
    print("Modèle local prêt sur http://127.0.0.1:8000/v1  (Ctrl+C pour arrêter)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")
