# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APPNAME', '0006_travel_joined_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='travel',
            name='joined_users',
        ),
        migrations.AddField(
            model_name='join',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APPNAME.Travel'),
        ),
        migrations.AddField(
            model_name='join',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APPNAME.User'),
        ),
    ]
