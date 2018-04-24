from django.contrib import admin
from importer.models import Pair , TradeValue, Ask, Bid



class AskInline(admin.TabularInline):
    model = Ask

class BidInline(admin.TabularInline):
    model = Bid

class ValeurTradeInline(admin.TabularInline):
    model = TradeValue

class PairAdmin(admin.ModelAdmin):
    inlines = [
        AskInline,
        BidInline,
        ValeurTradeInline,
    ]

# Register your models here.
admin.site.register(Pair, PairAdmin)
