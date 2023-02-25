import requests
from bs4 import BeautifulSoup

URL = "https://www.farsroid.com/bikes-hill/"
API = "https://www.farsroid.com/api/posts/?ids="
page = requests.get(URL)
# print(page.status_code)

soup = BeautifulSoup(page.content, "html.parser")
downloadbox = soup.find("table",class_="post-metas-tabeld")
infos = downloadbox.find("tbody")


googleplay_link=soup.find("a",class_="shadowed-btn gply-link")
# print(googleplay_link)

tr = soup.find_all("tr")
for i in tr:
    key = i.find("th").find_all("span")[1]
    value = i.find("td")
    print(key.text.strip())
    if key.text == 'تعداد بازدید':
        value = value.find('span').find('i').get('data-id')
        r = requests.get(API+value)
        value = r.json()['data'][0]['views']
        # print(r.json()['data'][0]['views'])
    else:
        value = value.text

    print(value.strip())

# print(downloadbox.prettify())
print(googleplay_link.get("data-link").strip())
title = googleplay_link.get("title")

en_name_found = True
fa_name_found = False

fa_name = ''
en_name = ''
# Bikes Hill 2.6.0 – بازی مسابقه ای “دوچرخه سواری در تپه ها” اندروید + مود
for j in title:
    if j == "–":
        en_name_found=False
        continue
    if j == '“' or j == '”':
        fa_name_found = not fa_name_found
        continue
    if en_name_found:
        en_name += j
    elif fa_name_found:
        fa_name += j

print(f'fa name "{fa_name.strip()}, en name "{en_name.strip()}"')