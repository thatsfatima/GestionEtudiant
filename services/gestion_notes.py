from models.note import Note
from services.gestion_classe import GestionClasse
from services.db import MongoService

class GestionNote:
    def __init__(self):
        self.db = MongoService()
        classe = GestionClasse()

    def ajouterNoteClasse(self, libelle):
        classeNote = self.classe.findClasse(libelle)
        tabNotes = []
        if classeNote and "matieres" in classeNote:
            for matiere in classeNote["matieres"]:
                tabNotes.append(Note(matiere, 0))
            return tabNotes