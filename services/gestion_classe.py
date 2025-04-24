from models.classe import Classe
from services.db import MongoService

class GestionClasse:
    def __init__(self):
        self.db = MongoService()

    def ajouterClasse(self, libelle, matieres):
        if self.db.classes.find_one({"libelle": libelle}):
            print("❌ Classe existe déjà !")
            return

        classe = Classe(libelle, matieres)
        classe_data = classe.to_dict()

        self.db.classes.insert_one(classe_data)

        print("✅ Classe ajouté avec succès !")

    def findClasse(self, libelle):
        classe = self.db.classes.find_one({"libelle": libelle})
        if classe:
            return {
                "libelle": classe["libelle"],
                "matieres": classe["matieres"]
            }