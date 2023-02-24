import requests
from bs4 import BeautifulSoup as bs

farsroid_sitemap_url = "https://www.farsroid.com/sitemap.xml"

r = requests.get(farsroid_sitemap_url, headers={"Accept": "application/xml"})

print(r.status_code)
print(r.headers['Content-type'])
print(r.content.decode()[:100])
results = bs(r.content, 'lxml-xml')
results = results.find_all('sitemap')

for i in results[-10:]:
	print(i)