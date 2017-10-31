# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('necestovka', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airlines',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Aerolinky',
            },
        ),
        migrations.AlterModelOptions(
            name='airports',
            options={'verbose_name_plural': 'Letiště'},
        ),
        migrations.AlterModelOptions(
            name='flights',
            options={'verbose_name_plural': 'Lety'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name_plural': 'Objednávky'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name_plural': 'Uživatelé'},
        ),
        migrations.AlterField(
            model_name='flights',
            name='airlines',
            field=models.ForeignKey(related_name='fk_fly_airlines', to='necestovka.Airlines'),
        ),
        migrations.AlterField(
            model_name='flights',
            name='orders',
            field=models.ForeignKey(related_name='fk_fly_orders', to='necestovka.Orders'),
        ),
    ]
