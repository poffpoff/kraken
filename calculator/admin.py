from django.contrib import admin
from calculator.models import MovingAverageOnTradeValue, ResultMovingAverageOnTradeValue


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

    readonly_fields = ('chart',)



# Register your models here.
admin.site.register(MovingAverageOnTradeValue, CalculAdmin)
