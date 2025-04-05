class Etudiant:
    def __init__(self, nom, prenom, telephone, classe, notes):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.classe = classe
        self.notes = notes
        self.moyenne = self.calculer_moyenne()

    def calculer_moyenne(self):
        return round(sum(self.notes) / len(self.notes), 2) if self.notes else 0

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "telephone": self.telephone,
            "classe": self.classe,
            "notes": self.notes,
            "moyenne": self.moyenne
        }
