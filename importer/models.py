
from django.db import models

# Create your models here.
from django.template.loader import render_to_string


class Pair(models.Model):
    name = models.CharField(max_length=200, default='Error')

    def __str__(self):
        return self.name

    def trade_value(self):
        tradeValue_set = TradeValue.objects.filter(pair = self)
        data_list = []
        for tradeValue in tradeValue_set :
            temp = [int(tradeValue.time*1000), tradeValue.price]
            data_list.append(temp)
        data_dict = { 'data' : data_list,
                      'title' : 'Trade Price ' + self.name,
                      'name' : self.name}
        return render_to_string('admin/importer/pair/stock_chart.html', data_dict )


class TradeValue(models.Model):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')
    price = models.FloatField()
    volume = models.FloatField()
    time = models.FloatField()
    bs = models.CharField(max_length=200, default='')
    ml = models.CharField(max_length=200, default='')
    misce = models.CharField(max_length=200, default='')



class OrderValue(models.Model):
    price = models.FloatField()
    volume = models.FloatField()
    timestamp = models.FloatField()

class Ask(OrderValue):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')


class Bid(OrderValue):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')



