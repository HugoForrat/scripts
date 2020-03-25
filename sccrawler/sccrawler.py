#!/usr/bin/env python3
import sys
import requests
import re
import os
from bs4 import BeautifulSoup

def err_and_quit(valeur):
    sys.stderr.write("Erreur : la valeur "+valeur+" n'est pas reconnue.\n"+usage)
    sys.exit()

def parse_arglist(args):
    if len(sys.argv) < 2:
        sys.stderr.write("Erreur.\n"+usage)
        sys.exit()
    elif (len(sys.argv) - 2) % 2 != 0:
        sys.stderr.write("Erreur, veuillez donner une unique valeur par option.\n"+usage)
        sys.exit()
    else:
        ta_dict = { "envies":"wish", "coup_de_coeur":"recommend", "en_cours":"current", "notés":"rating", "achevés":"done"}
        tr_dict = { "date_sortie":"release_date", "note_global":"global_rating", "popularité":"popularite", "titre":"titre"}
        args['pseudo'] = sys.argv[1]

        for i in range(2, len(sys.argv), 2):
            option = sys.argv[i]
            valeur = sys.argv[i+1]
            if option in ["-u", "--univers"]:
                if valeur in ["films", "series", "jeuxvideo", "livres", "bd", "albums", "morceaux"]:
                    args["univers"] = valeur
                else:
                    err_and_quit(valeur)
            elif option in ["-o", "--output"]:
                args["output"] = valeur
            elif option in ["-ta", "--type_action"]:
                if valeur in ta_dict:
                    args["type_action"] = ta_dict[valeur]
                else:
                    err_and_quit(valeur)
            elif option in ["-tr", "--trier_par"]:
                if valeur in tr_dict:
                    # args["trier_par"] = valeur # Bug non ? A tester
                    args["trier_par"] = tr_dict[valeur]
                else:
                    err_and_quit(valeur)
            elif option in ["-s", "--sortie"]:
                args["date_sortie"] = valeur
            else:
                sys.stderr.write("Erreur : l'option "+option+" n'est pas reconnue.\n"+usage)
                sys.exit()

def check_output_file(args):
    if args["output"] == "":
        args["output"] = "donnees_senscritique"
        for key in args:
            if key != "output" and args[key] != "all":
                args["output"] += ("_"+args[key])
        args["output"] += ".csv"
        print("Nom de fichier de sortie automatique : "+args["output"])
    if os.path.exists(args['output']):
        print("Le fichier {} existe déjà. Voulez vous l'écraser ? (O)ui/(N)on".format(args['output']))
        reponse = input()
        if reponse == 'Non' or reponse == 'N' or reponse == 'non' or reponse == 'n':
            print("Veuillez préciser un nouveau nom de fichier avec l'option -o")
            sys.exit()
        elif reponse == 'Oui' or reponse == 'O' or reponse == 'oui' or reponse == 'o':
            pass
        else:
            sys.stderr.write("Erreur : réponse non reconnue.\n Écrivez 'oui' ou 'non'")
            sys.exit()
    return open(args['output'], 'w')

usage = """Usage : sccrawler <pseudo> <options>

Options :
-o, --output          Donne le nom du fichier de sortie
-u, --univers         Récupère uniquement un univers.
                      Valeurs possibles : films, series, jeuxvideo, livres, bd, albums, morceaux
-ta, --type_action    Récupère uniquement les oeuvres pour un certain type d'action
                      Valeurs possibles : envies, coup_de_coeur, en_cours, notés, achevés
-tr, --trier_par      Indique une façon de trier les résultats.
                      Si cette option n'est pas précisée, on trie d'après la dernière action de l'utilisateur 
                      dont on a donné le pseudo
                      Valeurs possibles : date_sortie, note_globale, popularité, titre
-s, --sortie          Récupère uniquement les oeuvres sorties pendant une certaine année
                      Attention : pour --sortie, si vous indiquez une année se terminant par un 0, on récupèrera les 
                      oeuvres pour toute la décennie


Exemple :
    sccrawler Pseudo --univers films -ta envies --sortie 2018
"""

# Constructing the URL
arglist = {
        "pseudo": "", #OK
        "type_action": "all", #OK
        "trier_par": "all",
        "genre": "all", #NON
        "univers": "all", #OK
        "categorie": "all", #NON
        "date_sortie": "all", #OK
        "date_lecture": "all", #OK
        "output": ""
}

parse_arglist(arglist)

url_skeleton = "https://www.senscritique.com/{}/collection/{}/{}/{}/{}/all/{}/{}/{}/list/page-".format(
        arglist['pseudo'],
        arglist['type_action'],
        arglist['univers'],
        arglist['trier_par'],
        arglist['genre'],
        arglist['categorie'],
        arglist['date_sortie'],
        arglist['date_lecture'],
        )

url = url_skeleton+"1"

# GETting the first page and finding out how many page should we treat
r = requests.get(url, allow_redirects=False)
if r.status_code != 200:
    sys.stderr.write("Erreur : impossible d'accéder à la page SensCritique demandée.\n")
    if r.status_code == 301:
        sys.stderr.write("Avez vous saisi un identifiant correct ?")
    sys.exit()

out = check_output_file(arglist)

max_page = 1
regex_pager = re.compile(r"data-sc-pager-page\=\"(\d*)\"")
soup = BeautifulSoup(r.text, 'html.parser')
for line in soup.find_all(attrs={"class":"eipa-anchor"}):
    result = regex_pager.search(str(line))
    if result != None and int(result.group(1)) > max_page:
        max_page = int(result.group(1))
# print(max_page)

date = ""
titre = ""
artiste = []

re_title = re.compile(r"<a.*id=\"product-title-\d*\">(.*)</a>")
re_date = re.compile(r"<span class=\"elco-date\">\((.*)\)</span>")
re_artiste = re.compile(r"<(?:a|span) class=\"elco-baseline-a\".*>(.*)</(?:a|span)>")

# Main loop
for i_current_page in range(1, max_page+1, 1):
    url = url_skeleton+str(i_current_page)
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for line in soup.find_all(attrs={"class":"elco-product-detail"}):
        artiste.clear()
        s_line = str(line)
        res = re_title.search(s_line)
        titre = res.group(1).replace('&amp;', '&')
        if "," in titre:
            titre = '"{}"'.format(titre)
        res = re_date.search(s_line)
        if res != None:
            date = res.group(1)
        else:
            date = "NA"
        for i in re_artiste.finditer(s_line):
            artiste.append(i.group(1).replace('&amp;', '&'))

        # Writing the line
        new_line = titre+","
        if len(artiste) == 1:
            new_line += (artiste[0]+",")
        else:
            new_line += '"'
            for j in range(len(artiste)):
                new_line += artiste[j]
                if j != (len(artiste)-1):
                    new_line += ","
            new_line += '",'
        new_line += (date+"\n")
        out.write(new_line)

out.close()
