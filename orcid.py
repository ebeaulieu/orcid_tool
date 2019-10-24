####################################################################################################
#
# Avec une liste d'identifiants ORCID, ce petit programme extrait des APIs de
# ORCID, unpaywall, Dimensions Metrics et CrossRef tous les travaux inscrits
# pour chaque chercheur et exporte un fichier csv comprenant une liste de
# publications incluant prenom, nom, putcode, type, revue, issn, titre, annee et auteurs
#
####################################################################################################

import requests
from xml.etree import ElementTree as ET
import json
import os, csv
import bibtexparser

# Pour Git cd ~/Documents/SuiviPublications/ORCID/Outil/orcid_tool
os.chdir('C:\\Users\Eric\Documents\SuiviPublications\ORCID\Outil\orcid_tool')

import time, datetime
timestr = time.strftime("%Y%m%d-%H%M%S")
#print timestr

fichier_sortie = "PublicationsGRIL_"+timestr+".csv"

with open('list_members.csv','r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    members = []
    next(reader, None)
    for row in reader:
        members.append({'last_name':row[0],'first_name':row[1], 'status':row[2], 'email':row[3], 'orcid':row[4]})

chercheurs = []
for member in members:
    if member['status'] == 'Régulier' and member['orcid'] != '':
    #if member['last_name'] == 'Beisner':
        chercheurs.append(member['orcid'])

#print(regular_members)

f1 = open(fichier_sortie, 'w', newline='', encoding='utf-8')
with f1:
    writer = csv.writer(f1)
    writer.writerow(['first_name','last_name','doi','putcode','source','type','journal','volume','number','pages','issn','publisher','title','publication_year','romeo_colour','url_for_pdf','times_cited','authors'])

for chercheur in chercheurs:
    resp_orcid = requests.get("http://pub.orcid.org/"+chercheur, headers={'Accept':'application/orcid+json'})
    prenom = resp_orcid.json()["person"]["name"]["given-names"]["value"]
    nom = resp_orcid.json()["person"]["name"]["family-name"]["value"]
    #print('\n'+prenom+' '+nom+'\n')

    print('\n'+prenom+' '+nom +' ('+chercheur+')')
    start = time.time()

    putcodes = []

    #resp_orcid = requests.get("http://pub.orcid.org/"+jflapierre, headers={'Accept':'application/orcid+json'})
    #print(json.dumps(resp_orcid.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    #print(resp_orcid.json()["activities-summary"]["works"]["group"])
    for group in resp_orcid.json()["activities-summary"]["works"]["group"]:
        for work_summary in group["work-summary"]:
            putcodes.append(work_summary["put-code"])
            #print(work_summary["put-code"])
            if work_summary["source"]["source-name"]["value"]:
                source = work_summary["source"]["source-name"]["value"]
            else:
                source = 'unknown'

    for putcode in putcodes:
        auteurs=[]
        resp_orcid = requests.get("http://pub.orcid.org/"+chercheur+"/work/"+str(putcode), headers={'Accept':'application/orcid+json'})

        doi=''
        url_for_pdf=''
        times_cited=''
        issn=''
        revue=''
        editeur=''
        authors=[]
        romeo_colour=''

        try:
            if "external-ids" in resp_orcid.json():
                for external_id in resp_orcid.json()["external-ids"]["external-id"]:
                    if "external-id-type" in external_id:
                        if external_id["external-id-type"] == "doi":
                            doi = external_id["external-id-value"]

                            # API unpaywall
                            try:
                                email = 'eric.g.beaulieu@umontreal.ca'
                                url = 'https://api.unpaywall.org/v2/'+doi+'?email='+email
                                resp_unpaywall = requests.get(url)
                                if resp_unpaywall.ok is True:
                                    if resp_unpaywall.json()["best_oa_location"]:
                                        url_for_pdf = resp_unpaywall.json()["best_oa_location"]["url_for_pdf"]
                                        #print(url_for_pdf)
                            except:
                                #pass
                                print('Something went wrong with unpaywall API with request',url)
                                #url_for_pdf = ''

                            # API Dimensions Metrics
                            try:
                                url = 'https://metrics-api.dimensions.ai/doi/'+doi
                                resp_dimensions = requests.get(url)
                                if resp_dimensions.ok is True:
                                    value = resp_dimensions.json()["times_cited"]
                                    if value:
                                        times_cited = value
                                        #print(times_cited)
                            except:
                                #pass
                                print('Something went wrong with Dimensions Metrics API for request',url)
                                #times_cited = ''

                            # API CrossRef
                            try:
                                url = "https://api.crossref.org/works/"+doi
                                resp_crossref = requests.get(url)
                                if resp_crossref.ok is True:
                                    if "ISSN" in resp_crossref.json()["message"]:
                                        issn = resp_crossref.json()["message"]["ISSN"][0]
                                    if "publisher" in resp_crossref.json()["message"]:
                                        editeur = resp_crossref.json()["message"]["publisher"]
                                    for rang, author in enumerate(resp_crossref.json()["message"]["author"]):
                                        authors.append({"rang":rang+1,"given":author["given"]})
                                        authors[len(authors)-1]["family"] = author["family"]
                                        if "ORCID" in author:
                                            authors[len(authors)-1]["orcid"] = author["ORCID"]
                                        #print(authors[len(authors)-1])
                                    resp_crossref = requests.get("https://api.crossref.org/journals/"+issn)
                                    if "title" in resp_crossref.json()["message"]:
                                        revue = resp_crossref.json()["message"]["title"]
                            except:
                                #pass
                                print('Something went wrong with CrossRef API with request',url)
                                #revue=''

                            #ajout SHERPA/RoMEO
                            try:
                                romeo_key = "tEKXGkhWygY"
                                if issn != '':
                                    url = "http://www.sherpa.ac.uk/romeo/api29.php?issn="+issn+"&ak="+romeo_key
                                    resp_romeo = requests.get(url)
                                    if resp_romeo.ok:
                                        resp_romeo_ET = ET.fromstring(resp_romeo.text.strip())
                                        value = resp_romeo_ET.find('publishers/publisher/romeocolour')
                                        if value is not None and value.text:
                                            romeo_colour = value.text
                                            #print(romeo_colour)
                            except:
                                #pass
                                print('Something went wrong with SHERPA/RoMEO API with request',url)
                                #romeo_colour = ''
        except:
            #pass
            print('Something went wrong with DOI acquisition for putcode',putcode)
            #doi=''

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
            if resp_orcid.json()["citation"]["citation-type"] == "bibtex":
                bib_database = bibtexparser.loads(resp_orcid.json()["citation"]["citation-value"])
                volume = bib_database.entries[0]["volume"]
                number = bib_database.entries[0]["number"]
                pages = bib_database.entries[0]["pages"]
                #print(volume+'('+number+'):'+pages)
        except:
            volume,number,pages = '','',''

        try:
            for rang, contributor in enumerate(resp_orcid.json()["contributors"]["contributor"]):
                #print(str(rang)+" : "+contributor["credit-name"]["value"])
                auteurs.append(contributor["credit-name"]["value"])
            #print(auteurs)
        except:
            auteurs=[]

        #print(prenom+' '+nom+'*'+doi+'*'+str(putcode)+'*'+type+'*'+revue+'*'+issn+'*'+titre+'*'+str(annee)+'*['+'*'.join(auteurs)+']')
        #print(nom+', '+prenom+' ('+str(annee)+') '+titre)

        #nms = [prenom,nom,doi,str(putcode),type,revue,issn,titre,str(annee),'*'.join(auteurs)]
        nms = [prenom,nom,doi,str(putcode),source,type,revue,volume,number,pages,issn,editeur,titre,str(annee),romeo_colour,url_for_pdf,times_cited,'*'.join(auteurs)]
        #nms = [prenom,nom,doi]

        #os.chdir('C:\\Users\Eric\Documents\siteweb')
        f2 = open(fichier_sortie, 'a', newline='', encoding='utf-8')

        with f2:

            writer = csv.writer(f2)

            #for row in nms:
            writer.writerow(nms)

        #print('.', end='')
        #print(putcode, end=' ')

    end = time.time()
    a = datetime.timedelta(seconds=end-start)
    # Référence : https://stackoverflow.com/a/1384465
    print(str(a), end='')
    #print('', end - start, 'seconds', end='')
    # Référence : https://stackoverflow.com/a/7370824