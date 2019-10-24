Cet outil permet de produire une liste des publications des membres d'un groupe de recherche.

- Fournir en entrée le fichier list_members.csv avec nom de famille (last_name), prénom (first_name), statut (status), adresse courriel (email) et numéro d'identifiant ORCID (ORCID). Le fichier list_members.csv est une copie de l'onglet ORCID_export du document de suivi des membres :
https://www.dropbox.com/scl/fi/verl2khb2sd3e0lbl928o/Suivi_ORCID_GRIL.xlsx?cloud_editor=excel&dl=0&web_open_id=web_open_id-51e5bb79a8c360a7

Niveau Chercheur
	- Extrait une liste d'identifiants de travaux (putcode) de l'API d'ORCID en fournissant l'identifiant ORCID du chercheur
	Référence : https://pub.orcid.org
	https://members.orcid.org/api/tutorial/reading-xml

Niveau Travail (API d'ORCID, CrossRef)
	- Extrait les informations suivantes de l'API d'ORCID en fournissant l'identifiant ORCID du chercheur et l'identifiant du travail (putcode) : 
		- l'identifiant DOI du travail (doi)
		- le type de document (type)
		- l'identidiant de revue (issn)
		- le volume, le numéro et l'intervalle de pages sont extraits de la citation bibtex (volume, number, pages)
		- le titre du travail (title)
		- l'année de publication (publication_year)
		- la liste des auteurs (authors)
	Référence : https://pub.orcid.org

	- Extrait l'URL du PDF si disponible (url_for_pdf) de l'API public d'ORCID en fournissant le doi obtenu avec l'API d'ORCID
	Référence : http://unpaywall.org/data-format
	
	- Extrait le nombre de citations (times_cited) de l'API de Dimensions Metrics en fournissant le doi obtenu avec l'API d'ORCID
	Exemple : https://metrics-api.dimensions.ai/doi/10.1071/EN11140

Niveau Revue
	- Extrait le nom de la revue de l'API CrossRef avec l'identifiant de revue (issn) obtenu avec l'API d'ORCID : 
	- le nom de la revue (journal)
	- le nom de l'éditeur (publisher)

Niveau Éditeur

- Extrait le nom de l'éditeur de l'API CrossRef avec l'identifiant de revue (issn) obtenu avec l'API d'ORCID
- Extrait la couleur RoMEO (romeo_colour) de l'éditeur de l'API SHERPA/RoMEO avec l'identifiant de revue (issn) obtenu avec l'API d'ORCID
Exemple : http://www.sherpa.ac.uk/romeo/api29.php?issn=0956-7135&ak=tEKXGkhWygY

Pour en savoir plus sur les couleurs RoMEO
http://www.sherpa.ac.uk/romeoinfo.html : 
Pour en savoir plus sur l'utilisation de l'API : 
http://sherpa.ac.uk/romeo/apimanual.php?la=en&fIDnum=|&mode=simple#howto

- Produit en sortie un fichier csv avec first_name, last_name, doi, putcode, type, journal, issn, publisher, title, publication_year, romeo_colour, url_for_pdf, times_cited et authors

Développement prévu :

- Optimiser pour que l'exécution se fasse beaucoup plus rapidement
- Ne Permettre d'ajouter que les nouvelles publications par rapport à ce qui est déjà présent dans le fichier export.csv
- Algorithme de name matching pour parvenir à identifier les coauteurs membres du GRIL
- Documenter
- Intégration directe dans une base de données Access
- Séparer le code interrogeant avec le doi pour ne faire des requêtes qu'avec une liste de doi uniques
