import requests
from bs4 import BeautifulSoup

API = 'https://confiraloterias.com.br/'


def get_result(lottery, concourse=""):
    page = requests.get("{}{}".format(API, lottery), params={'concurso': concourse})
    soup = BeautifulSoup(page.text, 'html.parser')
    result = [soup.find("h5", {'class': 'card-title'}).text]
    for a in soup.findAll("div", {'class': 'kit-{}'.format(lottery)}):
        result.append(a.text)
    return result
