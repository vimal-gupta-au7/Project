
import time
import json
import datetime
import requests
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'1',
  'convert':'INR'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '6e40c521-fd3c-4262-b1b6-14e798e7095e',
}

bitcoin_threshold = 500000
WebHookUrl = 'https://maker.ifttt.com/trigger/{}/with/key/cpC_P0BFq0kzW5fNujStTv'

def getLatestPrice():
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, params = parameters)
    data = json.loads(response.text)
    price = float(data['data'][0]['quote']['INR']['price'])
    return round(price, 2)

def ifttt_webhook(event, value):
    data = {'value1' : value}   
    Ifttt_event_url = WebHookUrl.format(event)
    requests.post(Ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y')
        time = bitcoin_price['date'].strftime('%H:%M:%S')
        price = bitcoin_price['price']
        row = 'Date: {} Time: {}<br>Price: ₹<b>{}</b>'.format(date, time, price)
        rows.append(row)
    
    return'<br>'.join(rows)

def main():
    bitcoin_history = []
    while True:
        price = getLatestPrice()
        date = datetime.datetime.now()
        bitcoin_history.append({'date' : date, 'price' : price})

        if price < bitcoin_threshold:
            ifttt_webhook('BitcoinPriceEmergency', price)
        
        if len(bitcoin_history) == 5:
            ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []
        time.sleep(5 * 60)
        print(len(bitcoin_history))
if __name__ == "__main__":
    main()