# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-14 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0016_servicepicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
