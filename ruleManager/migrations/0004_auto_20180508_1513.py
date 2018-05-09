# Generated by Django 2.0.4 on 2018-05-08 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0004_auto_20180508_1216'),
        ('ruleManager', '0003_rule_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_choice', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell'), ('NONE', 'None')], default='None', max_length=2)),
                ('volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RuleOn2Calculs',
            fields=[
                ('rule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ruleManager.Rule')),
                ('action_choice', models.CharField(choices=[('GT', 'greater than'), ('GT', 'greater or equal than'), ('LT', 'lower than'), ('LT', 'lower or equal than'), ('NONE', 'None')], default='None', max_length=2)),
                ('data_1', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='calculator.Calcul')),
            ],
            bases=('ruleManager.rule',),
        ),
        migrations.RemoveField(
            model_name='rule',
            name='data',
        ),
        migrations.AddField(
            model_name='action',
            name='data_2',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='ruleManager.Rule'),
        ),
    ]