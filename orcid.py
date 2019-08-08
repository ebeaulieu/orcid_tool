####################################################################################################
#
# Avec une liste d'identifiants ORCID, ce petit programme extrait de l'API de
# ORCID tous les travaux inscrits pour chaque chercheur et exporte un fichier
# csv comprenant une liste de publications incluant prenom, nom, putcode,
# type, revue, issn, titre, annee et auteurs
#
####################################################################################################

import requests
import json
import os, csv

os.chdir('C:\\Users\Eric\Documents\Suivi des publications\ORCID\Outil\orcid_tool')

with open('list_members.csv','r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    members = []
    next(reader, None)
    for row in reader:
        members.append({'last_name':row[0],'first_name':row[1], 'status':row[2], 'email':row[3], 'orcid':row[4]})

chercheurs = []
for member in members:
    if member['status'] == 'Régulier' and member['orcid'] != '':
    #if member['last_name'] == 'Talbot':
        chercheurs.append(member['orcid'])

#print(regular_members)

f1 = open('export.csv', 'w', newline='', encoding='utf-8')
with f1:
    writer = csv.writer(f1)
    writer.writerow(['prenom','nom','doi','putcode','type','revue','issn','editeur','titre','annee'])

for chercheur in chercheurs:
    resp = requests.get("http://pub.orcid.org/"+chercheur, headers={'Accept':'application/orcid+json'})
    prenom = resp.json()["person"]["name"]["given-names"]["value"]
    nom = resp.json()["person"]["name"]["family-name"]["value"]
    #print('\n'+prenom+' '+nom+'\n')

    putcodes = []

    #resp = requests.get("http://pub.orcid.org/"+jflapierre, headers={'Accept':'application/orcid+json'})
    #print(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    #print(resp.json()["activities-summary"]["works"]["group"])
    for group in resp.json()["activities-summary"]["works"]["group"]:
        for work_summary in group["work-summary"]:
            putcodes.append(work_summary["put-code"])
            #print(work_summary["put-code"])

    for putcode in putcodes:
        auteurs=[]
        resp = requests.get("http://pub.orcid.org/"+chercheur+"/work/"+str(putcode), headers={'Accept':'application/orcid+json'})

        doi=''
        issn=''
        revue=''
        editeur=''
        authors=[]
        try:
            for external_id in resp.json()["external-ids"]["external-id"]:
                if "external-id-type" in external_id:
                        if external_id["external-id-type"] == "doi":
                            doi = external_id["external-id-value"]
                            respcrossref = requests.get("https://api.crossref.org/works/"+doi)
                            issn = respcrossref.json()["message"]["ISSN"][0]
                            editeur = respcrossref.json()["message"]["publisher"]
                            for rang, author in enumerate(respcrossref.json()["message"]["author"]):
                                authors.append({"rang":rang+1,"given":author["given"]})
                                authors[len(authors)-1]["family"] = author["family"]
                                if "ORCID" in author:
                                    authors[len(authors)-1]["orcid"] = author["ORCID"]
                                #print(authors[len(authors)-1])
                            respcrossref = requests.get("https://api.crossref.org/journals/"+issn)
                            revue = respcrossref.json()["message"]["title"]

        except:
            doi=''

        #print(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))
        type = resp.json()["type"]

##        try:
##            if "journal-title" in resp.json():
##                revue = resp.json()["journal-title"]["value"]
##            else:
##                revue = ''
##        except:
##            revue = ''

##        issn=''
##        try:
##            for external_id in resp.json()["external-ids"]["external-id"]:
##                if "external-id-type" in external_id:
##                        if external_id["external-id-type"] == "issn":
##                            issn = external_id["external-id-value"]
##        except:
##            issn=''

        try:
            if "title" in resp.json():
                titre = resp.json()["title"]["title"]["value"]
            else:
                titre = ''
        except:
            titre = ''

        #print(resp.json()["contributors"]["contributor"][0]["credit-name"]["value"])

        try:
            if "publication-date" in resp.json():
                annee = resp.json()["publication-date"]["year"]["value"]
            else:
                annee = ''
        except:
            annee = ''

        try:
            for rang, contributor in enumerate(resp.json()["contributors"]["contributor"]):
                #print(str(rang)+" : "+contributor["credit-name"]["value"])
                auteurs.append(contributor["credit-name"]["value"])
            #print(auteurs)
        except:
            auteurs=[]

        #print(prenom+' '+nom+'*'+doi+'*'+str(putcode)+'*'+type+'*'+revue+'*'+issn+'*'+titre+'*'+str(annee)+'*['+'*'.join(auteurs)+']')
        print(nom+', '+prenom+' ('+str(annee)+') '+titre)

        #nms = [prenom,nom,doi,str(putcode),type,revue,issn,titre,str(annee),'*'.join(auteurs)]
        nms = [prenom,nom,doi,str(putcode),type,revue,issn,editeur,titre,str(annee)]
        #nms = [prenom,nom,doi]

        #os.chdir('C:\\Users\Eric\Documents\siteweb')
        f2 = open('export.csv', 'a', newline='', encoding='utf-8')

        with f2:

            writer = csv.writer(f2)

            #for row in nms:
            writer.writerow(nms)
