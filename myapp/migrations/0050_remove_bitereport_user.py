# Generated by Django 4.2.7 on 2024-08-25 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0049_bitereport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bitereport',
            name='user',
        ),
    ]
