# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='Profile',
        ),
    ]