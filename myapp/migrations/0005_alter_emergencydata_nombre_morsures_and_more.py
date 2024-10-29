# Generated by Django 5.1.1 on 2024-10-15 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_emergencydata_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencydata',
            name='nombre_morsures',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emergencydata',
            name='poids',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='emergencydata',
            name='taille',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]