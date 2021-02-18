import requests
from bs4 import BeautifulSoup
import re

geekbrainsReq = requests.get("https://geekbrains.ru/events")
geekbrainsText = geekbrainsReq.text

soup = BeautifulSoup(geekbrainsText, 'lxml')
findList = soup.find("div", attrs={ 'class' : 'gb-future-events__items'})


i = 0
monthFirst = ""

for child in findList.children:
    date = child.find("div", attrs={ 'class' : 'gb-event-info__datetime'})
    title = child.find("h3", attrs={ 'class' : 'gb-event-info__item gb-event-info__title'})
    ElementInfo = child.find("ul", attrs={ 'class' : 'gb-item-stats gb-event-info__item'})
    countPeople = ElementInfo.li.text
    link = "https://geekbrains.ru" + title.a.get("href")

    month = date.text.split(" ")[2]
    month = re.sub('\,|\.', '', month)

    if i == 0:
        monthFirst = date.text.split(" ")[2]
        monthFirst = re.sub('\,|\.', '', monthFirst)

    if int(countPeople) < 30:
        continue

    if monthFirst != month:
        break


    i += 1

    print(date.text)
    print(title.text)
    print(link)
    print(countPeople)
    print(month)
    print()

print("Количество записей:", i)