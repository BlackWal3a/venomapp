# Generated by Django 4.2.7 on 2024-05-06 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0044_account_update1'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='time_by_filter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]