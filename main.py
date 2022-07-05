import json
from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify, request
from flask.wrappers import Response
application = Flask(__name__)

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
    "car_mark": "foreigners/ours/others",
    "car_body": "bodies",
    "car_model": "models",
}

paraminurl = {
    "transmission": "AUTO",
    "year_from": "2021",
    "year_to": "2021",
    "engine_group": "GASOLINE",
    "gear_type": "FORWARD_CONTROL",
    "km_age_from": "5000",
    "km_age_to": "5000",
    "displacement_from": "2424",
    "displacement_to": "2454",
    "price_from": "5000",
    "price_to": "56464",
}

@application.route('/makePageUrl', methods=['GET', 'POST'])
def make_page_url():
    url = prefix
    mark = request.json.get('mark')
    if mark != "":
        url = url + mark + '/all/?'
    else:
        url = url + 'all/?'
    bodytype = request.json.get('body')
    if bodytype != None:
        url = url + 'body_type_group=' + bodytype + '&'
    transmission = request.json.get('transmission')
    if transmission != None:
        url = url + 'transmission=' + transmission + '&'
    year_from = request.json.get('year_from')
    if year_from != None:
        url = url + 'year_from=' + year_from + '&'
    year_to = request.json.get('year_to')
    if year_to != None:
        url = url + 'year_to=' + year_to + '&'
    gear_type = request.json.get('gear_type')
    if gear_type != None:
        url = url + 'gear_type=' + gear_type + '&'
    km_age_from = request.json.get('km_age_from')
    if km_age_from != None:
        url = url + 'km_age_from=' + km_age_from + '&'
    km_age_to = request.json.get('km_age_to')
    if km_age_to != None:
        url = url + 'km_age_to=' + km_age_to + '&'
    displacement_from = request.json.get('displacement_from')
    if displacement_from != None:
        url = url + 'displacement_from=' + displacement_from + '&'
    displacement_to = request.json.get('displacement_to')
    if displacement_to != None:
        url = url + 'displacement_to=' + displacement_to + '&'
    price_from = request.json.get('price_from')
    if price_from != None:
        url = url + 'price_from=' + price_from + '&'
    price_to = request.json.get('price_to')
    if price_to != None:
        url = url + 'price_to=' + price_to + '&'
    return jsonify({"url":url})

@application.route('/getCarsByParams', methods=['GET', 'POST'])
def get_cars_by_params():
    r = requests.get(request.json.get("url"))
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.prettify()
    app = soup.find('div', {'id': 'app'})
    car_urls = []
    for a in app.find_all('a', {'class': 'Link OfferThumb'}):
        car_urls.append(a['href'])
    return jsonify({"urls": car_urls})

