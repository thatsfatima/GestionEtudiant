from models.classe import Classe

class Note:
    def __init__(self, libelle, valeur=0):
        self.libelle = libelle,
        self.valeur = valeur

    def to_dict(self):
        return {
            'libelle': self.libelle,
            'valeur': self.valeur
        }
    
