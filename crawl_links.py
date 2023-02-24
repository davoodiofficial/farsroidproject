import requests
from bs4 import BeautifulSoup as bs

farsroid_sitemap_url = "https://www.farsroid.com/sitemap.xml"

r = requests.get(farsroid_sitemap_url, headers={"Accept": "application/xml"})


results = bs(r.content, 'lxml-xml')
results = results.find_all('sitemap')

for i in results:
    link = i.find('loc').contents[0]

    if "sitemap-pt" in link:
        print(link)


    