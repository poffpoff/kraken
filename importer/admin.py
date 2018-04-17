from django.contrib import admin
from importer.models import Pair, Data, Value

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