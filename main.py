import requests
from selectorlib import Extractor


URL="https://mepel.pl/gry-planszowe"
URL2="https://shopgracz.pl/19-gry-planszowe"
#+ ?page=2

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    response=requests.get(url, headers=HEADERS)
    print(response)
    source = response.text
    #return source

def extract(source):
    extractor=Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["Mepel"]
    return value

if __name__ == '__main__':

    print(scrape(URL))
    #print(extract(scrape(URL)))
    #print(extract(scrape(URL2)))

    #print(extract(scrape(URL)))




