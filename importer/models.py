from django.db import models

# Create your models here.

class Pair(models.Model):
    name = models.CharField(max_length=200)
