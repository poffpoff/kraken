from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from calculator.models import MovingAverageOnTradeValue, ResultMovingAverageOnTradeValue, ResultLowPassOnTradeValue, LowPassOnTradeValue


class ResultInline(admin.TabularInline):
    model = ResultMovingAverageOnTradeValue

    def get_queryset(self, request):
        LIMIT_SEARCH = 50
        queryset = super(ResultInline, self).get_queryset(request)
        ids = queryset.order_by('-time').values('pk')[:LIMIT_SEARCH]
        qs = ResultMovingAverageOnTradeValue.objects.filter(pk__in=ids).order_by('-time')
        return qs


class CalculAdmin(admin.ModelAdmin):
    inlines = [
        ResultInline,
    ]

    list_display = (
        'name',
        'calcul_action',
    )

    readonly_fields = ('chart',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<movingaverageontrade_id>.+)/calcul/$',
                self.admin_site.admin_view(self.process_calcul),
                name='calcul_2',
            ),
        ]
        return custom_urls + urls


    def calcul_action(self, obj):
        return format_html(
            '<a class="button" target="_blank" href="{}">Calcul</a>&nbsp;',
            reverse('admin:calcul_2', args=[obj.pk]),
        )
        calcul_action.short_description = 'Calcul'
        calcul_action.allow_tags = True


    def process_calcul(self, request, movingaverageontrade_id, *args, **kwargs):
        calcul = MovingAverageOnTradeValue.objects.get(id = movingaverageontrade_id)
        calcul.launch_calculation()
        self.message_user(request, 'Success')
        url = reverse(
            'admin:calculator_movingaverageontradevalue_change',
            args=[calcul.pk],
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

class LowPassResultInline(admin.TabularInline):
    model = ResultLowPassOnTradeValue

    def get_queryset(self, request):
        LIMIT_SEARCH = 50
        queryset = super(LowPassResultInline, self).get_queryset(request)
        ids = queryset.order_by('-time').values('pk')[:LIMIT_SEARCH]
        qs = ResultLowPassOnTradeValue.objects.filter(pk__in=ids).order_by('-time')
        return qs


class LowPassCalculAdmin(admin.ModelAdmin):
    inlines = [
        LowPassResultInline,
    ]

    readonly_fields = ('chart',)

    list_display = (
        'name',
        'calcul_action',
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<lowpassontradevalue_id>.+)/calcul/$',
                self.admin_site.admin_view(self.process_calcul),
                name='calcul',
            ),
        ]
        return custom_urls + urls


    def calcul_action(self, obj):
        return format_html(
            '<a class="button" target="_blank" href="{}">Calcul</a>&nbsp;',
            reverse('admin:calcul', args=[obj.pk]),
        )
        calcul_action.short_description = 'Calcul'
        calcul_action.allow_tags = True


    def process_calcul(self, request, lowpassontradevalue_id, *args, **kwargs):
        calcul = LowPassOnTradeValue.objects.get(id = lowpassontradevalue_id)
        calcul.launch_calculation()
        self.message_user(request, 'Success')
        url = reverse(
            'admin:calculator_lowpassontradevalue_change',
            args=[calcul.pk],
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

# Register your models here.
admin.site.register(MovingAverageOnTradeValue, CalculAdmin)
admin.site.register(LowPassOnTradeValue, LowPassCalculAdmin)
