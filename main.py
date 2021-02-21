import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

geekbrainsReq = requests.get("https://geekbrains.ru/events")
geekbrainsText = geekbrainsReq.text

soup = BeautifulSoup(geekbrainsText, 'lxml')
findList = soup.find("div", attrs={ 'class' : 'gb-future-events__items'})

mouthList = ("января", "февраля","марта","апреля","мая","июня", "июля",
         "августа", "сентября", "октября", "ноября", "декабря")

i = 0

dif = 7 - datetime.now().isoweekday()

print(dif)
listDate = []
for d in range(1, 7):
    listDate.append(datetime.now() + timedelta(days=dif + d))

print(listDate)

for child in findList.children:
    date = child.find("div", attrs={ 'class' : 'gb-event-info__datetime'})
    title = child.find("h3", attrs={ 'class' : 'gb-event-info__item gb-event-info__title'})
    ElementInfo = child.find("ul", attrs={ 'class' : 'gb-item-stats gb-event-info__item'})
    countPeople = ElementInfo.li.text
    link = "https://geekbrains.ru" + title.a.get("href")

    day = date.text.split(" ")[1]
    day = re.sub('\,|\.', '', day)
    day = int(day.strip())

    month = date.text.split(" ")[2]
    month = re.sub('\,|\.', '', month)

    skip = True

    for i, m in enumerate(mouthList):
        if month in m:

            for lDate in listDate:
                if day == lDate.day and i + 1 == lDate.month:
                    print("Good")
                    skip = False

    if skip:
        continue

    i += 1

    print(date.text)
    print(title.text)
    print(link)
    print(countPeople)
    print(month)
    print()

print("Количество записей:", i)

