import requests
from bs4 import BeautifulSoup as bs

def get_apps_link(link):
    r = requests.get(link, headers={"Accept": "application/xml"})
    results = bs(r.content,'lxml-xml')
    results = results.find_all('url')

    lst = []

    for j in results :
        app_link = j.find('loc').contents[0]
        lst.append(app_link)
    
    return lst



farsroid_sitemap_url = "https://www.farsroid.com/sitemap.xml"

r = requests.get(farsroid_sitemap_url, headers={"Accept": "application/xml"})


results = bs(r.content, 'lxml-xml')
results = results.find_all('sitemap')


for i in results:
    link = i.find('loc').contents[0]

    if "sitemap-pt" in link:
        apps_link= get_apps_link(link)
        print(*apps_link , sep='\n')
