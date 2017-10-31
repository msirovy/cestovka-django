# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airports',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('arrive_time', models.DateTimeField()),
                ('airlines', models.CharField(max_length=20)),
                ('fly_no', models.CharField(max_length=10)),
                ('arrive_place', models.ForeignKey(related_name='fk_arrive_airport', to='necestovka.Airports')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('contact_name', models.CharField(max_length=25)),
                ('contact_email', models.EmailField(max_length=25)),
                ('contact_phone', models.CharField(max_length=12)),
                ('state', models.CharField(max_length=10, choices=[('zaplacena', 'Zaplacena'), ('rozpracovana', 'Rozpracovana'), ('nova', 'Nova'), ('zrusena', 'Zrusena')])),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('born_year', models.IntegerField()),
                ('email', models.EmailField(max_length=30)),
                ('cabin_lugg', models.CharField(max_length=10, choices=[('1', '21x21x24'), ('2', '22x22x21')])),
                ('checked_lugg', models.CharField(max_length=10, choices=[('1', '40x50x60'), ('2', '50x65x45')])),
                ('orders', models.ForeignKey(related_name='user2orders', to='necestovka.Orders')),
            ],
        ),
        migrations.AddField(
            model_name='flights',
            name='orders',
            field=models.ForeignKey(related_name='fly2orders', to='necestovka.Orders'),
        ),
        migrations.AddField(
            model_name='flights',
            name='start_place',
            field=models.ForeignKey(related_name='fk_start_airport', to='necestovka.Airports'),
        ),
    ]
