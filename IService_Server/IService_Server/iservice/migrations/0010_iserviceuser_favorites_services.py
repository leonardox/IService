# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-26 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0009_auto_20160720_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='iserviceuser',
            name='favorites_services',
            field=models.ManyToManyField(to='iservice.Service'),
        ),
    ]
