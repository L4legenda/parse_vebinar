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

testPost = "Приглашаем принять участие в вебинарах\n\n"
dif = 7 - datetime.now().isoweekday()

listDate = []
for d in range(1, 7):
    listDate.append(datetime.now() + timedelta(days=dif + d))

for child in findList.children:
    date = child.find("div", attrs={ 'class' : 'gb-event-info__datetime'})
    title = child.find("h3", attrs={ 'class' : 'gb-event-info__item gb-event-info__title'})
    ElementInfo = child.find("ul", attrs={ 'class' : 'gb-item-stats gb-event-info__item'})
    link = "https://geekbrains.ru" + title.a.get("href")

    if date == None or title == None or ElementInfo == None:
        continue

    countPeople = ElementInfo.li.text

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
                    skip = False

    if skip:
        continue
    testPost += f"✅ {date.text} — «{title.text}»: {link}\n\n"

print(testPost)
print("Количество записей:", i)

