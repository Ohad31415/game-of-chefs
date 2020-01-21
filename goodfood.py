import time
from math import ceil
from random import gauss

import requests
import bs4


BASE = 'https://www.bbcgoodfood.com/search'
prefix = 'https://www.bbcgoodfood.com'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}


def search_results(query, pages=None, wait=5, jitter=True):
    if not wait:
        wait = 0

    res = requests.get(BASE, headers=headers, params={'query': query})

    if res.ok is False:
        # replace this using logger next commit:
        print('request denied for the first page!')
        return

    soup = bs4.BeautifulSoup(res.text, features='lxml')
    search_header = soup.select('#block-current-search-bbcgf > div > h1')[0]
    all_results, search_q = search_header.select('em')
    all_results, search_q = int(all_results.text), search_q.text

    urls = [a['href'] for a in soup.select('#search-results article > h3 > a')]

    results_per_page = len(urls)
    all_pages = ceil(all_results / results_per_page)

    limit = pages or all_pages

    for page in range(1, limit):
        # spaces up the requests:
        if callable(wait):
            wait()
        else:
            # if jitter=True (default) adds some normal gaussian noise to wait seconds:
            time.sleep(wait + (jitter and abs(gauss(mu=0, sigma=1))))

        res = requests.get(BASE, headers=headers, params={'query': query})

        if res.ok is False:
            # some logging can be done here
            break

        soup = bs4.BeautifulSoup(res.text, features='lxml')
        urls.extend([a['href'] for a in soup.select('#search-results article > h3 > a')])

    return [prefix + url for url in urls]


# print(search_results(query='mushroom soup', wait=2))
