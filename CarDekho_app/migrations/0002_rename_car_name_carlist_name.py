# Generated by Django 5.1.7 on 2025-04-24 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CarDekho_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carlist',
            old_name='car_name',
            new_name='name',
        ),
    ]
