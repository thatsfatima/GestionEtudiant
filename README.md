# GestionEtudiant

# Système de Gestion des Étudiants

## **Description**
Ce projet est une application interne pour la gestion des étudiants d’un établissement scolaire. Il utilise **Python**, **MongoDB** pour le stockage des données, et **Redis** pour optimiser les performances grâce à la mise en cache.

---

## **Installation et Lancement**

### **Prérequis**
- **Python** (version 3.9 ou supérieure).
- **MongoDB** (service actif sur votre machine ou serveur).
- **Redis** (service actif).

### **Étapes d'installation**
1. Clonez ce dépôt sur votre machine :
   ```bash
   git clone https://github.com/thatsfatima/GestionEtudiant.git
   cd gestion-etudiants
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l’application :
   ```bash
   python gestion_etudiants/main.py
   ```

---

## **Fonctionnalités Principales**

### **1. Gestion des étudiants**
- **Ajouter un étudiant** : Ajout avec validation stricte (Téléphone unique, notes entre 0 et 20).
- **Afficher les étudiants** : Liste récupérée depuis Redis (si disponible) ou MongoDB.
- **Rechercher un étudiant** : Recherche par nom, prénom, téléphone ou classe.
- **Modifier les notes** : Mise à jour des notes avec synchronisation entre MongoDB et Redis.
- **Supprimer un étudiant** : Suppression complète avec mise à jour des bases.
- **Exporter les données** : Export en formats CSV, JSON, Excel ou PDF.
- **Importer les données** : Import depuis un fichier CSV ou Excel.

### **2. Gestion des utilisateurs**
- Authentification avec rôles :
  - **Admin** : Gestion complète des étudiants et utilisateurs.
  - **Enseignant** : Ajout et modification des notes.
  - **Étudiant** : Consultation des notes uniquement.
- Stockage sécurisé des mots de passe avec `bcrypt`.
- Gestion des sessions via Redis.

### **3. Statistiques et rapports**
- Calcul de la moyenne générale par classe.
- Génération de rapports PDF avec un résumé des résultats.

---

## **Utilisation**

### **Menu Interactif**
Une fois l'application lancée, naviguez à travers le menu interactif en ligne de commande. Voici les options principales :
1. Ajouter un étudiant.
2. Afficher la liste des étudiants.
3. Rechercher un étudiant.
4. Modifier les informations d’un étudiant.
5. Supprimer un étudiant.
6. Exporter les données.
7. Importer des données.
8. Générer un rapport.
9. Gérer les utilisateurs.

Sélectionnez une option en entrant son numéro correspondant.

---

## **Licence**
Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).
```

Ce fichier peut être enregistré directement sous le nom `README.md`. Il contient une structure claire avec les instructions pour l’installation, les fonctionnalités principales, et l’utilisation.
```
