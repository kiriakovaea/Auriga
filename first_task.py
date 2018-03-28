import bs4
import requests
import json
response = requests.get('http://www.auriga.com')
full_html = response.content.decode()
soup = bs4.BeautifulSoup(full_html, 'html.parser')
spisok = []
for a in soup.find_all('a', href=True):
 elem = dict(text = a.text, link = a['href'])
 spisok.append(elem)

with open('data.json', 'w') as outfile:
    json.dump(spisok, outfile)
outfile.close()