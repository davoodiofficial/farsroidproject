import requests
from bs4 import BeautifulSoup as bs
import sys
import concurrent.futures


def get_apps_link(link):
    global counter
    global limit
    r = requests.get(link, headers={"Accept": "application/xml"})
    results = bs(r.content, 'lxml-xml')
    results = results.find_all('url')

    lst = []

    for i in results:
        app_link = i.find('loc').text
        last_mod = i.find('lastmod').text
        last_mod = last_mod.split(
            'T')[0] + ' ' + last_mod.split('T')[1].split('+')[0]  # date + ' ' + time
        # 'app link, date, time' seprated by space
        lst.append(app_link + ' ' + last_mod)

    print(*lst, sep='\n')


farsroid_sitemap_url = "https://www.farsroid.com/sitemap.xml"

r = requests.get(farsroid_sitemap_url, headers={"Accept": "application/xml"})

results = bs(r.content, 'lxml-xml')
results = results.find_all('loc')
app_links = list()

for i in results:
    link = i.text
    if "sitemap-pt" in link:
        app_links.append(link)
        # apps_link = get_apps_link(link)
        # print(*apps_link, sep='\n')

max_workers = 20
with concurrent.futures.ThreadPoolExecutor(max_workers) as thp:
    thp.map(get_apps_link, app_links)
