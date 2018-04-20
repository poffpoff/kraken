import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kraken.settings")
django.setup()

import pandas as pd
import krakenex
import pprint
from requests.exceptions import HTTPError
import datetime
import calendar
import sqlite3
import time
from importer.models import ValeurTrade

# takes date and returns nix time
def date_nix(str_date):
    return calendar.timegm(str_date.timetuple())

# takes nix time and returns date
def date_str(nix_time):
    return datetime.datetime.fromtimestamp(nix_time).strftime('%m, %d, %Y')

titre =  {'1': ["price"], '2': ["time"], '3':["buy/sell"], '4':["market/limit"], '5':["miscellaneous"]}
data1 = []
data2 = []
data3 = []

DataColonne1bdd = []
# return formatted TradesHistory request data
#def data(start, end, ofs):
#    req_data = {'type': 'all',
#                'trades': 'true',
#                'start': str(date_nix(start)),
#                'end': str(date_nix(end)),
#                'ofs': str(ofs)
#                }
#   return req_data

k = krakenex.API()

try:
   response = k.query_public('Trades', {'pair': 'XBTEUR', 'since': '1524059916390775696'})
   pprint.pprint(response['result']['last'])
except HTTPError as e:
    print(str(e))


data1.append(pd.DataFrame.from_dict(response['result']['XXBTZEUR']))
#data2.append(pd.DataFrame(data=titre))
#data3=set().union(data2,data1)
trades = pd.DataFrame
trades = pd.concat(data1, axis = 0)

trades.rename(columns={0: 'price', 1: 'Volume', 2: 'index' , 3: 'buy/sell', 4: 'market/limit', 5: 'miscellaneous'}, inplace=True)

pprint.pprint(trades)

trades.to_csv('data.csv',sep = ';')


last_trade = trades.tail(1)
pprint.pprint(last_trade)

price = last_trade['price']
volume = last_trade['Volume']
index = last_trade['index']
buy_sell = last_trade['buy/sell']
market_limit = last_trade['market/limit']
miscellaneous = last_trade['miscellaneous']

pprint.pprint(price)
pprint.pprint(volume)
pprint.pprint(index)
pprint.pprint(buy_sell)
pprint.pprint(market_limit)
pprint.pprint(miscellaneous)


new_trade = ValeurTrade.objects.create( name='XBTEUR' , numeroechange=volume , price = price , bs=buy_sell ,ml=market_limit , misce = miscellaneous , time = datetime.datetime.now())
new_trade.save()

#pprint.pprint(trades['price'])

# DataColonne1bdd = trades['price'].as_matrix()
# DataColonne2bdd = trades['Volume'].as_matrix()
# DataColonne3bdd = trades['buy/sell'].as_matrix()
# DataColonne4bdd = trades['market/limit'].as_matrix()
# DataColonne5bdd = trades['miscellaneous'].as_matrix()
#
# Tailleextraction = len(DataColonne1bdd)
# pprint.pprint(DataColonne1bdd[0])
# boucleBDD = 0
# DateActuelle = str(datetime.datetime.now())
#
# connexion = sqlite3.connect('C:/Users/bapti_000/PycharmProjects/kraken/db.sqlite3', timeout=30)
# cur =connexion.cursor()
#
#
# while boucleBDD <  1 :
#     Numeroplus = float(1524059916390775696 + boucleBDD)
#     cur.execute("INSERT INTO importer_testtest(name) Values ('TESTE2')")
#    # connexion.execute("INSERT INTO ValeurTrade (name, numeroechange, price,bs,ml,misce,time) VALUES ('XBTEUR', "+float(Numeroplus)+", "+float(DataColonne1bdd[boucleBDD])+", "+str(DataColonne4bdd[boucleBDD])+", "+str(DataColonne4bdd[boucleBDD])+", "+str(DataColonne5bdd[boucleBDD])+", "+DateActuelle+")")
# #    ValeurTrade(name="XBTEUR", numeroechange=, price=DataColonne1bdd[boucleBDD],bs=DataColonne3bdd[boucleBDD],ml=DataColonne4bdd[boucleBDD],misce=DataColonne5bdd[boucleBDD],time=DateActuelle ).save()
#     connexion.commit()
#     boucleBDD += 1
#
# datefozieoz = connexion.execute("select * from importer_testtest")
# connexion.close



