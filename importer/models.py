from django.db import models

# Create your models here.

class Pair(models.Model):
    name = models.CharField(max_length=200, default='Error')

    def __str__(self):
        return self.name


class Value(models.Model):
    name = models.CharField(max_length=200, default='Error')
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='Error')

    def __str__(self):
        return self.name

class ValeurTrade(models.Model):
    name = models.CharField(max_length=200, default='Error')
    numeroechange = models.FloatField()
    price = models.FloatField()
    bs = models.CharField(max_length=200, default='Error')
    ml = models.CharField(max_length=200, default='Error')
    misce = models.CharField(max_length=200, default='Error')
    time = models.DateTimeField()

    def __str__(self):
        return self.numeroechange

class LastTrade(models.Model):
    name = models.CharField(max_length=200, default='Error')
    valueLast = models.FloatField()

    def __str__(self):
        return self.name

class Data(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE, default=1)
    data = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return self.name

class testtest(models.Model):
    name = models.CharField(max_length=200, default='Error')


