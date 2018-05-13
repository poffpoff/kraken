from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from importer.models import Pair , TradeValue, Ask, Bid

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AskInline(admin.TabularInline):
    model = Ask
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 10
        queryset = super(AskInline, self).get_queryset(request)
        ids = queryset.order_by('-timestamp').values('pk')[:LIMIT_SEARCH]
        qs = Ask.objects.filter(pk__in=ids).order_by('-timestamp')
        return qs

class BidInline(admin.TabularInline):
    model = Bid
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 10
        queryset = super(BidInline, self).get_queryset(request)
        ids = queryset.order_by('-timestamp').values('pk')[:LIMIT_SEARCH]
        qs = Bid.objects.filter(pk__in=ids).order_by('-timestamp')
        return qs

class TradeValueInline(admin.TabularInline):
    model = TradeValue
    max_num = 10

    def get_queryset(self, request):
        LIMIT_SEARCH = 50
        queryset = super(TradeValueInline, self).get_queryset(request)
        ids = queryset.order_by('-time').values('pk')[:LIMIT_SEARCH]
        qs = TradeValue.objects.filter(pk__in=ids).order_by('-time')
        return qs

class PairAdmin(admin.ModelAdmin):
    inlines = [
        AskInline,
        BidInline,
        TradeValueInline,
    ]

    list_display = (
        'name',
        'import_action',
    )

    readonly_fields = ('trade_chart','depth_chart', )


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<pair_id>.+)/import/$',
                self.admin_site.admin_view(self.process_import),
                name='import',
            ),
        ]
        return custom_urls + urls


    def import_action(self, obj):
        return format_html(
            '<a class="button" target="_blank" href="{}">Import</a>&nbsp;',
            reverse('admin:import', args=[obj.pk]),
        )
        import_action.short_description = 'Import'
        import_action.allow_tags = True


    def process_import(self, request, pair_id, *args, **kwargs):
        pair = Pair.objects.get(id = pair_id)
        logger.info("For pair " + pair.name + " with id " + str(pair.id) + " - Start manually import of trades value since " + str(pair.since) + " and book orders ")
        pair.launch_import_trade_value(pair.since.timestamp())
        pair.launch_import_book_order()
        self.message_user(request, 'Success')
        url = reverse(
            'admin:importer_pair_change',
            args=[pair.pk],
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

# Register your models here.
admin.site.register(Pair, PairAdmin)
