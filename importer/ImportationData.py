
import pandas as pd
import krakenex
import pprint
from requests.exceptions import HTTPError
import datetime
import calendar
import time

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
   pprint.pprint(response['result']['XXBTZEUR'][1])
except HTTPError as e:
    print(str(e))


data1.append(pd.DataFrame.from_dict(response['result']['XXBTZEUR']))
#data2.append(pd.DataFrame(data=titre))
#data3=set().union(data2,data1)
trades = pd.DataFrame
trades = pd.concat(data1, axis = 0)
trades.rename(columns={0: 'price', 1: 'time', 2: 'buy/sell', 3: 'market/limit', 4: 'miscellaneous'}, inplace=True)
trades.to_csv('data.csv',sep = ';')

