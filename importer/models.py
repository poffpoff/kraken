from django.db import models

# Create your models here.

class Pair(models.Model):
    name = models.CharField(max_length=200, default='Error')

    def __str__(self):
        return self.name



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



