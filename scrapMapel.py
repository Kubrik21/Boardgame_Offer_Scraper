import requests
from selectorlib import Extractor

URL="https://mepel.pl/gry-planszowe"


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(URL):
    response = requests.get(URL,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = Extractor.from_yaml_file("../extract.yaml")
    value = extractor.extract(source)["Mepel"]
    site = extractor.extract(source)["Selector"]
    for elem in value:
        elem["Img"]=f"https://mepel.pl{elem['Img']}"
        elem["Link"]=f"https://mepel.pl{elem['Link']}"
        elem["Price"]=elem['Price'][:elem['Price'].index(',')+3].replace(',', '.').replace(' ','')
        elem["Name"] = str(elem["Name"]).lower()

    return value,site


def scrap():
    url = f"{URL}/1"
    i = 1
    list=[]
    while requests.get(url, headers=HEADERS).status_code == 200:
        raw=extract(scrape(url))
        siteSelector=int(raw[1])

        if (siteSelector != i):
            break
        print("Przerobiono wierszy: ", i)
        list+=raw[0]
        i += 1
        url = f"{URL}/{i}"

    return list

if __name__ == '__main__':
    #print(scrap())
    print(extract(scrape(URL)))
