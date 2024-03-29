import sys
import requests
from bs4 import BeautifulSoup
import json
import time

URL = 'https://www.way2sms.com/api/v1/sendCampaign'

def send_message(stock_code, stockPrice):
  req_params = {
  'apikey':'xxxxxxxxxxxxxxxxxxxxxxxx',
  'secret':'xxxxxxxxxxxxxx',
  'usetype':'stage',
  'phone': '<Receiver mobile number>',
  'message':'Current stock price for ' + stock_code + ' is '  + str(stockPrice),
  'senderid':'Zafrul'
  }
  return requests.post(URL, req_params)

def fetch_NSE_stock_price(stock_code):
    
    stock_url  = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+str(stock_code)
    response = requests.get(stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_array = soup.find(id='responseDiv').getText().strip().encode('utf-8').split(":")
    
    for item in data_array:
        if 'lastPrice' in item:
            index = data_array.index(item)+1
            latestPrice=data_array[index].split('"')[1]
            return float(latestPrice.replace(',',''))
    

stock_code = sys.argv[1]
stock_threshold = float(sys.argv[2])

while True:

    current_stock_price = fetch_NSE_stock_price(stock_code)

    if current_stock_price > stock_threshold:
        print "you got it"
        response = send_message(stock_code, current_stock_price)
        print (response.text)
        break
    else:
        print 'Code : '+ stock_code + ' :  Current Value - ' + str(current_stock_price) + ' , Threshold - '+str(stock_threshold)

    time.sleep(2)