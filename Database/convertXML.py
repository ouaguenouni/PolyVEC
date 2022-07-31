from Experiments import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import psycopg2

conn = psycopg2.connect(
    host="195.154.45.91",
    database="politicometre",
    user="politicometre",
    password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
    sslmode ='disable')
c = conn.cursor()

def extract_xml_simple(xml_l):
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
    datas = {}
    for p in tqdm(p_links):
        #print("p = " , p.attrs["code_grammaire"])
        if( len(p.find_all("orateur")) > 0 and p.attrs["code_grammaire"] == "PAROLE_GENERIQUE" and p.attrs["code_parole"] == "PAROLE_1_2"):
            if p.find_all("nom")[0].text.replace("M. ","").replace("Mme ","") not in datas:
                datas[p.find_all("nom")[0].text.replace("M. ","").replace("Mme ","")] = []
            datas[p.find_all("nom")[0].text.replace("M. ","").replace("Mme ","")].append(p.find_all("texte")[0].text)

    return datas

def deputesId():
    deputes = dict()
    c.execute("SELECT id,nom FROM deputes")
    myresult = c.fetchall()
    for x in myresult:
        deputes[x[1]]=x[0]

    return  deputes

def xmlToSQL(url):

    data = extract_xml_simple("https://www.assemblee-nationale.fr/dyn/opendata/CRSANR5L15S2022O1N164.xml")
    deputes = deputesId()

    for d in data:
        if d in deputes:
            for t in data[d]:
                c.execute('''
                              INSERT INTO texts ( deputes_id, text) VALUES
                              (\'''' + str(deputes[d]) + '''\', \'''' + t.replace("'","''") + '''\');
                              ''')

    conn.commit()