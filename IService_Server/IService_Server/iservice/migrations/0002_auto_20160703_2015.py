# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-03 20:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iserviceuser',
            old_name='foto',
            new_name='picture',
        ),
    ]
