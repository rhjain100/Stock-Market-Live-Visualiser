#! python3.7

from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
#import pandas_datareader.data as web
#import quandl
import csv
import numpy as np
import bs4 as bs
import pickle
import requests
from collections import OrderedDict
import time
from pynput import keyboard
import threading

quandl.ApiConfig.api_key = "yirX6eaKyzYkhhfH4dnF"
style.use('ggplot')
items=[]
n=0

def infiniteloop1():
    global items
    global n
    x=datetime.now().minute
    print('')
    print("Key Options: \n 1. Alt to exit. \n 2. Ctrl to refresh now.")
    print('')
    while True:
        if (datetime.now().minute-x) % 2 == 0:
            df = getnsedata()
            numrows=len(df.index)
            for i in range(len(items)):
                print(df[df['symbol']==items[i]][['symbol','high','low']])
                #symbols.append(df[df['symbol']==items[i]]['symbol'])
                #highs.append(df[df['symbol']==items[i]]['high'])
                #lows.append(df[df['symbol']==items[i]]['low'])    
            time.sleep(60)
        
        
def infiniteloop2():
    while True:
        get_current_key_input()
    


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
        key.char))
    except AttributeError:
        if key == keyboard.Key.alt: 
            exit()
        elif key == keyboard.Key.ctrl:
            global items
            a= len(items)
            df = getnsedata()
            for i in range(a):
                print(df[df['symbol']==items[i]][['symbol','high','low']])
        else:
            pass
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    else:
        pass
       
def get_current_key_input():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

'''
def nsetable():
        resp= requests.get('https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm')
        soup= bs.BeautifulSoup(resp.text, 'lxml')
        table= soup.find('div', {'class':'tabular_data_live_analysis'})
        tickers=[]
        print(resp.
        for row in table.findAll('tr')[1:]:
            ticker=row.findAll('td')[0].text
            tickers.append(ticker)

        with open('', 'wb') as f:
            pickle.dump(tickers, f)

        print(tickers)

        return tickers
'''

def getnsedata():
    resp=requests.get('https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json').json()
    data= resp['data']
    df= pd.DataFrame(data)
    return df
    

def getnow():
    now=datetime.now()-timedelta(1)
    date = datetime(now.year, now.month, now.day)
    return date

def getdate(date_entry):
    year, month, day = map(int, date_entry.split('-'))
    date = datetime(year, month, day)
    return date
    
def getcode():
    code=input("Enter stock symbol:")
    return code

print(
'''Select Task:
   1. Get data of a particular security.
   2. Compare different securities using a csv file (should be downloaded in the same folder).
   3. Get live data from NSE with Update Every 5 minutes(Program runs for an hour).''')
x=int(input())

if x==1:
    s=getcode()
    date_entry1=input("Enter Start date (YYYY-MM-DD): ")
    start=getdate(date_entry1)
    date_entry2=input("Enter End date:(YYYY-MM-DD): ")
    end= getdate(date_entry2)
    data = quandl.get('NSE/'+s, start_date=start, end_date=end)
  
    print (data[['High','Low']].tail())
    data[['High','Low']].plot()
    plt.show()


elif x==2:
    labels=['Symbol','Open','High','Low','Last Traded Price','Change','%Change','Traded Volume(lacs)','Traded Value(crs)','52 Week High','52 Week High','365 Days % Change','30 Days % Change']
    f= open('data.csv')
    csv_f=csv.reader(f, delimiter=',')
    li=[]
    symbols=[]
    highs=[]
    lows=[]
    items=[]
    a=int(input('Enter the number of stocks you want to compare: '))
    for i in range(a):
        print('Enter stock symbol no.', end='')
        print(i+1, end='')
        print(': ')
        item=input()
        items.append(item)        
    
    for row in csv_f:
        x=0
        for i in range(a):
            if row[0]==items[i]:
                x+=1
        if x>0:
            symbols.append(row[0])
            highs.append(row[2])
            lows.append(row[3])
            li.append(row)
    df = pd.DataFrame.from_records(li, columns=labels)
    print(df.tail())
    y_pos=np.arange(len(symbols))
    plt.bar(y_pos, highs)
    plt.xticks(y_pos,symbols)
    plt.show()
    f.close()
    
elif x==3:
    a=int(input('Enter the number of stocks you want to compare: '))
    for i in range(a):
        print('Enter stock symbol no.', end='')
        print(i+1, end='')
        print(': ',end='')
        item=input()
        items.append(item)
    
    n= int(input('Enter refresh time (minutes): '))
    thread1 = threading.Thread(target=infiniteloop1)
    thread1.start()

    thread2 = threading.Thread(target=infiniteloop2)
    thread2.start()

        
                
        

    
'''
try:
        sym=input("What symbols high do you want to know? \n")
        x=symbols.index(sym)
        print(highs[x])

    except Exception as e:
        print(e)
'''
        




