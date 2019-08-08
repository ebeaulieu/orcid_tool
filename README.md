# orcid_tool

Cet outil permet de produire une liste des publications des membres d'un groupe de recherche. 

- Fournir en entrée le fichier list_members.csv avec nom de famille (last_name), prénom (first_name), statut (status), adresse courriel, (email) et numéro d'identifiant ORCID (ORCID)
- Produit en sortie le fichier export.csv avec prenom, nom, doi, putcode, type, revue, issn, editeur, titre et annee

DÉVELOPPEMENT PRÉVU : 
- Optimiser pour que l'exécution se fasse beaucoup plus rapidement
- Permettre de n'ajouter que les nouvelles publications par rapport à ce qui est déjà présent dans le fichier export.csv
- Documenter
