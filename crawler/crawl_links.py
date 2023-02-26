import requests
from bs4 import BeautifulSoup as bs
import sys

counter = 0
limit = 500


def get_apps_link(link):
    global counter
    global limit
    r = requests.get(link, headers={"Accept": "application/xml"})
    results = bs(r.content, 'lxml-xml')
    results = results.find_all('url')

    lst = []

    if counter > limit:
        print('max limit reached', file=sys.stderr)
        exit(0)

    for j in results:
        counter += 1
        app_link = j.find('loc').text
        last_mod = j.find('lastmod').text
        last_mod = last_mod.split(
            'T')[0] + ' ' + last_mod.split('T')[1].split('+')[0]  # date + ' ' + time
        # 'app link, date, time' seprated by space
        lst.append(app_link + ' ' + last_mod)

    return lst


farsroid_sitemap_url = "https://www.farsroid.com/sitemap.xml"

r = requests.get(farsroid_sitemap_url, headers={"Accept": "application/xml"})


results = bs(r.content, 'lxml-xml')
results = results.find_all('sitemap')


for i in results:
    link = i.find('loc').text

    if "sitemap-pt" in link:
        apps_link = get_apps_link(link)
        print(*apps_link, sep='\n')
