# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from importer.models import Pair


from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def import_all_trade_values():
    pair_set = Pair.objects.all()
    for pair in pair_set:
        if (pair.enabled_auto_import) :
            pair.launch_import_trade_value()


@shared_task
def import_all_order_books():
    pair_set = Pair.objects.all()
    for pair in pair_set:
        if (pair.enabled_auto_import) :
            pair.launch_import_book_order()
