# Create your tasks here
from __future__ import absolute_import, unicode_literals

import pprint

from celery import shared_task
from calculator.models import MovingAverageOnTradeValue , LowPassOnTradeValue


from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def launch_all_moving_average():
    pprint.pprint("launch_all_moving_average")
    calcul_set = MovingAverageOnTradeValue.objects.all()
    for calcul in calcul_set:
        if (calcul.enabled) :
            calcul.launch_calculation()



@shared_task
def launch_all_low_pass():
    pprint.pprint("launch_all_low_pass")
    calcul_set = LowPassOnTradeValue.objects.all()
    for calcul in calcul_set:
        if (calcul.enabled) :
            calcul.launch_calculation()