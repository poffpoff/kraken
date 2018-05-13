import datetime
import pprint
import time

from django.db import models

# Create your models here.
from django.db.models import Sum, Max, FloatField
from django.template.loader import render_to_string
from django.utils import timezone
from requests import HTTPError
import krakenex
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class Pair(models.Model):
    BCHEUR = 'BCHEUR'
    BCHUSD = 'BCHUSD'
    BCHXBT = 'BCHXBT'
    DASHEUR = 'DASHEUR'
    DASHUSD = 'DASHUSD'
    DASHXBT = 'DASHXBT'
    EOSETH = 'EOSETH'
    EOSEUR = 'EOSEUR'
    EOSUSD = 'EOSUSD'
    EOSXBT = 'EOSXBT'
    GNOETH = 'GNOETH'
    GNOEUR = 'GNOEUR'
    GNOUSD = 'GNOUSD'
    GNOXBT = 'GNOXBT'
    USDTUSD = 'USDTUSD'
    ETCETH = 'ETCETH'
    ETCXBT = 'ETCXBT'
    ETCEUR = 'ETCEUR'
    ETCUSD = 'ETCUSD'
    ETHXBT = 'ETHXBT'
    ETHCAD = 'ETHCAD'
    ETHEUR = 'ETHEUR'
    ETHGBP = 'ETHGBP'
    ETHJPY = 'ETHJPY'
    ETHUSD = 'ETHUSD'
    ICNETH = 'ICNETH'
    ICNXBT = 'ICNXBT'
    LTCXBT = 'LTCXBT'
    LTCEUR = 'LTCEUR'
    LTCUSD = 'LTCUSD'
    MLNETH = 'MLNETH'
    MLNXBT = 'MLNXBT'
    REPETH = 'REPETH'
    REPXBT = 'REPXBT'
    REPEUR = 'REPEUR'
    REPUSD = 'REPUSD'
    XBTCAD = 'XBTCAD'
    XBTEUR = 'XBTEUR'
    XBTGBP = 'XBTGBP'
    XBTJPY = 'XBTJPY'
    XBTUSD = 'XBTUSD'
    XDGXBT = 'XDGXBT'
    XLMXBT = 'XLMXBT'
    XLMEUR = 'XLMEUR'
    XLMUSD = 'XLMUSD'
    XMRXBT = 'XMRXBT'
    XMREUR = 'XMREUR'
    XMRUSD = 'XMRUSD'
    XRPXBT = 'XRPXBT'
    XRPCAD = 'XRPCAD'
    XRPEUR = 'XRPEUR'
    XRPJPY = 'XRPJPY'
    XRPUSD = 'XRPUSD'
    ZECXBT = 'ZECXBT'
    ZECEUR = 'ZECEUR'
    ZECJPY = 'ZECJPY'
    ZECUSD = 'ZECUSD'
    PAIR_CHOICES = (
        (BCHEUR, 'BCHEUR'),
        (BCHUSD, 'BCHUSD'),
        (BCHXBT, 'BCHXBT'),
        (DASHEUR, 'DASHEUR'),
        (DASHUSD, 'DASHUSD'),
        (DASHXBT, 'DASHXBT'),
        (EOSETH, 'EOSETH'),
        (EOSEUR, 'EOSEUR'),
        (EOSUSD, 'EOSUSD'),
        (EOSXBT, 'EOSXBT'),
        (GNOETH, 'GNOETH'),
        (GNOEUR, 'GNOEUR'),
        (GNOUSD, 'GNOUSD'),
        (GNOXBT, 'GNOXBT'),
        (USDTUSD, 'USDTUSD'),
        (ETCETH, 'ETCETH'),
        (ETCXBT, 'ETCXBT'),
        (ETCEUR, 'ETCEUR'),
        (ETCUSD, 'ETCUSD'),
        (ETHXBT, 'ETHXBT'),
        (ETHCAD, 'ETHCAD'),
        (ETHEUR, 'ETHEUR'),
        (ETHGBP, 'ETHGBP'),
        (ETHJPY, 'ETHJPY'),
        (ETHUSD, 'ETHUSD'),
        (ICNETH, 'ICNETH'),
        (ICNXBT, 'ICNXBT'),
        (LTCXBT, 'LTCXBT'),
        (LTCEUR, 'LTCEUR'),
        (LTCUSD, 'LTCUSD'),
        (MLNETH, 'MLNETH'),
        (REPETH, 'REPETH'),
        (REPXBT, 'REPXBT'),
        (REPEUR, 'REPEUR'),
        (REPUSD, 'REPUSD'),
        (XBTCAD, 'XBTCAD'),
        (XBTEUR, 'XBTEUR'),
        (XBTGBP, 'XBTGBP'),
        (XBTJPY, 'XBTJPY'),
        (XBTUSD, 'XBTUSD'),
        (XDGXBT, 'XDGXBT'),
        (XLMXBT, 'XLMXBT'),
        (XLMEUR, 'XLMEUR'),
        (XLMUSD, 'XLMUSD'),
        (XMRXBT, 'XMRXBT'),
        (XMREUR, 'XMREUR'),
        (XMRUSD, 'XMRUSD'),
        (XRPXBT, 'XRPXBT'),
        (XRPCAD, 'XRPCAD'),
        (XRPEUR, 'XRPEUR'),
        (XRPJPY, 'XRPJPY'),
        (XRPUSD, 'XRPUSD'),
        (ZECXBT, 'ZECXBT'),
        (ZECEUR, 'ZECEUR'),
        (ZECJPY, 'ZECJPY'),
        (ZECUSD, 'ZECUSD'),
    )


    name = models.CharField(max_length=8, choices=PAIR_CHOICES, default=BCHEUR)
    enabled_auto_import = models.BooleanField(default=True)
    since = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return self.name

    def trade_chart(self):
        tradeValue_set = TradeValue.objects.filter(pair = self).order_by('time')
        data_list = []
        for tradeValue in tradeValue_set :
            temp = [int(tradeValue.time*1000), tradeValue.price]
            data_list.append(temp)
        data_dict = {
                      'data_list' : data_list,
                      'title' : 'Trade Price ' + self.name,
                      'currency': self.name[-3:]
                      }
        return render_to_string('admin/importer/pair/stock_chart.html', data_dict )

    def depth_chart(self):
        ask_set = Ask.objects.filter(pair = self)
        bid_set = Bid.objects.filter(pair = self)
        ask_list = []
        bid_list = []
        for ask in ask_set :
            sum_volum = Ask.objects.filter(price__lte = ask.price).aggregate(Sum('volume'))
            temp = [ask.price, sum_volum['volume__sum']]
            ask_list.append(temp)

        for bid in bid_set :
            sum_volum = Bid.objects.filter(price__gte = bid.price).aggregate(Sum('volume'))
            temp = [bid.price, sum_volum['volume__sum']]
            bid_list.append(temp)

        data_dict = { 'ask_data' : ask_list,
                      'ask_name' : "Ask " + self.name,
                      'bid_data': bid_list,
                      'bid_name': "Bid " + self.name,
                      'currency': self.name[-3:],
                      'title': 'Depth ' + self.name
                      }
        return render_to_string('admin/importer/pair/depth_chart.html', data_dict )


    def launch_import_trade_value(self, since=0):
        t0 = time.time()
        k = krakenex.API()
        to_time = datetime.datetime.now()
        to_id = int(to_time.timestamp() * 1000000000)
        if(since is 0):
            since = TradeValue.objects.filter(pair_id=self.id).aggregate(Max('time', output_field=FloatField()))['time__max']
            logger.info("For pair " + self.name + " with id " + str(self.id) + " - Get the time of the last trade saved :" + str(since))


        if(since is not None):
            since_date = datetime.datetime.fromtimestamp(int(since)).strftime('%Y-%m-%d %H:%M:%S')
            since_id = int(since * 1000000000)
            logger.info("Start importing trade values for pair " + self.name + " with id " + str(self.id) + " since " + str(since_date) + " to " + str(to_time))
        else:
            logger.info("Start importing the last 1000 trade values for pair " + self.name + " with id " + str(self.id))
            since_id = 0


        nbr_of_new_import = 0
        while True:
            nbr_of_new_import_in_the_loop = 0
            try:
                if (since_id is not 0):
                    response = k.query_public('Trades', {'pair': self.name, 'since': since_id})
                else:
                    response = k.query_public('Trades', {'pair': self.name})
            except HTTPError as e:
                logger.error(str(e))

            # trick to get the right name of the set
            i = 0
            title_ok = ''
            try:
                response['result']
            except:
                continue

            for title in response['result']:
                if (i == 0):
                    title_ok = title
                i = i + 1

            # save data into database only if the value with th same time doen't exist already
            for trade in response['result'][title_ok]:
                nbr_of_new_import_in_the_loop = nbr_of_new_import_in_the_loop + 1
                if (TradeValue.objects.filter(pair_id=self.id, time=trade[2])):
                    logger.info("For pair " + self.name + " with id " + str(self.id) + " - Trade " + str(trade) + " already exist in database")
                else:
                    new_trade = TradeValue.objects.create(pair=self,
                                                          price=trade[0],
                                                          volume=trade[1],
                                                          time=trade[2],
                                                          bs=trade[3],
                                                          ml=trade[4],
                                                          misce=trade[5])
                    new_trade.save()
                    logger.info("For pair " + self.name + " with id " + str(self.id) + " - Trade " + str(trade) + " saved into database")



            nbr_of_new_import = nbr_of_new_import + nbr_of_new_import_in_the_loop
            last_id = int(response['result']['last'])
            if(last_id > to_id):
                break
            else:
                if(nbr_of_new_import_in_the_loop is not 0):
                    since_id = last_id
                else:
                    break

        k.close()
        t1 = time.time()
        duration = t1 - t0
        if(nbr_of_new_import is not 0):
            average = duration / nbr_of_new_import
            logger.info("Summary : " + str(nbr_of_new_import) + " of new trade value in " + str(duration) + " seconds " + ", Average : " + str(average) + " seconds per trade value")
        else:
            logger.info("Summary : No new trade values")
        logger.info("End importing trade values for pair " + self.name + " with id " + str(self.id))


    def launch_import_book_order(self):
        t0 = time.time()
        logger.info("Start importing book orders for pair " + self.name + " with id " + str(self.id))

        k = krakenex.API()
        try:
            response = k.query_public('Depth', {'pair': self.name, 'count': 250})
        except HTTPError as e:
            print(str(e))

        # trick to get the right name of the set
        i = 0
        title_ok = ''
        for title in response['result']:
            if (i == 0):
                title_ok = title
            i = i + 1

        Ask.objects.all().delete()
        Bid.objects.all().delete()

        nbr_of_new_bid_import = 0
        nbr_of_new_ask_import = 0

        for ask in response['result'][title_ok]['asks']:
            nbr_of_new_ask_import = nbr_of_new_ask_import +1
            if (Ask.objects.filter(pair=self, timestamp=ask[2])):
                logger.info("For pair " + self.name + " with id " + str(self.id) + " - Ask " + str(ask) + " already exist in database")
            else:
                new_ask = Ask.objects.create(pair=self,
                                             price=ask[0],
                                             volume=ask[1],
                                             timestamp=ask[2])
                new_ask.save()
                logger.info("For pair " + self.name + " with id " + str(self.id) + " - Ask " + str(ask) + " saved into database")


        for bid in response['result'][title_ok]['bids']:
            nbr_of_new_bid_import = nbr_of_new_bid_import +1
            if (Bid.objects.filter(pair_id=self.id, timestamp=bid[2])):
                logger.info("For pair " + self.name + " with id " + str(self.id) + " - Bid " + str(bid) + " already exist in database")
            else:
                new_bid = Bid.objects.create(pair=self,
                                             price=bid[0],
                                             volume=bid[1],
                                             timestamp=bid[2])
                new_bid.save()
                logger.info("For pair " + self.name + " with id " + str(self.id) + " - Bid " + str(bid) + " saved into database")

        k.close()
        t1 = time.time()
        duration = t1 - t0
        average = duration / ( nbr_of_new_ask_import + nbr_of_new_bid_import)
        logger.info("Summary : " + str(nbr_of_new_ask_import) + " of new ask and " +str(nbr_of_new_bid_import) + " of new bid in " + str(duration) + " seconds " + ", Average : " + str(average) + " seconds per order")
        logger.info("End importing trade values for pair " + self.name + " with id " + str(self.id))

class TradeValue(models.Model):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')
    price = models.FloatField(blank=True)
    volume = models.FloatField(blank=True)
    time = models.FloatField(blank=True)
    bs = models.CharField(max_length=200, default='', blank=True)
    ml = models.CharField(max_length=200, default='', blank=True)
    misce = models.CharField(max_length=200, default='', blank=True)



class OrderValue(models.Model):
    price = models.FloatField(blank=True)
    volume = models.FloatField(blank=True)
    timestamp = models.FloatField(blank=True)

class Ask(OrderValue):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')


class Bid(OrderValue):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')



