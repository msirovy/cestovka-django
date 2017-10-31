# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('necestovka', '0002_auto_20171031_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='contact_name',
            field=models.CharField(max_length=25, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='contact_phone',
            field=models.CharField(max_length=16, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='born_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=30, blank=True, null=True),
        ),
    ]
