import bcrypt
import uuid
import json

class Utilisateur:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
        self.collection = db.utilisateurs

    def creer_utilisateur(self, nom, prenom, telephone, mot_de_passe, role):
        if self.collection.find_one({"telephone": telephone}):
            print("❌ Utilisateur déjà existant.")
            return

        mot_de_passe_hash = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())

        utilisateur = {
            "nom": nom,
            "prenom": prenom,
            "telephone": telephone,
            "mot_de_passe": mot_de_passe_hash,
            "role": role
        }

        self.collection.insert_one(utilisateur)
        print("✅ Utilisateur créé avec succès.")

    def connecter(self, telephone, mot_de_passe):
        utilisateur = self.collection.find_one({"telephone": telephone})
        if utilisateur and bcrypt.checkpw(mot_de_passe.encode(), utilisateur["mot_de_passe"]):
            token = str(uuid.uuid4())
            self.redis.set(token, json.dumps({
                "telephone": utilisateur["telephone"],
                "role": utilisateur["role"],
                "nom": utilisateur["nom"],
                "prenom": utilisateur["prenom"]
            }), ex=3600)
            print(f"✅ Connexion réussie ({utilisateur['role']})")
            return token
        else:
            print("❌ Identifiants incorrects.")
            return None

    def get_session(self, token):
        session = self.redis.get(token)
        return json.loads(session) if session else None


