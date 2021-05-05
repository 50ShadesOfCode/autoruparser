from flask import Flask, jsonify, request
from flask.wrappers import Response
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
import json

prefix = "https://auto.ru/cars/"

HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Length': '137',
        'content-type': 'application/json',
        'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
        'Host': 'auto.ru',
        'origin': 'https://auto.ru',
        'Referer': 'https://auto.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'x-client-app-version': '202002.03.092255',
        'x-client-date': '1580933207763',
        'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
        'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
        'x-requested-with': 'fetch'
}

paramurls = {

  "car_state": "used/new/all",
  "car_mark" : "foreigners/ours/others",
  "car_body" : "bodies",
  "car_model" : "models", 
}

paraminurl = {
  "transmission":"AUTO",
  "year_from":"2021",
  "year_to":"2021",
  "engine_group" : "GASOLINE",
  "gear_type" : "FORWARD_CONTROL",
  "km_age_from" : "5000",
  "km_age_to" : "5000",
  "displacement_from" : "2424",
  "displacement_to" : "2454",
  "price_from":"5000",
  "price_to" : "56464",
}

def get_cars_by_params(params):
  url = ""
  r = requests.get(url)
  r.encoding = 'utf-8'
  soup = BeautifulSoup(r.text, 'html.parser')
  soup.prettify()
  app = soup.find('div', {'id': 'app'})
  return  app.find_all('div', {'class': 'ListingItem-module__main'})


def parseCard(cardText):
  return


@app.route('/get/<carModel>')
def getVaz(carModel):
  url = "https://auto.ru/cars/" + carModel + "/all/"
  r = requests.get(url)
  r.encoding = 'utf-8'
  soup = BeautifulSoup(r.text, 'html.parser')
  soup.prettify()
  app = soup.find('div', {'id': 'app'})
  return app.find(('div'), {'class' : 'ListingItem-module__main'}).text

def getCarByUrl(url):
  r = requests.get(url)
  r.encoding = 'utf-8'
  soup = BeautifulSoup(r.text, 'html.parser')
  soup.prettify()
  charsUrl = soup.find('a', { 'class' : 'Link SpoilerLink CardCatalogLink SpoilerLink_type_default'})['href']
  carDescription = soup.find('div', {'class' : 'CardDescription__textInner'}).find('span').text
  carDescription = modifyCarDesc(carDescription)
  carYear = soup.find('li', {'class' : 'CardInfoRow_year'}).find('a', {'class' : 'Link'}).text
  carKmage = soup.find('li', {'class' : 'CardInfoRow_kmAge'}).find('a', {'class' : 'Link'}).text
  carBodytype = soup.find('li', {'class' : 'CardInfoRow_bodytype'}).find('a', {'class' : 'Link'}).text
  carColor = soup.find('li', {'class' : 'CardInfoRow_color'}).find('a', {'class' : 'Link'}).text
  
  return carDescription

def modifyCarDesc(desc):
  desc = desc.replace('<span>', '')
  desc = desc.replace('</span>', '')
  desc = desc.replace('<br/>', '')
  desc = desc.replace('_', '')
  return desc

@app.route('/getCardByUrl', methods=['GET', 'POST'])
def getCardByUrl():
  rjson = request.json
  url = rjson.get("url")
  HEADERS['Referer']=url
  r = requests.get(url)
  r.encoding = 'utf-8'
  soup = BeautifulSoup(r.text, 'html.parser')
  soup.prettify()
  carKmage = soup.find('li', {'class' : 'CardInfoRow_kmAge'}).find_all('span', {'class' : 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
  carEngine = soup.find('li', {'class' : 'CardInfoRow_engine'}).find('div').text.replace(u'\xa0', ' ')
  carTransmission = soup.find('li', {'class' : 'CardInfoRow_transmission'}).find_all('span', {'class' : 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
  carColor = soup.find('li', {'class' : 'CardInfoRow_color'}).find_all('span', {'class' : 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
  carDrive = soup.find('li', {'class' : 'CardInfoRow_drive'}).find_all('span', {'class' : 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
  carBody = soup.find('li', {'class' : 'CardInfoRow_bodytype'}).find_all('span', {'class' : 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
  images = soup.find_all('img', {'class': 'ImageGalleryDesktop__image'})
  image_urls = []
  for image in images:
    image_urls.append(image['src'])
  js = json.loads({
    "kmage": carKmage, 
    "engine": carEngine,
    "transmission": carTransmission,
    "color" : carColor,
    "drive": carDrive,
    "body": carBody,
    "images_urls": image_urls,
  })
  return js

@app.route("/")
def getHome():
  return "ads"

def getCarCharsByUrl(url):
  return

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
  #print(getCardByUrl('https://auto.ru/cars/used/sale/mercedes/gle_klasse_coupe/1103168273-6ac4b173/'))
