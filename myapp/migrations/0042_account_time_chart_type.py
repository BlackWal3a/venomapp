# Generated by Django 4.2.7 on 2024-04-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0041_account_time_global_selection'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='time_chart_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
