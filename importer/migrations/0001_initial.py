# Generated by Django 2.0.4 on 2018-05-08 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True)),
                ('volume', models.FloatField(blank=True)),
                ('timestamp', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_import', models.BooleanField(default=True)),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TradeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True)),
                ('volume', models.FloatField(blank=True)),
                ('time', models.FloatField(blank=True)),
                ('bs', models.CharField(blank=True, default='', max_length=200)),
                ('ml', models.CharField(blank=True, default='', max_length=200)),
                ('misce', models.CharField(blank=True, default='', max_length=200)),
                ('pair', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='importer.Pair')),
            ],
        ),
        migrations.CreateModel(
            name='Ask',
            fields=[
                ('ordervalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='importer.OrderValue')),
                ('pair', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='importer.Pair')),
            ],
            bases=('importer.ordervalue',),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('ordervalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='importer.OrderValue')),
                ('pair', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='importer.Pair')),
            ],
            bases=('importer.ordervalue',),
        ),
    ]
