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

# ktk-45
# headers = {"Authorization" : "7cae34465dce7b9a1dea92a96bf3c9e3e1260fed2f168e9721efa0c955f1e9cc"}
# ktk-dev
headers = {"Authorization" : "8eef307acfc5d02c4a7558b529ceefb6fa11f52c856a86979ebc430c3f02122a"}

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

    times = date.text.split(",")[2].strip()[:5]

    hour = int(times.split(":")[0])
    minute = int(times.split(":")[1])

    countPeople = ElementInfo.li.text

    day = date.text.split(" ")[1]
    day = re.sub('\,|\.', '', day)
    day = int(day.strip())

    month = date.text.split(" ")[2]
    month = re.sub('\,|\.', '', month)

    skip = True

    saveDate = None

    for i, m in enumerate(mouthList):
        if month in m:
            for lDate in listDate:
                if day == lDate.day and i + 1 == lDate.month:
                    skip = False
                    saveDate = lDate
    if skip:
        continue

    saveDate = saveDate.replace(hour=hour, minute=minute, second=0)
    
    # print(saveDate + " " + times)
    # print(datetime.strptime(saveDate + " " + times, ""))

    # saveDate.timedelta(hours=)

    # requests.post("http://ktk-dev.ru/api/event/insert", headers=headers, data={
    #     "Date" : 
    # })
    print("Название:", title.text)
    print("Место проведение:", "Онлайн")
    print("Время начала:", saveDate)
    print("Ссылка:", link)
    print()

