# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-14 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='definition',
            field=models.CharField(max_length=1000),
        ),
    ]
