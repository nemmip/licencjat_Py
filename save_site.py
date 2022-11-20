from bs4 import BeautifulSoup
from stable_model import Adress, Stable
import csv


def saveSite():
    # try:
    f = open('./revolta.html', 'r')
    soup = BeautifulSoup(f, features="html.parser")
    stables_html = soup.body.find_all("div", "ogloszenie stajnie")
    stables = [extractStableIntoClass(el) for el in stables_html]

    saveStablesCsv(*stables)
    # except:
    #     print("Not found, trying to scrap...")


def extractStableIntoClass(stable):
    adress = extractAdress(stable)
    infrastructure = extractInfrastructure(stable)

    return Stable(adress, infrastructure)


def extractAdress(stable):
    adress_html = stable.find("div", "adres")
    adress_content = str.join(
        '', [el.string for el in adress_html.contents]).strip(). split(', ')

    if len(adress_content) == 2:
        return Adress(adress_content[0], None, adress_content[1])
    return Adress(adress_content[0],  adress_content[1],  adress_content[2])


def extractInfrastructure(stable):
    infrastructure_html = stable.ul.find_all("li")
    infrastructure_content = [el.contents[2].strip()
                              for el in infrastructure_html]
    infrastructure_content.sort()
    return infrastructure_content


def saveStablesCsv(*stables):
    i = 0
    with open('stables.csv', "w") as file:
        writer = csv.writer(file)
        with open('infra.csv', "w") as infra_file:
            infra_writer = csv.writer(infra_file)
            writer.writerow(['ID', 'city', 'district', 'state'])
            infra_writer.writerow(['Stable_ID', 'Category'])
            for stable in stables:
                writer.writerow([i, stable.adress.city,
                                stable.adress.district, stable.adress.state])
                for infr in stable.infrastructure:
                    infra_writer.writerow([i, infr])
                i += 1
