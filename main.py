import requests
from selectorlib import Extractor
from merger import merge_all

import scrapMapel
import scrapShopgracz


if __name__ == '__main__':

    L1=scrapMapel.scrap()
    L2=scrapShopgracz.scrap()
    All=merge_all(L1,L2)







