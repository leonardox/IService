# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-15 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0013_auto_20160814_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
