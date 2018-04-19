from django.contrib import admin
from importer.models import Pair, Data, Value, ValeurTrade,LastTrade,testtest

class ValueInline(admin.TabularInline):
    model = Value

class DataInline(admin.TabularInline):
    model = Data


class ValueAdmin(admin.ModelAdmin):
    inlines = [
        DataInline,
    ]

# Register your models here.
admin.site.register(Value, ValueAdmin)
admin.site.register(Pair)
admin.site.register(ValeurTrade)
admin.site.register(LastTrade)
admin.site.register(testtest)