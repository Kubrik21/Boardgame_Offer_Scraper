import requests
from selectorlib import Extractor

URL="https://shopgracz.pl/19-gry-planszowe?page="


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(URL):
    response = requests.get(URL,headers=HEADERS)
    source = response.text
    return source

#Extract data from source and modify
def extract(source):
    extractor = Extractor.from_yaml_file("../extract.yaml")
    value = extractor.extract(source)["Shopgracz"]

    return value

#Extract data for every single page with boardgames
def scrap():
    url = f"{URL}1"
    i = 1
    list=[]

    while requests.get(url, headers=HEADERS).status_code == 200:

        raw=extract(scrape(url))

        if (raw==None):
            break
        for elem in raw:
            elem["Name"] = str(elem["Name"]).lower()
        list+=raw
        print("Przerobiono wierszy: ",i)
        i += 1
        url = f"{URL}{i}"

    return list

if __name__ == '__main__':
    print(scrap())
