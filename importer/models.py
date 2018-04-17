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