@application.route('/getCarByUrl', methods=['GET', 'POST'])
def getCarByUrl():
    r = requests.get(request.json.get('url'))
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.prettify()
    charsUrl = soup.find(
        'a', {'class': 'Link SpoilerLink CardCatalogLink SpoilerLink_type_default'})['href']
    carDescription = soup.find(
        'div', {'class': 'CardDescription__textInner'}).find('span').text
    carDescription = modifyCarDesc(carDescription)
    carYear = soup.find('li', {'class': 'CardInfoRow_year'}).find(
        'a', {'class': 'Link'}).text
    carKmage = soup.find('li', {'class': 'CardInfoRow_kmAge'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carBody = soup.find('li', {'class': 'CardInfoRow_bodytype'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carColor = soup.find('li', {'class': 'CardInfoRow_color'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carEngine = soup.find('li', {'class': 'CardInfoRow_engine'}).find(
        'div').text.replace(u'\xa0', ' ')
    carTransmission = soup.find('li', {'class': 'CardInfoRow_transmission'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carDrive = soup.find('li', {'class': 'CardInfoRow_drive'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carWheel = soup.find('li', {'class': 'CardInfoRow_wheel'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carState = soup.find('li', {'class': 'CardInfoRow_state'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carOwners = soup.find('li', {'class': 'CardInfoRow_ownersCount'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carPts = soup.find('li', {'class': 'CardInfoRow_pts'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carCustoms = soup.find('li', {'class': 'CardInfoRow_customs'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    images = soup.find_all('img', {'class': 'ImageGalleryDesktop__image'})
    image_urls = []
    for image in images:
        tmp = "http:" + image['src']
        print(tmp)
        image_urls.append(tmp)
    return jsonify({
        "kmage": carKmage,
        "engine": carEngine,
        "transmission": carTransmission,
        "color": carColor,
        "drive": carDrive,
        "body": carBody,
        "images_urls": image_urls,
        "year": carYear,
        "wheel": carWheel,
        "state": carState,
        "owners": carOwners,
        "pts": carPts,
        "customs": carCustoms,
        "desc":carDescription,
        "chars":charsUrl,
    })


def modifyCarDesc(desc):
    desc = desc.replace('<span>', '')
    desc = desc.replace('</span>', '')
    desc = desc.replace('<br/>', '')
    desc = desc.replace('_', '')
    return desc


@application.route('/getCardByUrl', methods=['GET', 'POST'])
def getCardByUrl():
    rjson = request.json
    url = rjson.get("url")
    HEADERS['Referer'] = url
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.prettify()
    carKmage = soup.find('li', {'class': 'CardInfoRow_kmAge'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carEngine = soup.find('li', {'class': 'CardInfoRow_engine'}).find(
        'div').text.replace(u'\xa0', ' ')
    carTransmission = soup.find('li', {'class': 'CardInfoRow_transmission'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carColor = soup.find('li', {'class': 'CardInfoRow_color'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carDrive = soup.find('li', {'class': 'CardInfoRow_drive'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carBody = soup.find('li', {'class': 'CardInfoRow_bodytype'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    images = soup.find_all('img', {'class': 'ImageGalleryDesktop__image'})
    image_urls = []
    for image in images:
        tmp = image['src']
        image_urls.append(tmp[2:])
    return jsonify({
        "kmage": carKmage,
        "engine": carEngine,
        "transmission": carTransmission,
        "color": carColor,
        "drive": carDrive,
        "body": carBody,
        "images_urls": image_urls,
    })


@application.route("/")
def getHome():
    return "ads"

@application.route('/getCharsByUrl', methods=['GET', 'POST'])
def getCarCharsByUrl():
    r = requests.get(request.json.get('url'))
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.prettify()
    groups = soup.find_all('div', {'class':'catalog__details-group'})
    for group in groups:
      group.prettify()
    carCountry = groups[0].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carClass = groups[0].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')
    carDoors = groups[0].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')
    carPlaces = groups[0].find('dd', {'class': 'list-values__value'})[3].text.replace(u'\xa0', ' ')

    carLength = groups[1].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carWidth = groups[1].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')
    carHeight = groups[1].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')
    carBase = groups[1].find('dd', {'class': 'list-values__value'})[3].text.replace(u'\xa0', ' ')
    carClirense = groups[1].find('dd', {'class': 'list-values__value'})[4].text.replace(u'\xa0', ' ')
    carFrWidth = groups[1].find('dd', {'class': 'list-values__value'})[5].text.replace(u'\xa0', ' ')
    carBackWidth = groups[1].find('dd', {'class': 'list-values__value'})[6].text.replace(u'\xa0', ' ')

    carBackVolume = groups[2].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carFuelVolume = groups[2].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')

    carTransmission = groups[3].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carNumberTrans = groups[3].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')
    carPrivod = groups[3].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')   

    carFrSusp = groups[4].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')     
    carBackSusp = groups[4].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')    
    carFrBrakes = groups[4].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')    
    carBackBrakes = groups[4].find('dd', {'class': 'list-values__value'})[3].text.replace(u'\xa0', ' ')   

    carMaxSpeed = groups[5].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carRacing = groups[5].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')
    carWaste = groups[5].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')
    carFuelMark = groups[5].find('dd', {'class': 'list-values__value'})[3].text.replace(u'\xa0', ' ')
    carEcoClass = groups[5].find('dd', {'class': 'list-values__value'})[4].text.replace(u'\xa0', ' ')
    carCo2 = groups[5].find('dd', {'class': 'list-values__value'})[5].text.replace(u'\xa0', ' ')
    
    carEngType = groups[6].find('dd', {'class': 'list-values__value'})[0].text.replace(u'\xa0', ' ')
    carEngPos = groups[6].find('dd', {'class': 'list-values__value'})[1].text.replace(u'\xa0', ' ')
    carEngVolume = groups[6].find('dd', {'class': 'list-values__value'})[2].text.replace(u'\xa0', ' ')
    carBoost = groups[6].find('dd', {'class': 'list-values__value'})[3].text.replace(u'\xa0', ' ')
    carMaxPower = groups[6].find('dd', {'class': 'list-values__value'})[4].text.replace(u'\xa0', ' ')
    carMaxTurn = groups[6].find('dd', {'class': 'list-values__value'})[5].text.replace(u'\xa0', ' ')
    carCylPos = groups[6].find('dd', {'class': 'list-values__value'})[6].text.replace(u'\xa0', ' ')
    carCylNum = groups[6].find('dd', {'class': 'list-values__value'})[7].text.replace(u'\xa0', ' ')
    carClapNum = groups[6].find('dd', {'class': 'list-values__value'})[8].text.replace(u'\xa0', ' ')
    carFeedSystem = groups[6].find('dd', {'class': 'list-values__value'})[9].text.replace(u'\xa0', ' ')
    carPressure = groups[6].find('dd', {'class': 'list-values__value'})[10].text.replace(u'\xa0', ' ')
    carDiameter = groups[6].find('dd', {'class': 'list-values__value'})[11].text.replace(u'\xa0', ' ')
    return jsonify({
        "country":carCountry,
        "class":carClass,
        "doors":carDoors,
        "places":carPlaces,
        "length": carLength,
        "width":carWidth,
        "height":carHeight,
        "base":carBase,
        "clirense":carClirense,
        "frwidth":carFrWidth,
        "backwidth":carBackWidth,
        "backvolume":carBackVolume,
        "fuelvolume":carFuelVolume,
        "traansmission":carTransmission,
        "numberTrans":carNumberTrans,
        "privod":carPrivod,
        "frsusp":carFrSusp,
        "backsusp":carBackSusp,
        "frbrakes": carFrBrakes,
        "backbrakes":carBackBrakes,
        "maxspeed":carMaxSpeed,
        "racing":carRacing,
        "waste":carWaste,
        "fuelmark":carFuelMark,
        "ecoclass":carEcoClass,
        "co2":carCo2,
        "engtype":carEngType,
        "engpos":carEngPos,
        "engvolume":carEngVolume,
        "boost":carBoost,
        "maxpower":carMaxPower,
        "maxturn":carMaxTurn,
        "cylpos":carCylPos,
        "cylnum":carCylNum,
        "clapnum":carClapNum,
        "feedsystem":carFeedSystem,
        "pressure":carPressure,
        "diameter":carDiameter,
    })



if __name__ == '__main__':
    application.run(host='0.0.0.0')
    # print(getCardByUrl('https://auto.ru/cars/used/sale/mercedes/gle_klasse_coupe/1103168273-6ac4b173/'))
