import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import spacy
from sklearn.feature_extraction.text import CountVectorizer

root_an_site = "https://www.assemblee-nationale.fr"


def get_full(part):
    """
    Used to rebuild an absolute link of the website of the national assembly from a relative one.
    """
    return root_an_site + part

def get_cr_ls(page):
    """
    User to walk over the different pages that contains the report.
    """
    return f"https://www.assemblee-nationale.fr/dyn/15/comptes-rendus/seance?page={page}"

def get_xml(test_lk):
    """
    Fetches from the link of a report the XML version of it.
    """
    results = requests.get(test_lk)
    soup = BeautifulSoup(results.text, 'html.parser')
    links = soup.find_all('a', attrs = {"aria-label":"Accéder à la version XML de l'open data du document"})
    if(len(links) == 0):
        return None
    return (get_full(links[0]["href"]))


def get_person_dt(person_lk):
    """
    Fetches from the link of a parlementarian, it's name, circonscription and group.
    """
    results = requests.get(person_lk)
    soup = BeautifulSoup(results.text, 'html.parser')
    try:
        name = soup.find_all("h1")[0].text
    except(Exception):
        print("Cannot parse the link: ", person_lk)
        return {}
    group = soup.find_all("a", attrs = dict(title="Accédez à la composition du groupe"))[0].text
    circonscription  = soup.find_all("p", attrs = {"class":"deputy-healine-sub-title"})[0].text
    return {"name": name, "group": group, "circonscription": circonscription}




def get_links_page(page):
    """
    Fetches from a page of the national assembly's website all the links to the different reports.
    """
    link_L = []
    results = requests.get(get_cr_ls(page))
    soup = BeautifulSoup(results.text, 'html.parser')
    links = soup.find_all('h3', attrs = {"class":"crs-h-seance _colored"})
    for li in links:
        children = li.findChildren("a" , recursive=False)
        link_L.append(get_full(children[0].get("href")))
    return link_L


def extract_xml(xml_l, orateurs_datas = {}, not_found = []):
    """
    From the XML link to a report extract a list of dictionnaries containing :  (parlementarian, group, circonscription, texte).
    Args:
        - xml_l : XML Link
        - orateurs_datas: Previously saved data about the orators (used to avoid to refetch the group/circonscription of a parlementarian twice).
        - not_found: Contain the links that cannot be fetched (often because it's not parlementarian i.e the governement or an external intervention) and used
        to avoid trying to fetch them another time.
    """
    results = requests.get(xml_l)
    soup = BeautifulSoup(results.text, 'html.parser')
    p_links = soup.find_all("paragraphe")
    datas = []
    for p in tqdm(p_links):
        #print("p = " , p.attrs["code_grammaire"])
        if( len(p.find_all("orateur")) > 0 and len(p.find_all("acteurref")) > 0 and p.attrs["code_grammaire"] == "PAROLE_GENERIQUE"):
            orateur_link = "https://www2.assemblee-nationale.fr/deputes/fiche/OMC_" + p.find_all("orateur")[0].find_all("acteurref")[0].text
            if(not orateur_link in orateurs_datas):
                if(orateur_link in not_found):
                    continue
                or_data = get_person_dt(orateur_link)
                if(len(or_data.values()) == 0):
                    not_found.append(orateur_link)
                    name2 = p.find_all("orateur")[0].find_all("nom")[0]
                    print("paragraph p not parsed: ", name2)
                    continue
                orateurs_datas[orateur_link] = or_data
            else:
                or_data = orateurs_datas[orateur_link]
            data = or_data.copy()
            data["texte"] = (p.find_all("texte")[0].text)
            datas.append(data)
    return datas

