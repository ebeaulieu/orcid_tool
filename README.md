Cet outil permet de produire une liste des publications des membres d'un groupe de recherche.

- Fournir en entrée le fichier list_members.csv avec nom de famille (last_name), prénom (first_name), statut (status), adresse courriel, (email) et numéro d'identifiant ORCID (ORCID). Le fichier list_members.csv est une copie de l'onglet ORCID_export du document de suivi des membres :
https://www.dropbox.com/scl/fi/verl2khb2sd3e0lbl928o/Suivi_ORCID_GRIL.xlsx?cloud_editor=excel&dl=0&web_open_id=web_open_id-51e5bb79a8c360a7

- Produit en sortie le fichier export.csv avec prenom, nom, doi, putcode, type, revue, issn, editeur, titre annee, romeo_colour et	url_for_pdf

Développement prévu :

- Optimiser pour que l'exécution se fasse beaucoup plus rapidement
- Ne Permettre d'ajouter que les nouvelles publications par rapport à ce qui est déjà présent dans le fichier export.csv
- Algorithme de name matching pour parvenir à identifier les coauteurs membres du GRIL
- Documenter
