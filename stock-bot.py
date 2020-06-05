import robin_stocks as rs
import pandas as pd
from bs4 import BeautifulSoup
import requests

stock = 'TQQQ'

rs.login('username', 'password')

info = rs.get_historicals(stock, span = 'year')
df = pd.DataFrame(data = info, columns = ['close_price'])

s = df[-10:]
hist = s['close_price'].tolist()
hist = [float(i) for i in hist]

# Calculates the moving average over the course of a given number of days
def moving_average(days):
    total = sum(hist)
    return total / days


# Fast stochastic measurement
def fast_stochastic():
    temp_hist = hist

    cp = hist[-1]
    l = min(temp_hist)
    h = max(temp_hist)

    k = 100 * (cp - l)/(h - l)

    return k

#Relative Strength Index Calculator
def rsi():
    gain = 0
    g_count = 0
    loss = 0
    l_count = 0

    for x in range(1, len(hist)):
        if hist[x]<hist[x-1]:
            loss += -(hist[x]-hist[x-1])
            l_count += 1

        if hist[x]>hist[x-1]:
            gain += hist[x]-hist[x-1]
            g_count += 1

    r =  100 / (1 + ((gain/g_count)/(loss/l_count)))
    return 100 - r

#Web Scrape for CNN Fear and Greed Index
def scrape():
    fg_url = 'https://money.cnn.com/data/fear-and-greed/'
    fg = requests.get(fg_url)
    soup = BeautifulSoup(fg.content, features="lxml")
    x = soup.find_all(id='needleChart')
    x = str(x[0])
    pos = x.find('Greed Now: 65')

    r = x[pos:pos+14]
    s = float(x[pos+11:pos+14])
    return s


def show():
    print("Lastest Closing Price: " + str(hist[-1]))
    print("10-Day moving average: " + str(moving_average(10)))
    print('Fast Stochastic: ' + str(fast_stochastic()))
    print('Relative Strength Index: ' + str(rsi()))
    print(scrape())

if moving_average(10) > hist[-1] and fast_stochastic() < 20 and rsi() < 20 and scrape() < 45:
    show()
    print('Recommend Buy')
    #rs.order_buy_market(stock, 1)

elif moving_average(10) < hist[-1] and fast_stochastic() > 80 and rsi() > 80 and scrape() > 55:
    show()
    print('Recommend Sell')
    #rs.order_sell_market(stock, 1)

else:
    show()
    print('Recommend Wait')
