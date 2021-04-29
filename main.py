from flask import Flask
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup

prefix = "https://auto.ru/cars/"

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
  


@app.route('/get/<carModel>')
def getVaz(carModel):
  url = "https://auto.ru/cars/" + carModel + "/all/"
  r = requests.get(url)
  r.encoding = 'utf-8'
  soup = BeautifulSoup(r.text, 'html.parser')
  soup.prettify()
  app = soup.find('div', {'id': 'app'})
  return app.find(('div'), {'class' : 'ListingItem-module__main'}).text

if __name__ == '__main__':
  app.debug = True
  app.run()