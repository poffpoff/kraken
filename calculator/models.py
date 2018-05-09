import pprint

from django.db import models
# Create your models here.
from django.db.models import Max, FloatField
from django.template.loader import render_to_string

from importer.models import Pair, TradeValue
from scipy import signal


class ResultValueTime(models.Model):
    value = models.FloatField(blank=True)
    time = models.FloatField(blank=True)

class Calcul(models.Model):
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default='0')
    name = models.CharField(max_length=200, default='')
    enabled = models.BooleanField(default=True)

    def launch_calculation(self):
        pprint.pprint("need to have launch_calculation method")

    def __str__(self):
        return self.name


class MovingAverageOnTradeValue(Calcul):
    delta = models.IntegerField(default=500)


    def chart(self):
        tradeValue_set = TradeValue.objects.filter(pair = self.pair)
        data_list = []
        for tradeValue in tradeValue_set :
            temp = [int(tradeValue.time*1000), tradeValue.price]
            data_list.append(temp)

        result_set = ResultMovingAverageOnTradeValue.objects.filter(moving_average_on_trade_value = self)
        moving_average_data_list = []

        for result in result_set :
            if (result.value != 0) :
                temp = [int(result.time*1000), result.value]
                moving_average_data_list.append(temp)

        data_dict = { 'data' : data_list,
                      'title' : 'Trade Price ' + self.name,
                      'currency': self.name[-3:],
                      'name' : self.name,
                      'moving_average_data' : moving_average_data_list,
                      }
        return render_to_string('admin/importer/pair/stock_chart.html', data_dict )

    def launch_calculation(self):
        # get the las trade values since the last data save into the db
        time = ResultMovingAverageOnTradeValue.objects.filter(moving_average_on_trade_value=self).aggregate(Max('time', output_field=FloatField()))

        if (time['time__max']):
            pprint.pprint(time['time__max'])
            to_start = TradeValue.objects.filter(pair = self.pair, time = time['time__max'])[0]
            trade_value_set = TradeValue.objects.filter(pair = self.pair, id__gte = to_start.id - self.delta)
        else:
            trade_value_set = TradeValue.objects.filter(pair = self.pair)

        pprint.pprint(trade_value_set)

        if (self.delta):
            index = self.delta
            for trade_value in trade_value_set[self.delta:]:

                time = trade_value.time
                value = trade_value.price

                trade_value_set_part = trade_value_set[index+1-self.delta:index]

                for trade_value_part in trade_value_set_part:
                    value = value + trade_value_part.price

                value = value / self.delta
                if(ResultMovingAverageOnTradeValue.objects.filter(moving_average_on_trade_value=self , time = time)):
                    pprint.pprint("moving avegare already exist")
                else:
                    new_result = ResultMovingAverageOnTradeValue.objects.create(moving_average_on_trade_value=self,
                                                          value=value,
                                                          time=time
                                                                                )

                    pprint.pprint(new_result.value)
                    pprint.pprint(new_result.time)
                    new_result.save()
                    index = index + 1




class LowPassOnTradeValue(Calcul):
    fc = models.IntegerField(default=500)


    def chart(self):
        tradeValue_set = TradeValue.objects.filter(pair = self.pair)
        data_list = []
        for tradeValue in tradeValue_set :
            temp = [int(tradeValue.time*1000), tradeValue.price]
            data_list.append(temp)

        result_set = ResultLowPassOnTradeValue.objects.filter(low_pass_on_trade_value = self)
        low_pass_data_list = []

        for result in result_set :
            temp = [int(result.time*1000), result.value]
            low_pass_data_list.append(temp)

        data_dict = { 'data' : data_list,
                      'title' : 'Trade Price ' + self.name,
                      'currency': self.name[-3:],
                      'name' : self.name,
                      'low_pass_data' : low_pass_data_list,
                      }
        return render_to_string('admin/importer/pair/stock_chart.html', data_dict )

    def launch_calculation(self):
        delta = 100
        if (self.fc):
            # # get the las trade values since the last data save into the db
            time = ResultLowPassOnTradeValue.objects.filter(low_pass_on_trade_value=self).aggregate(Max('time', output_field=FloatField()))

            if (time['time__max']):
                pprint.pprint(time['time__max'])
                to_start = TradeValue.objects.filter(pair = self.pair, time=time['time__max'])[0]
                trade_value_set = TradeValue.objects.filter(pair = self.pair, id__gte=to_start.id - delta)
            else:
                trade_value_set = TradeValue.objects.filter(pair = self.pair)

            pprint.pprint(trade_value_set)
            pprint.pprint(trade_value_set)


            win = signal.hann(self.fc)


            value_list = []
            time_list = []


            for trade_value in trade_value_set:
                time = trade_value.time
                value = trade_value.price
                pprint.pprint(time)
                pprint.pprint(value)
                value_list.append(value)
                time_list.append(time)

            pprint.pprint('len(value_list)')
            pprint.pprint(len(value_list))
            pprint.pprint(len(win))
            pprint.pprint("win")
            pprint.pprint(win)
            filtered_set = signal.convolve(value_list, win, mode='same') / sum(win)
            pprint.pprint('filtered_set')
            pprint.pprint(filtered_set)

            index = delta
            pprint.pprint('len(filtered_set)')
            pprint.pprint(len(filtered_set))
            for filtered in filtered_set[delta:len(filtered_set)-delta]:

                time = time_list[index]
                value = filtered
                pprint.pprint(time)
                pprint.pprint(value)

                if(ResultLowPassOnTradeValue.objects.filter(low_pass_on_trade_value=self , time = time)):
                    pprint.pprint("low pass already exist")
                else:
                    new_result = ResultLowPassOnTradeValue.objects.create(low_pass_on_trade_value=self,
                                                          value=value,
                                                          time=time
                                                                                )

                    pprint.pprint(new_result.value)
                    pprint.pprint(new_result.time)
                    new_result.save()
                index = index + 1

class ResultLowPassOnTradeValue(ResultValueTime):
    low_pass_on_trade_value = models.ForeignKey(LowPassOnTradeValue, on_delete=models.CASCADE, default='0')


class ResultMovingAverageOnTradeValue(ResultValueTime):
    moving_average_on_trade_value = models.ForeignKey(MovingAverageOnTradeValue, on_delete=models.CASCADE, default='0')