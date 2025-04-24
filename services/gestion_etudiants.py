from models.etudiant import Etudiant
from models.note import Note
from services.gestion_notes import GestionNote
from services.db import MongoService
from services.redis_cache import RedisCache
import json
import pandas as pd
from fpdf import FPDF

class GestionEtudiants:
    def __init__(self):
        self.db = MongoService()
        self.cache = RedisCache()
        self.noteService = GestionNote()

    def ajouter_etudiant(self, nom, prenom, telephone, classe):
        if self.db.etudiants.find_one({"telephone": telephone}):
            print("❌ Téléphone déjà utilisé !")
            return

        notes = GestionNote.ajouterNoteClasse(classe)
        etudiant = Etudiant(nom, prenom, telephone, classe, notes)
        etudiant_data = etudiant.to_dict()

        self.db.etudiants.insert_one(etudiant_data)

        self.cache.set_etudiant(telephone, etudiant_data)

        print("✅ Étudiant ajouté avec succès !")

    def lister_etudiants(self):
        etudiants = self.cache.get_etudiants()
        
        if etudiants:
            print("✅ Étudiants récupérés depuis Redis")
        else:
            print("⚠️ Étudiants non trouvés dans Redis, récupération depuis MongoDB...")
            etudiants = list(self.db.etudiants.find({}, {'_id': 0}))
            if etudiants:
                self.cache.set_etudiants_bulk(etudiants)

        if not etudiants:
            print("Aucun étudiant trouvé.")
            return

        for etu in etudiants:
            print(f"{etu['nom']} {etu['prenom']} | Classe : {etu['classe']} | Moyenne : {etu['moyenne']}")

    def modifier_notes(self, telephone, matiere, note):
        etudiant = self.db.etudiants.find_one({"telephone": telephone})

        if not etudiant:
            print("❌ Étudiant non trouvé.")
            return

        anciennes_notes = etudiant.get("notes", [])
        
        nouvelles_notes = []
        note_trouvee = False

        for n in anciennes_notes:
            if n["libelle"] == matiere:
                nouvelles_notes.append({"libelle": matiere, "valeur": note})
                note_trouvee = True
            else:
                nouvelles_notes.append(n)

        if not note_trouvee:
            print("❌ Cette matiere n'est pas disponible.")

        moyenne = sum(n["valeur"] for n in nouvelles_notes) / len(nouvelles_notes)

        result = self.db.etudiants.update_one(
            {"telephone": telephone},
            {"$set": {"notes": nouvelles_notes, "moyenne": moyenne}}
        )

        if result.matched_count == 0:
            print("❌ Mise à jour échouée.")
            return

        print("✅ Notes modifiées avec succès.")

    def supprimer_etudiant(self, telephone):
        result = self.db.etudiants.delete_one({"telephone": telephone})
        if result.deleted_count == 0:
            print("❌ Étudiant non trouvé.")
            return

        self.cache.delete_etudiant(telephone)
        print("✅ Étudiant supprimé avec succès.")

    def rechercher_etudiant(self, champ, valeur):
        if champ not in ["nom", "prenom", "telephone", "classe"]:
            print("❌ Champ de recherche invalide.")
            return

        query = {champ: {"$regex": f"^{valeur}", "$options": "i"}}
        resultats = list(self.db.etudiants.find(query, {'_id': 0}))

        if resultats:
            for etu in resultats:
                print(f"{etu['nom']} {etu['prenom']} | Tél : {etu['telephone']} | Classe : {etu['classe']} | Moyenne : {etu['moyenne']}")
        else:
            print("Aucun étudiant trouvé.")

    def trier_etudiants_par_moyenne(self):
        etudiants = list(self.db.etudiants.find({}, {'_id': 0}).sort("moyenne", -1))
        if not etudiants:
            print("Aucun étudiant à trier.")
            return
        print("📊 Classement par moyenne :")
        for i, etu in enumerate(etudiants, start=1):
            print(f"{i}. {etu['nom']} {etu['prenom']} | Moyenne : {etu['moyenne']}")

    def exporter_donnees(self, format="csv"):
        etudiants = list(self.db.etudiants.find({}, {'_id': 0}))
        if not etudiants:
            print("Aucune donnée à exporter.")
            return

        df = pd.DataFrame(etudiants)

        if format == "csv":
            df.to_csv("etudiants.csv", index=False)
            print("✅ Données exportées vers etudiants.csv")
        elif format == "json":
            df.to_json("etudiants.json", orient="records", indent=2)
            print("✅ Données exportées vers etudiants.json")
        elif format == "excel":
            df.to_excel("etudiants.xlsx", index=False)
            print("✅ Données exportées vers etudiants.xlsx")
        elif format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Liste des étudiants", ln=True, align="C")

            for etu in etudiants:
                ligne = f"{etu['nom']} {etu['prenom']} | Tél: {etu['telephone']} | Classe: {etu['classe']} | Moyenne: {etu['moyenne']}"
                pdf.cell(200, 10, txt=ligne, ln=True)
            pdf.output("etudiants.pdf")
            print("✅ Données exportées vers etudiants.pdf")
        else:
            print("❌ Format non supporté.")

    def importer_donnees(self, fichier):
        try:
            if fichier.endswith(".csv"):
                df = pd.read_csv(fichier)
            elif fichier.endswith(".xlsx"):
                df = pd.read_excel(fichier)
            else:
                print("❌ Format non supporté.")
                return

            for _, row in df.iterrows():
                etudiant = {
                    "nom": row["nom"],
                    "prenom": row["prenom"],
                    "telephone": str(row["telephone"]),
                    "classe": row["classe"],
                    "notes": row["notes"] if isinstance(row["notes"], list) else eval(row["notes"]),
                    "moyenne": sum(eval(row["notes"])) / len(eval(row["notes"]))
                }
                try:
                    self.db.etudiants.insert_one(etudiant)
                    self.redis.set(etudiant["telephone"], json.dumps(etudiant))
                except:
                    print(f"⚠️ Étudiant {etudiant['nom']} {etudiant['prenom']} ignoré (téléphone en double ?)")
            print("✅ Importation terminée.")
        except Exception as e:
            print(f"❌ Erreur lors de l’importation : {e}")
