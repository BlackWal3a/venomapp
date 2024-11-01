# Generated by Django 5.1.1 on 2024-10-13 09:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BiteReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('place_of_bite', models.CharField(max_length=255)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('date', models.DateField()),
                ('time_since_bite', models.CharField(max_length=100)),
                ('symptom', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('nom_complet', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('sexe', models.CharField(max_length=10)),
                ('poids', models.DecimalField(decimal_places=2, max_digits=5)),
                ('taille', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_heure_envenimation', models.CharField(max_length=255)),
                ('lieu_envenimation', models.CharField(max_length=255)),
                ('activite', models.CharField(max_length=255)),
                ('lieu_morsure', models.CharField(max_length=255)),
                ('nombre_morsures', models.IntegerField()),
                ('recidivistes', models.CharField(max_length=255)),
                ('type_animal', models.CharField(max_length=255)),
                ('taille_animal', models.CharField(blank=True, max_length=255, null=True)),
                ('couleur_animal', models.CharField(blank=True, max_length=255, null=True)),
                ('douleur', models.BooleanField(default=False)),
                ('gonflement', models.BooleanField(default=False)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pression', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NormalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('units', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, max_length=50, null=True)),
                ('dark_mode', models.IntegerField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_geo_date', models.DateField(blank=True, null=True)),
                ('end_geo_date', models.DateField(blank=True, null=True)),
                ('start_supplier_date', models.DateField(blank=True, null=True)),
                ('end_supplier_date', models.DateField(blank=True, null=True)),
                ('is_selected', models.BooleanField(default=False)),
                ('provider1', models.CharField(blank=True, max_length=50, null=True)),
                ('provider2', models.CharField(blank=True, max_length=50, null=True)),
                ('rates', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('update1', models.CharField(blank=True, max_length=50, null=True)),
                ('suppliers_global_selection', models.IntegerField(blank=True, null=True)),
                ('supplier_name_filter', models.CharField(blank=True, max_length=100, null=True)),
                ('geography_global_selection', models.IntegerField(blank=True, null=True)),
                ('time_global_selection', models.IntegerField(blank=True, null=True)),
                ('time_by_filter', models.IntegerField(blank=True, null=True)),
                ('time_chart_type', models.IntegerField(blank=True, null=True)),
                ('aircraft_chart_type', models.IntegerField(blank=True, null=True)),
                ('geography_filter_id', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
