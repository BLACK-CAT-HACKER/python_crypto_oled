import requests
import json
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

oled = sh1106(i2c(port=1, address=0x3C))

usd_inr_url = "https://free.currconv.com/api/v7/convert?q=USD_INR&compact=ultra&apiKey=897fcc909d9b77a950b2"
crypto_url = "https://api.cryptonator.com/api/ticker/{}-usd"
cryptos = ["btc"]
prices_usd = prices_inr = []

headers = {
    'User-Agent' : 'My User Agent 1.0'
}
def get_usd_inr():
    return json.loads(requests.request("GET", usd_inr_url).text)["USD_INR"]

def get_all_crypto_prices():
    usd = []
    inr = []
    usd_inr = get_usd_inr()
    for crypto in cryptos:
        price_usd = float(json.loads(requests.request("GET", crypto_url.format(crypto), headers=headers).text)["ticker"]["price"])
        price_inr = price_usd * usd_inr
        usd.append(price_usd)
        inr.append(price_inr)
    return usd, inr

def tick_display():
    global prices_usd, prices_inr

    for index, crypto in enumerate(cryptos):
        with canvas(oled) as draw:
            draw.text((30, 0), "CRYPTO RATES", fill="white")
            draw.text((55, 15), crypto.upper(), fill="white")
            draw.text((0, 30), "USD: {}".format(prices_usd[index]), fill="white")
            draw.text((0, 45), "INR: {}".format(prices_inr[index]), fill="white")
            time.sleep(5)
while True:
    prices_usd, prices_inr =get_all_crypto_prices()
    tick_display()