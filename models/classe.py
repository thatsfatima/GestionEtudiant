class Classe:
    def __init__(self, libelle, matieres):
        self.libelle = libelle
        self.matieres = matieres

    def to_dict(self):
        return {
            "libelle": self.libelle,
            "matieres": self.matieres
        }