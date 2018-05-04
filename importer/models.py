
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.template.loader import render_to_string


class Pair(models.Model):
    name = models.CharField(max_length=200, default='Error')
    enable_import = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    def trade_chart(self):
        tradeValue_set = TradeValue.objects.filter(pair = self)
        data_list = []
        for tradeValue in tradeValue_set :
            temp = [int(tradeValue.time*1000), tradeValue.price]
            data_list.append(temp)
        data_dict = { 'data' : data_list,
                      'title' : 'Trade Price ' + self.name,
                      'name' : self.name}
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
                      'title': 'Depth ' + self.name
                      }
        return render_to_string('admin/importer/pair/depth_chart.html', data_dict )


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



