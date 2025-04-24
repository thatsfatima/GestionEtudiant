from services.gestion_etudiants import GestionEtudiants
from services.gestion_utilisateur import Utilisateur
from services import db, redis_cache

utilisateur_service = Utilisateur(db.MongoService(), redis_cache.RedisCache())
session_token = None

def main():
    gestion = GestionEtudiants()

    while True:
        print("\n=== MENU Principal ===")
        print("1. Créer un utilisateur")
        print("2. Se connecter")
        print("3. Continuer en tant qu’utilisateur connecté")
        print("0. Quitter")

        choix = input("Choix : ")

        if choix == "1":
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            telephone = input("Téléphone : ")
            mot_de_passe = input("Mot de passe : ")
            role = input("Rôle (admin / enseignant / etudiant) : ").lower()
            utilisateur_service.creer_utilisateur(nom, prenom, telephone, mot_de_passe, role)

        elif choix == "2":
            tel = input("Téléphone : ")
            mdp = input("Mot de passe : ")
            session_token = utilisateur_service.connecter(tel, mdp)

        elif choix == "3":
            if not session_token:
                print("⚠️ Vous devez d'abord vous connecter.")
                continue

            session = utilisateur_service.get_session(session_token)
            if not session:
                print("Session expirée.")
                session_token = None
                continue

            role = session["role"]
            nom_complet = session["prenom"] + " " + session["nom"]
            print(f"\n🎉 Connecté en tant que {nom_complet} ({role})")

            if role == "admin":
                while True:
                    print("\n--- MENU ADMIN ---")
                    print("1. Ajouter un étudiant")
                    print("2. Modifier les notes")
                    print("3. Supprimer un étudiant")
                    print("4. Afficher tous les étudiants")
                    print("5. Rechercher un étudiant")
                    print("6. Trier les étudiants")
                    print("7. Exporter les données")
                    print("8. Importer les données")
                    print("9. Déconnexion")
                    choix_admin = input("Choix : ")

                    if choix_admin == "1":
                        nom = input("Nom : ")
                        prenom = input("Prénom : ")
                        telephone = input("Téléphone : ")
                        classe = input("classe : ")
                        gestion.ajouter_etudiant(nom, prenom, telephone, classe)
                    elif choix_admin == "2":
                        matiere = input("Matiere : ")
                        valeur = input("Valeur:" )
                        gestion.modifier_notes(matiere, valeur)
                    elif choix_admin == "3":
                        gestion.supprimer_etudiant()
                    elif choix_admin == "4":
                        gestion.lister_etudiants()
                    elif choix_admin == "5":
                        gestion.rechercher_etudiant()
                    elif choix_admin == "6":
                        gestion.trier_etudiants_par_moyenne()
                    elif choix_admin == "7":
                        fmt = input("Format (csv, json, excel, pdf) : ").lower()
                        gestion.exporter_donnees(fmt)
                    elif choix_admin == "8":
                        fichier = input("Nom du fichier à importer (.csv ou .xlsx) : ")
                        gestion.importer_donnees(fichier)
                    elif choix_admin == "9":
                        session_token = None
                        break
                    else:
                        print("❌ Choix invalide.")

            elif role == "enseignant":
                while True:
                    print("\n--- MENU ENSEIGNANT ---")
                    print("1. Modifier les notes")
                    print("2. Rechercher un étudiant")
                    print("3. Déconnexion")
                    choix_ens = input("Choix : ")
                    if choix_ens == "1":
                        gestion.modifier_notes()
                    elif choix_ens == "2":
                        gestion.rechercher_etudiant()
                    elif choix_ens == "3":
                        session_token = None
                        break
                    else:
                        print("❌ Choix invalide.")

            elif role == "etudiant":
                telephone = session["telephone"]
                print("\n--- VOS NOTES ---")
                etudiant = db.etudiants.find_one({"telephone": telephone})
                if etudiant:
                    print(f"{etudiant['nom']} {etudiant['prenom']} ({etudiant['classe']})")
                    print("Notes : ", etudiant['notes'])
                    moyenne = sum(etudiant["notes"]) / len(etudiant["notes"])
                    print(f"Moyenne : {moyenne:.2f}")
                else:
                    print("❌ Étudiant non trouvé.")
            else:
                print("❌ Rôle inconnu.")

        elif choix == "0":
            print("À bientôt ! 👋")
            break

        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    main()
