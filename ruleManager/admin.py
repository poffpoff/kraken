from django.contrib import admin
from django import forms

from ruleManager.models import Rule
# Register your models here.


#
# class MyForm(forms.ModelForm):
#     ACTION_CHOICES = (
#         ('GT', 'greater than'),
#         ('GTE', 'greater or equal than'),
#         ('LT', 'lower than'),
#         ('LTE', 'lower or equal than'),
#         ('NONE', 'None'),
#     )
#
#     action_choice = forms.CharField(max_length=255, choices=ACTION_CHOICES, default=None)
#
#     class Meta:
#         model = Rule
#         fields = ('action_choice',)
#
#
# class MyRuleAdmin(admin.ModelAdmin):
#     fields = ('action_choice',)
#     list_display = ('action_choice',)
#     form = MyForm()
#
#
#
#
# admin.site.register(Rule, MyRuleAdmin)
