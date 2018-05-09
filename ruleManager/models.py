from django.db import models
from importer.models import Pair
from calculator.models import Calcul

# Create your models here.

class Rule(models.Model):
    name = models.CharField(default='', max_length=50)
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')
    enabled = models.BooleanField(default=True)


class RuleOn2Calculs(Rule):
    data_1 = models.ForeignKey(Calcul, on_delete=models.CASCADE, default='0')

    GT = 'GT'
    LT = 'LT'
    EQ = 'EQ'
    GTE = 'GT'
    LTE = 'LT'
    NONE = 'NONE'
    ACTION_CHOICES = (
        (GT, 'greater than'),
        (GTE, 'greater or equal than'),
        (LT, 'lower than'),
        (LTE, 'lower or equal than'),
        (NONE, 'None'),
    )

    action_choice = models.CharField(
        max_length=2,
        choices=ACTION_CHOICES,
        default='None',
    )




class Action(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    NONE = 'NONE'
    ACTION_CHOICES = (
        (BUY, 'Buy'),
        (SELL, 'Sell'),
        (NONE, 'None'),
    )

    action_choice = models.CharField(
        max_length=2,
        choices=ACTION_CHOICES,
        default='None',
    )

    price = models.FloatField
    volume = models.FloatField()

    data_2 = models.ForeignKey(Rule, on_delete=models.CASCADE, default='0')
