import pprint

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from calculator.models import MovingAverageOnTradeValue, ResultMovingAverageOnTradeValue, ResultLowPassOnTradeValue, LowPassOnTradeValue, ResultValueTime, CalculOnTradeValue


class ResultInline(admin.TabularInline):
    def get_model(self):
        return ResultValueTime

    def get_queryset(self, request):
        LIMIT_SEARCH = 50
        queryset = super(ResultInline, self).get_queryset(request)
        ids = queryset.order_by('-time').values('pk')[:LIMIT_SEARCH]
        qs = self.model.objects.filter(pk__in=ids).order_by('-time')
        return qs


class ResultMovingAverageOnTradeValueInLine(ResultInline):
    model = ResultMovingAverageOnTradeValue


class ResultLowPassOnTradeValueInLine(ResultInline):
    model = ResultLowPassOnTradeValue


class CalculAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'calcul_action',
    )

    readonly_fields = ('chart',)

    def get_model(self):
        return Calcul

    def get_model_name(self):
        return self.get_model()._meta.model_name

    def get_urls(self):
        urls = super().get_urls()
        name = self.get_model_name()
        custom_urls = [
            url(
                r'^(?P<calcul_id>.+)/calcul/$',
                self.admin_site.admin_view(self.process_calcul),
                name=name,
            ),
        ]
        return custom_urls + urls





    def calcul_action(self, obj):
        name = 'admin:' + self.get_model_name()

        return format_html(
            '<a class="button" target="_blank" href="{}">Calcul</a>&nbsp;',
            reverse(name , args=[obj.pk]),
        )
        calcul_action.short_description = 'Calcul'
        calcul_action.allow_tags = True


    def process_calcul(self, request, calcul_id, *args, **kwargs):
        calcul = self.get_model().objects.get(id = calcul_id)
        calcul.launch_calculation()
        self.message_user(request, 'Success')
        name = 'admin:calculator_' + self.get_model_name() + '_change'
        url = reverse(
            name,
            args=[calcul.pk],
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

class MovingAverageOnTradeValueAdmin(CalculAdmin):
    def get_model(self):
        return MovingAverageOnTradeValue

    inlines = [
        ResultMovingAverageOnTradeValueInLine,
    ]


class LowPassOnTradeValueAdmin(CalculAdmin):
    def get_model(self):
        return LowPassOnTradeValue

    inlines = [
        ResultLowPassOnTradeValueInLine,
    ]


# Register your models here.
admin.site.register(MovingAverageOnTradeValue, MovingAverageOnTradeValueAdmin)
admin.site.register(LowPassOnTradeValue, LowPassOnTradeValueAdmin)
