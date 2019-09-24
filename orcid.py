####################################################################################################
#
# Avec une liste d'identifiants ORCID, ce petit programme extrait de l'API de
# ORCID tous les travaux inscrits pour chaque chercheur et exporte un fichier
# csv comprenant une liste de publications incluant prenom, nom, putcode,
# type, revue, issn, titre, annee et auteurs
#
####################################################################################################

import requests
from xml.etree import ElementTree as ET
import json
import os, csv

os.chdir('C:\\Users\Eric\Documents\Suivi des publications\ORCID\Outil\orcid_tool')
fichier_sortie = "export2.csv"

with open('list_members.csv','r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    members = []
    next(reader, None)
    for row in reader:
        members.append({'last_name':row[0],'first_name':row[1], 'status':row[2], 'email':row[3], 'orcid':row[4]})

chercheurs = []
for member in members:
    #if member['status'] == 'Régulier' and member['orcid'] != '':
    if member['last_name'] == 'Talbot':
        chercheurs.append(member['orcid'])

#print(regular_members)

f1 = open(fichier_sortie, 'w', newline='', encoding='utf-8')
with f1:
    writer = csv.writer(f1)
    writer.writerow(['prenom','nom','doi','putcode','type','revue','issn','editeur','titre','annee','romeo_colour','url_for_pdf'])

for chercheur in chercheurs:
    resp_orcid = requests.get("http://pub.orcid.org/"+chercheur, headers={'Accept':'application/orcid+json'})
    prenom = resp_orcid.json()["person"]["name"]["given-names"]["value"]
    nom = resp_orcid.json()["person"]["name"]["family-name"]["value"]
    #print('\n'+prenom+' '+nom+'\n')

    putcodes = []

    #resp_orcid = requests.get("http://pub.orcid.org/"+jflapierre, headers={'Accept':'application/orcid+json'})
    #print(json.dumps(resp_orcid.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    #print(resp_orcid.json()["activities-summary"]["works"]["group"])
    for group in resp_orcid.json()["activities-summary"]["works"]["group"]:
        for work_summary in group["work-summary"]:
            putcodes.append(work_summary["put-code"])
            #print(work_summary["put-code"])

    for putcode in putcodes:
        auteurs=[]
        resp_orcid = requests.get("http://pub.orcid.org/"+chercheur+"/work/"+str(putcode), headers={'Accept':'application/orcid+json'})

        doi=''
        url_for_pdf=''
        issn=''
        revue=''
        editeur=''
        authors=[]
        romeo_colour=''
        try:
            for external_id in resp_orcid.json()["external-ids"]["external-id"]:
                if "external-id-type" in external_id:
                        if external_id["external-id-type"] == "doi":
                            doi = external_id["external-id-value"]

                            #ajout unpaywall
                            email = 'eric.g.beaulieu@umontreal.ca'
                            resp_unpaywall = requests.get('https://api.unpaywall.org/v2/'+doi+'?email='+email)
                            value = resp_unpaywall.json()["best_oa_location"]["url_for_pdf"]
                            if value:
                                url_for_pdf = value
                                #print(url_for_pdf)
                            else:
                                url_for_pdf = ''

                            resp_crossref = requests.get("https://api.crossref.org/works/"+doi)
                            issn = resp_crossref.json()["message"]["ISSN"][0]
                            editeur = resp_crossref.json()["message"]["publisher"]
                            for rang, author in enumerate(resp_crossref.json()["message"]["author"]):
                                authors.append({"rang":rang+1,"given":author["given"]})
                                authors[len(authors)-1]["family"] = author["family"]
                                if "ORCID" in author:
                                    authors[len(authors)-1]["orcid"] = author["ORCID"]
                                #print(authors[len(authors)-1])
                            resp_crossref = requests.get("https://api.crossref.org/journals/"+issn)
                            revue = resp_crossref.json()["message"]["title"]

                            #ajout SHERPA/RoMEO
                            romeo_key = "tEKXGkhWygY"
                            resp_romeo = requests.get("http://www.sherpa.ac.uk/romeo/api29.php?issn="+issn+"&ak="+romeo_key)
                            value = ET.fromstring(resp_romeo.text.strip()).find('publishers/publisher/romeocolour')
                            if value:
                                romeo_colour = value.text
                                print(romeo_colour)
                            else:
                                romeo_colour = ''

        except:
            doi=''

        #print(json.dumps(resp_orcid.json(), sort_keys=True, indent=4, separators=(',', ': ')))
        type = resp_orcid.json()["type"]

##        try:
##            if "journal-title" in resp_orcid.json():
##                revue = resp_orcid.json()["journal-title"]["value"]
##            else:
##                revue = ''
##        except:
##            revue = ''

##        issn=''
##        try:
##            for external_id in resp_orcid.json()["external-ids"]["external-id"]:
##                if "external-id-type" in external_id:
##                        if external_id["external-id-type"] == "issn":
##                            issn = external_id["external-id-value"]
##        except:
##            issn=''

        try:
            if "title" in resp_orcid.json():
                titre = resp_orcid.json()["title"]["title"]["value"]
            else:
                titre = ''
        except:
            titre = ''

        #print(resp_orcid.json()["contributors"]["contributor"][0]["credit-name"]["value"])

        try:
            if "publication-date" in resp_orcid.json():
                annee = resp_orcid.json()["publication-date"]["year"]["value"]
            else:
                annee = ''
        except:
            annee = ''

        try:
            for rang, contributor in enumerate(resp_orcid.json()["contributors"]["contributor"]):
                #print(str(rang)+" : "+contributor["credit-name"]["value"])
                auteurs.append(contributor["credit-name"]["value"])
            #print(auteurs)
        except:
            auteurs=[]

        #print(prenom+' '+nom+'*'+doi+'*'+str(putcode)+'*'+type+'*'+revue+'*'+issn+'*'+titre+'*'+str(annee)+'*['+'*'.join(auteurs)+']')
        print(nom+', '+prenom+' ('+str(annee)+') '+titre)

        #nms = [prenom,nom,doi,str(putcode),type,revue,issn,titre,str(annee),'*'.join(auteurs)]
        nms = [prenom,nom,doi,str(putcode),type,revue,issn,editeur,titre,str(annee),romeo_colour,url_for_pdf]
        #nms = [prenom,nom,doi]

        #os.chdir('C:\\Users\Eric\Documents\siteweb')
        f2 = open(fichier_sortie, 'a', newline='', encoding='utf-8')

        with f2:

            writer = csv.writer(f2)

            #for row in nms:
            writer.writerow(nms)
