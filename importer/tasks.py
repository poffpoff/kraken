# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import krakenex
import pprint
from requests.exceptions import HTTPError
from importer.models import TradeValue, Pair, Bid, Ask
from django.db.models import Max
from django.db.models import FloatField

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def import_all_trade_values():
    pair_set = Pair.objects.all()
    k = krakenex.API()
    # get the las trade values since the last data save into the db
    for pair in pair_set:
        try:
            since = TradeValue.objects.filter(pair_id=pair.id).aggregate(Max('time', output_field=FloatField()))
            if (since['time__max']) :
                since_id = int(since['time__max'] * 1000000000)
                pprint.pprint(since_id)
                response = k.query_public('Trades', {'pair': pair.name, 'since' :  since_id})
                pprint.pprint(response['result']['last'])
            else:
                response = k.query_public('Trades', {'pair': pair.name})
        except HTTPError as e:
            print(str(e))

        # trick to get the right name of the set
        i = 0
        title_ok = ''
        for title in response['result']:
            if (i==0):
                title_ok = title
                pprint.pprint(title)
            i=i+1

        # save data into database only if the value with th same time doen't exist already
        for trade in response['result'][title_ok]:
            if(TradeValue.objects.filter(time = trade[2])):
                pprint.pprint("trade already exist")
            else:
                pprint.pprint(trade)
                new_trade = TradeValue.objects.create(pair = pair,
                                                      price=trade[0],
                                                      volume=trade[1],
                                                      time=trade[2],
                                                      bs=trade[3],
                                                      ml=trade[4],
                                                      misce=trade[5])
                new_trade.save()


@shared_task
def import_all_order_books():
    pair_set = Pair.objects.all()
    k = krakenex.API()
    for pair in pair_set:
        try:
            response = k.query_public('Depth', {'pair': pair.name})
        except HTTPError as e:
            print(str(e))

        # trick to get the right name of the set
        i = 0
        title_ok = ''
        for title in response['result']:
            if (i==0):
                title_ok = title
                pprint.pprint(title)
            i=i+1

        for ask in response['result'][title_ok]['asks']:
            if(Ask.objects.filter(timestamp = ask[2])):
                pprint.pprint("ask already exist")
            else:
                pprint.pprint(ask)
                new_ask = Ask.objects.create(pair = pair,
                                                  price=ask[0],
                                                  volume=ask[1],
                                                  timestamp=ask[2])
                new_ask.save()

        for bid in response['result'][title_ok]['bids']:
            if(Bid.objects.filter(timestamp = bid[2])):
                pprint.pprint("bid already exist")
            else:
                pprint.pprint(bid)
                new_bid = Bid.objects.create(pair = pair,
                                                  price=bid[0],
                                                  volume=bid[1],
                                                  timestamp=bid[2])
                new_bid.save()