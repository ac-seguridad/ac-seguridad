# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alertas',
            fields=[
                ('Numero_alertas', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('RIF', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=200)),
                ('Numero_de_puestos', models.IntegerField(default=1000)),
                ('Acceso_restringido', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ocurre_a',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha_alertas', models.DateTimeField(verbose_name='fecha de alerta')),
            ],
        ),
        migrations.CreateModel(
            name='Ocurre_en',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha_alertas', models.DateTimeField(verbose_name='fecha de alerta')),
                ('Numero_alertas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Alertas')),
                ('RIF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Estacionamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero_ticket', models.IntegerField(default=0)),
                ('Hora_entrada', models.DateTimeField(verbose_name='Hora de entrada')),
                ('Hora_salida', models.DateTimeField(verbose_name='Hora de salida')),
                ('Pagado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=25)),
                ('cedula', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('contrasena', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('Placa', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Cedula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='Placa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Vehiculos'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='RIF',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Estacionamiento'),
        ),
        migrations.AddField(
            model_name='ocurre_a',
            name='Cedula_usuarios_en_alertas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Usuarios'),
        ),
        migrations.AddField(
            model_name='ocurre_a',
            name='Numero_alertas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ac_seguridad.Alertas'),
        ),
    ]