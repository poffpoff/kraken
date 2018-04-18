from django.db import models

# Create your models here.

class Pair(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Value(models.Model):
    name = models.CharField(max_length=200)
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Data(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE)
    data = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return self.name

class ValeurTrade(models.Model):
    name = models.ForeignKey(Pair, on_delete=models.CASCADE)
    id_echange = models.FloatField()
    price = models.FloatField()
    bs = models.FloatField()
    ml = models.FloatField()
    misce = models.FloatField()
    time = models.DateTimeField()

