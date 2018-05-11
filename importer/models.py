import datetime
import pprint

from django.db import models

# Create your models here.
from django.db.models import Sum, Max, FloatField
from django.template.loader import render_to_string
from django.utils import timezone
from requests import HTTPError


import krakenex


class Pair(models.Model):
    name = models.CharField(max_length=200, default='')
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
        k = krakenex.API()
        to_id = int(datetime.datetime.now().timestamp() * 1000000000)

        if(since is not 0):
            since_id = int(since * 1000000000)
        else:
            since_id = 0
            pprint.pprint('since is  0')
            # get the las trade values since the last data save into the db
            since_max = TradeValue.objects.filter(pair_id=self.id).aggregate(Max('time', output_field=FloatField()))
            if(since_max['time__max']) :
                since_id = int(since * 1000000000)

        while True:
            try:
                if (since_id is not 0):
                    response = k.query_public('Trades', {'pair': self.name, 'since': since_id})
                else:
                    response = k.query_public('Trades', {'pair': self.name})
            except HTTPError as e:
                print(str(e))

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
                    pprint.pprint(title)
                i = i + 1

            # save data into database only if the value with th same time doen't exist already
            for trade in response['result'][title_ok]:
                if (TradeValue.objects.filter(pair_id=self.id, time=trade[2])):
                    pprint.pprint(self.name)
                    pprint.pprint("trade already exist")
                else:
                    pprint.pprint(self.name)
                    pprint.pprint('trade')
                    pprint.pprint(trade)
                    new_trade = TradeValue.objects.create(pair=self,
                                                          price=trade[0],
                                                          volume=trade[1],
                                                          time=trade[2],
                                                          bs=trade[3],
                                                          ml=trade[4],
                                                          misce=trade[5])
                    new_trade.save()




            last_id = int(response['result']['last'])
            if(last_id > to_id):
                break
            else:
                pprint.pprint('last_id')
                pprint.pprint(last_id)
                pprint.pprint('to_id')
                pprint.pprint(to_id)
                since_id = last_id

        k.close()


    def launch_import_book_order(self):
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
                pprint.pprint(title)
            i = i + 1

        Ask.objects.all().delete()
        Bid.objects.all().delete()

        for ask in response['result'][title_ok]['asks']:
            if (Ask.objects.filter(pair=self, timestamp=ask[2])):
                pprint.pprint(self.name)
                pprint.pprint("ask already exist")
            else:
                pprint.pprint(self.name)
                pprint.pprint('ask')
                pprint.pprint(ask)
                new_ask = Ask.objects.create(pair=self,
                                             price=ask[0],
                                             volume=ask[1],
                                             timestamp=ask[2])
                new_ask.save()

        for bid in response['result'][title_ok]['bids']:
            if (Bid.objects.filter(pair_id=self.id, timestamp=bid[2])):
                pprint.pprint(self.name)
                pprint.pprint("bid already exist")
            else:
                pprint.pprint(self.name)
                pprint.pprint('bid')
                pprint.pprint(bid)
                new_bid = Bid.objects.create(pair=self,
                                             price=bid[0],
                                             volume=bid[1],
                                             timestamp=bid[2])
                new_bid.save()

        k.close()


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



