from scrapping.scrapping_tools import *
from  Database.convertXML import *

rapports = []

for i in range(158):
    rapports += get_links_page(i)
    print(i)

print(len(rapports))

for r in tqdm(rapports):
    xmlToSQL(r)