# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 20:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ac_seguridad', '0005_auto_20170814_2030'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ocurre_a',
            new_name='OcurreA',
        ),
        migrations.RenameModel(
            old_name='Ocurre_en',
            new_name='OcurreEn',
        ),
    ]