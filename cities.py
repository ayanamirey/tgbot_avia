import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

link = 'https://ru.wikinews.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
full_page = requests.get(link, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser', )

convert = soup.findAll("div", {"class": "CategoryTreeItem"})
c = []
for i in range(len(convert)):
    c.append(convert[i].text)

city = []
for i in c:
    i = i.lstrip().split()
    city.append(i[0])
