import requests
from bs4 import BeautifulSoup

URL = "https://www.farsroid.com/bikes-hill/"
page = requests.get(URL)
print(page.status_code)

soup = BeautifulSoup(page.content, "html.parser")
downloadbox = soup.find("table",class_="post-metas-tabeld")
infos = downloadbox.find("tbody")


googleplay_link=soup.find("a",class_="shadowed-btn gply-link")
tr = soup.find_all("tr")
for i in tr:
    td = i.find("td")
    span = i.find("th").find_all("span")[1]
    print(span.text)
    print(td.text)
        






# print(downloadbox.prettify())
# print(googleplay_link.get("data-link"))
# print(googleplay_link.get("title"))
# print(infos.prettify())




