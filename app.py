from bs4 import BeautifulSoup #библиотека парсера
from requests_futures.sessions import FuturesSession
from quart import Quart, request, jsonify
from quart_cors import cors
import lxml
import cchardet
import logging

app = Quart(__name__)
app = cors(app, allow_origin="*")

#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='./profile')

session = FuturesSession()

@app.route('/', methods=['GET'])
async def home():
    r = session.get('https://auto.ru/cars/bmw/all/').result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    app = soup.find('div', {'id': 'app'})
    car_urls = []
    for a in app.find_all('a', {'class': 'Link OfferThumb'}):
        car_urls.append(a['href'])
        print(car_urls)
    return 'Homepage'

#получает все автомобили с заданными параметрами
@app.route('/getCarsByParams', methods=['GET', 'POST'])
async def get_cars_by_params():
    data = await request.get_json()
    url = data["url"]
    r = session.get(url).result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    app = soup.find('div', {'id': 'app'})
    car_urls = []
    for a in app.find_all('a', {'class': 'Link OfferThumb'}):
        car_urls.append(a['href'])
    return jsonify({"urls": car_urls})

#получает данные о автомобиле в зависимости от того какой он, новый или подержаный
@app.route('/getCarByUrl', methods=['GET', 'POST'])
async def getCarByUrl():
    data = await request.get_json()
    url = data["url"]
    r = session.get(url).result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    name = soup.find('div', {'class': 'CardSidebarActions__title'})
    carName = "Нет названия"
    if name != None:
        carName = name.text.replace(u'\xa0', ' ')
    charsUrl = soup.find(
        'a', {'class': 'Link SpoilerLink CardCatalogLink SpoilerLink_type_default'})['href']
    carDescription = soup.find(
        'div', {'class': 'CardDescription__textInner'}).text
    price = soup.find('span', {'class': 'OfferPriceCaption__price'})
    carPrice = "Нет цены"
    if price != None:
        carPrice = price.text.replace(u'\xa0', ' ')
    carDescription = modifyCarDesc(carDescription)
    carBody = soup.find('li', {'class': 'CardInfoRow_bodytype'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carEngine = soup.find('li', {'class': 'CardInfoRow_engine'}).find(
        'div').text.replace(u'\xa0', ' ')
    carTransmission = soup.find('li', {'class': 'CardInfoRow_transmission'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carColor = soup.find('li', {'class': 'CardInfoRow_color'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    carDrive = soup.find('li', {'class': 'CardInfoRow_drive'}).find_all(
        'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
    images = soup.find_all('img', {'class': 'ImageGalleryDesktop__image'})
    image_urls = []
    for image in images:
        tmp = "http:" + image['src']
        image_urls.append(tmp)
    if str(url).find("/new/") == -1: 
        carYear = soup.find('li', {'class': 'CardInfoRow_year'}).find(
            'a', {'class': 'Link'}).text
        carKmage = soup.find('li', {'class': 'CardInfoRow_kmAge'}).find_all(
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
        return jsonify({
            "name":carName,
            "price":carPrice,
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
    else:
        carComplectation = soup.find('li', {'class': 'CardInfoGrouped__row_complectation_name'}).find(
            'div', {'class': 'CardInfoGrouped__cellValue'}).text.replace(u'\xa0', ' ')
        carTax = soup.find('li', {'class': 'CardInfoGrouped__row_transportTax'}).find(
            'div', {'class': 'CardInfoGrouped__cellValue'}).text.replace(u'\xa0', ' ')
        return jsonify({
            "name": carName,
            "price":carPrice,
            "engine": carEngine,
            "transmission": carTransmission,
            "color": carColor,
            "drive": carDrive,
            "body": carBody,
            "images_urls": image_urls,
            "complectation": carComplectation,
            "tax": carTax,
            "chars":charsUrl,
            "desc":carDescription
        })

#получает число автомобилей с заданными параметрами
@app.route('/getNotUpdate', methods=['GET', 'POST'])
async def getNotUpdate():
    data = await request.get_json()
    url = data["url"]
    r = session.get(url).result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    t = soup.find('button', {'class':'Button Button_color_blue Button_size_m Button_type_button Button_width_full'})
    if (t == None):
        return "0"
    else:
        return t.text.replace(u'\xa0', ' ')

#убирает из описания теги
def modifyCarDesc(desc):
    desc = desc.replace('<span>', '')
    desc = desc.replace('</span>', '')
    desc = desc.replace('<br/>', '')
    desc = desc.replace('_', '')
    return desc

#получает данные о карточке по ссылке
@app.route('/getCardByUrl', methods=['GET', 'POST'])
async def getCardByUrl(): 
    data = await request.get_json()
    url = data["url"]
    r = session.get(url).result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    name = soup.find('h1', {'class': 'CardHead__title'})
    carName = "Нет названия"
    if name != None:
        carName = name.text.replace(u'\xa0', ' ')
    price = soup.find('span', {'class': 'OfferPriceCaption__price'})
    carPrice = "Нет цены"
    if price != None:
        carPrice = price.text.replace(u'\xa0', ' ')
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
    if str(url).find("/new/") == -1:
        carKmage = soup.find('div', {'class':'CardOfferBody__leftColumn'}).find('li', {'class': 'CardInfoRow CardInfoRow_kmAge'}).find_all(
            'span', {'class': 'CardInfoRow__cell'})[1].text.replace(u'\xa0', ' ')
        return jsonify({
            "name":carName,
            "kmage": carKmage,
            "engine": carEngine,
            "transmission": carTransmission,
            "color": carColor,
            "drive": carDrive,
            "body": carBody,
            "name":carName,
            "price":carPrice,
            "images_urls": image_urls,
        })
    else:
        carComplectation = soup.find('li', {'class': 'CardInfoGrouped__row_complectation_name'}).find(
            'div', {'class': 'CardInfoGrouped__cellValue'}).text.replace(u'\xa0', ' ')
        return jsonify({
            "name":carName,
            "engine": carEngine,
            "price":carPrice,
            "transmission": carTransmission,
            "color": carColor,
            "drive": carDrive,
            "body": carBody,
            "images_urls": image_urls,
            "complectation": carComplectation,
        })

#получает все характеристики автомобиля и преобразовавывает их в JSON
@app.route('/getCharsByUrl', methods=['GET', 'POST'])
async def getCarCharsByUrl():
    data = await request.get_json()
    url = data["url"]
    r = session.get(url).result()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    soup.prettify()
    traits = soup.find_all('dt', {'class': 'list-values__label'})
    vals = soup.find_all('dd', {'class': 'list-values__value'})
    res = {str(traits[a].text): str(vals[a].text) for a in range(len(traits))}
    return jsonify(res)


if __name__ == '__main__':
    app.run()
