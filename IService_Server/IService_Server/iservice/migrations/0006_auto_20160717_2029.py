# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-17 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0005_auto_20160717_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='service',
            name='phones',
        ),
        migrations.AddField(
            model_name='tag',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iservice.Service'),
        ),
    ]
