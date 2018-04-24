from django.contrib import admin
from importer.models import Pair , TradeValue, Ask, Bid



class AskInline(admin.TabularInline):
    model = Ask
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 10
        queryset = super(AskInline, self).get_queryset(request)
        ids = queryset.order_by('-id').values('pk')[:LIMIT_SEARCH]
        qs = Ask.objects.filter(pk__in=ids).order_by('-id')
        return qs

class BidInline(admin.TabularInline):
    model = Bid
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 10
        queryset = super(BidInline, self).get_queryset(request)
        ids = queryset.order_by('-id').values('pk')[:LIMIT_SEARCH]
        qs = Bid.objects.filter(pk__in=ids).order_by('-id')
        return qs

class TradeValueInline(admin.TabularInline):
    model = TradeValue
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 50
        queryset = super(TradeValueInline, self).get_queryset(request)
        ids = queryset.order_by('-id').values('pk')[:LIMIT_SEARCH]
        qs = TradeValue.objects.filter(pk__in=ids).order_by('-id')
        return qs

class PairAdmin(admin.ModelAdmin):
    inlines = [
        AskInline,
        BidInline,
        TradeValueInline,
    ]


# Register your models here.
admin.site.register(Pair, PairAdmin)
