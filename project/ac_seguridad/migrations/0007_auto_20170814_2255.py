# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 22:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ac_seguridad', '0006_auto_20170814_2036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ocurrea',
            old_name='cedula_usuarios_en_alertas',
            new_name='cedula_usuario',
        ),
    ]