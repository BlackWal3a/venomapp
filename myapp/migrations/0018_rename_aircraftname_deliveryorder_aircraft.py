# Generated by Django 4.2.7 on 2024-03-13 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_deliveryorder_delete_deliveryorders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveryorder',
            old_name='AircraftName',
            new_name='Aircraft',
        ),
    ]
