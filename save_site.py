from bs4 import BeautifulSoup
from stable_model import Adress, Stable
import csv
import requests as req
from os import path, remove

__STABLES_PATH = './stables.csv'
__INFRA_PATH = './infra.csv'


def scrapStables(numOfStables):
    responses: list = []
    for i in range(1, numOfStables+1):
        response = req.get(
            f"https://ogloszenia.re-volta.pl/stajnie/?boksy=2&strona={i}")
        responses.append(response.text)
        print(response.status_code)
    saveSites(responses)


def saveSites(htmls: list):
    stables: list = []
    for html in htmls:
        soup = BeautifulSoup(html, features="html.parser")
        stables_html = soup.body.find_all("div", "ogloszenie stajnie")
        stables.extend([extractStableIntoClass(el) for el in stables_html])

    saveStablesCsv(*stables)


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
    with open(__STABLES_PATH, "a") as file:
        writer = csv.writer(file)
        with open(__INFRA_PATH, "a") as infra_file:
            infra_writer = csv.writer(infra_file)
            writer.writerow(['ID', 'city', 'district', 'state'])
            infra_writer.writerow(['Stable_ID', 'Category'])
            for stable in stables:
                writer.writerow([i, stable.adress.city,
                                stable.adress.district, stable.adress.state])
                for infr in stable.infrastructure:
                    infra_writer.writerow([i, infr])
                i += 1


def deleteOldFiles():
    infraExist: bool = path.exists(__INFRA_PATH)
    stablesExist: bool = path.exists(__STABLES_PATH)

    if infraExist:
        remove('./infra.csv')
        print(f"Deleted {__INFRA_PATH}")
    if stablesExist:
        remove('./stables.csv')
        print(f"Deleted {__STABLES_PATH}")
