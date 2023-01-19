""""
The goal of this model is to fine tune a bull put spread, the strike price of the bull spread are larely left up to the trader but I wanted to create a model which 
according to the past historical data tells us which delta values for the corresponding strike prices will maximise the profits. This is done by first exporting the 
historical data and then cleaning it by removing columms which will not be used. Then we select 
"""
import pickle
import pandas as pd
from yahoo_fin.stock_info import get_data
from concurrent.futures import ThreadPoolExecutor

#Reading the data provided by ORATS
data = pd.read_csv("ORATS_SMV_Strikes_20200420.csv")

#Sorting the data with only the useful columns and creating a new column for put deltas
new = pd.DataFrame().assign(Ticker=data['ticker'], Stock_Price=data['stkPx'], Expiration_date=data['expirDate'], strike=data['strike'], call_price=data['cValue'], put_price=data['pValue'], IV=data['smoothSmvVol'], delta_c=data['delta'], delta_p=(1-data['delta']))

#For the inital process only taking contracts for a single expiration cycle 
new_filter = new.loc[(new['Expiration_date'] == "5/15/2020")]

#Here we have created a new database (df1) where each row represenets 1 Ticker and has all the different call and put values as different columns
indiv = new_filter.groupby(['Ticker', 'Stock_Price', 'Expiration_date']).cumcount()
df1 = new_filter.set_index(['Ticker', 'Stock_Price', 'Expiration_date', indiv]).unstack().sort_index(level=1, axis=1)
df1.columns = [f'{x}{y}' for x, y in df1.columns]
df1 = df1.reset_index()

#Adding a new column to the dataset which has the closing stock price of each of the stocks, this will be a day before the expiration date as we want to minimize 
#pin risk. This column will be used to calcualte our theoretical profit.

#The code does not run fast enough if we run it sequentially because it is making ~4000 HTTP requests sequentially, so we will use the 
#parallel programming to make it run faster using the concurrent library.
stock_name = df1['Ticker'].tolist()
price_dict = {}

def put_info(ticker):
    try:
        price_dict[ticker] = get_data(ticker, start_date="05/14/2020", end_date="05/15/2020")
        print(ticker)
    except:
        price_dict[ticker] = 'not found'
        print("error")

def populate_file(file_name):
    with ThreadPoolExecutor() as executor:
        [executor.submit(put_info, ticker) for ticker in stock_name]

    open_file = open(file_name, 'wb')
    pickle.dump(price_dict, open_file)
    open_file.close()
    return price_dict

try:
    file = open('stock_info.txt', 'rb')
    price_dict = pickle.load(file)
except:
    file = open('stock_info.txt', "x")
    price_dict = populate_file("stock_info.txt")

#Now that we have the stock prices a day before the expiration we can add it in as a new column to our existing datafram
#df1, note the API was not able to retrieve prices for some of the tickers, we will delete those rows for now
print(price_dict)

