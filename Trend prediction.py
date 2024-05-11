'''
this version compares the current trend and
matches it with similar trends from the past.
it then shows the outcome of the matched 
past trends
'''


import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
import time 
import matplotlib.pyplot as plt
import os


mt.initialize()

login = 5437786
password = 'dddDDD666---'
server = 'Deriv-Demo'

mt.login(login,password,server)

symbol = 'Drift Switch Index 30'
timeframe = mt.TIMEFRAME_M5
date_from = datetime(2024,1,1)
date_to = datetime.now()


cPrices = pd.DataFrame(mt.copy_rates_range(symbol,timeframe,date_from,date_to))
cPrices['time'] = pd.to_datetime(cPrices['time'],unit = 'ms')
cPrices.set_index('time', inplace=True)

prices = (cPrices['open'] + cPrices['close'])/2
#prices = (ticks['bid'] + ticks['ask'])/2
listOf75Ar = []
listOf25Ar = []
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

def arPercentChange25(ar1, ar2):
  percents = 0
  for i in range(50,75):
    percents += (100 - abs(percentChange(ar1[i], ar2[i]))) 
  return percents/50

#generate array of patterns (pattern of last 75 prices)
for i in range (75,30000):
  listOf75 = []
  listOf25 = []
  
  for pt in range(1,76):
    listOf75.append(percentChange(prices[i-75], prices[i-(75-pt)]))
  listOf75Ar.append(listOf75)
  for pt in range(1,26):
    listOf25.append(percentChange(prices[i-75], prices[i-(25-pt)]))
  listOf25Ar.append(listOf25)
  if i%300==0:
    os.system('cls')
    print(f'{((i/30000)*100)//1}%')

#current price to be predicted
for ar in range(30001, 30101):  #ar is current price
  print(f'####################{ar}')
  perList = []  #to get the accuracy of each signal for each current pattern
  currentPattern = []
  currentPatternOutcome = []
  neededArOf50 = []
  neededArOf25 = []
  for pt in range(1,51):
    currentPattern.append(percentChange(prices[ar-75], prices[ar-(75-pt)]))
  for pt in range(1,26):
    currentPatternOutcome.append(percentChange(prices[ar-75], prices[ar-(25-pt)]))

  for i in range(0, len(listOf75Ar)): #comparing pattern with saved pattern list, i is list of stored arrays
    per = arPercentChange(listOf75Ar[i], currentPattern)
    if per> 85:

      perList.append(per) #for signal accuracy
      neededArOf50.append(listOf75Ar[i])
      neededArOf25.append(listOf25Ar[i])
      #print(f'{per}% for {ar}_{i}')
  if len(neededArOf50)>3:
    print(f'{sum(perList)/float(len(perList))}% signal')

    colors = ['blue', 'green', 'grey', 'cyan', 'magenta']
    # Plotting
    for idx, array in enumerate(neededArOf50):
        plt.plot(range(1, 51), array[:50], color=colors[idx % len(colors)])
    for idx, array in enumerate(neededArOf25):    
        plt.plot(range(61,86), array[:50], color=colors[idx % len(colors)])
    plt.plot(range(1, 51), currentPattern, color='red', linewidth=3)
    plt.plot(range(61, 86), currentPatternOutcome, color='red', linewidth=3)

    plt.xlabel('Index')
    plt.ylabel(f'{ar}||{len(perList)}')
    plt.title('Multiple Lines Plot')
    plt.legend()
    plt.show()


