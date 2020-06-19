from twilio.rest import Client
from datetime import datetime, date
import requests
import time

BITCOIN_PRICE_THRESHOLD = 6000
today = date.today()

account_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice/GBP.json'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/x'


def get_latest_bitcoin_price():
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    gbp_response_json = response_json["bpi"]["GBP"]["rate"]
    pound_bitcoin = gbp_response_json.replace(',', '')
    print(pound_bitcoin)
    return float(pound_bitcoin)

"""    
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = ifttt_webhook_url.format(event)
    requests.post(ifttt_event_url, json=data)
"""    

def sms_notification(price):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to="+00000000000",
        from_="+00000000000",
        body="Bitcoin price is now at £" + str(price) + " .On " + str(today)
    )
    
    

def bitcoin_sms(bitcoin_history):
    client = Client(account_sid, auth_token)
    bitcoin_string = ' '.join(bitcoin_history)
    client.messages.create(
        to="+00000000000",
        from_="+00000000000",
        body=bitcoin_string
    )
    

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        
        row='{}:£{}'.format(date,price)
        rows.append(row)
    return '\n'.join(rows)    
  
  
def main():
    bitcoin_history = []
    
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price': price})
        
        #Sends an alert if the price is less that the threshold
        if price > BITCOIN_PRICE_THRESHOLD:
            #post_ifttt_webhook('bitcoin_price_emergency', price)
            sms_notification(price)
        
        
        if len(bitcoin_history) == 1:
            bitcoin_sms(bitcoin_history)
            print(bitcoin_history)
            print(type(bitcoin_history))
            bitcoin_history = []
        
        time.sleep(30)
        


            
            



if __name__ == '__main__':
   main()
 