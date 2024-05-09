

import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
import time 
import matplotlib.pyplot as plt
import os


mt.initialize()

login = #insert int
password = #insert str
server = #insert str

mt.login(login,password,server)

symbol = 'Volatility 75 Index'
timeframe = mt.TIMEFRAME_M10
date_from = datetime(2024,1,1)
#date_to = date_from
date_to = datetime.now()


'''
ticks = pd.DataFrame(mt.copy_ticks_from(symbol,date_from,100000000,mt.COPY_TICKS_ALL))
ticks['time'] = pd.to_datetime(ticks['time'],unit = 's')
ticks['time_msc'] = pd.to_datetime(ticks['time_msc'],unit = 'ms')
ticks.set_index('time', inplace=True)
'''


cPrices = pd.DataFrame(mt.copy_rates_range(symbol,timeframe,date_from,date_to))
cPrices['time'] = pd.to_datetime(cPrices['time'],unit = 'ms')
cPrices.set_index('time', inplace=True)

prices = (cPrices['open'] + cPrices['close'])/2
#prices = (ticks['bid'] + ticks['ask'])/2
listOf50Ar = []
priceOutcomeAr = []

#percent change between 2 numbers
def percentChange(start, current):
  return ((current - start)/abs(start))*100

#percent change between 2 arrays of numbers
def arPercentChange(ar1, ar2):
  percents = 0
  for i in range(0,50):
    percents += (100 - abs(percentChange(ar1[i], ar2[i]))) 
  return percents/50

#generate array of patterns (pattern of last 50 ticks)
for i in range (50,15000):
  listOf50 = []
  
  for pt in range(1,51):
    listOf50.append(percentChange(prices[i-50], prices[i-(50-pt)]))
  listOf50Ar.append(listOf50)
  priceOutcome = percentChange(prices[i-50], prices[i-(50-pt)+2])
  priceOutcomeAr.append(priceOutcome)   #the outcome of the pattern to compliment listof50ar
  if i%1000==0:
    os.system('cls')
    print(f'{((i/15000)*100)//1}%')

#current price to be predicted
for ar in range(15001, 15101):  #ar is current price
  print(f'####################{ar}')
  perList = []  #to get the accuracy of each signal for each current pattern
  currentPattern = []
  neededArOf50 = []
  ApriceOutcomeAr = []  #to be the same size as the neededArOf50
  for pt in range(1,51):
    currentPattern.append(percentChange(prices[ar-50], prices[ar-(50-pt)]))
  currentPriceOutcome = prices[ar-(50-pt)+2]   #the outcome of the current pattern

  for i in range(0, len(listOf50Ar)): #comparing pattern with saved pattern list, i is list of stored arrays
    per = arPercentChange(listOf50Ar[i], currentPattern)
    if per> 70:

      perList.append(per) #for signal accuracy
      neededArOf50.append(listOf50Ar[i])
      ApriceOutcomeAr.append(priceOutcomeAr[i])  #needed priceoutcome to compliment neededar0f50
      print(f'{per}% for {ar}_{i}')
  if len(neededArOf50)>0:
    print(f'{sum(perList)/float(len(perList))}% signal')

    colors = ['blue', 'green', 'red', 'cyan', 'magenta']
    # Plotting
    for idx, array in enumerate(neededArOf50):
        avrgPriceOutcome = []
        plt.plot(range(1, 51), array, color=colors[idx % len(colors)])
        '''if priceOutcome>0:
          plt.scatter(55, ApriceOutcomeAr[neededArOf50.index(array)], color = 'green', alpha=0.3)
          avrgPriceOutcome.append(ApriceOutcomeAr[neededArOf50.index(array)])
        else:
          plt.scatter(55, ApriceOutcomeAr[neededArOf50.index(array)], color = 'red', alpha=0.3)
          avrgPriceOutcome.append(ApriceOutcomeAr[neededArOf50.index(array)])
        plt.plot(60, currentPriceOutcome, color = 'blue')
        plt.plot(60, sum(avrgPriceOutcome)/len(avrgPriceOutcome), color = 'black')
'''
    plt.xlabel('Index')
    plt.ylabel(ar)
    plt.title('Multiple Lines Plot')
    plt.legend()

    plt.show()


