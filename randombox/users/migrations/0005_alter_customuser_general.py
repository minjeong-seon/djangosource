# Generated by Django 4.2.3 on 2023-08-11 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randombox', '0001_initial'),
        ('users', '0004_remove_customuser_general_customuser_general'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='general',
            field=models.ManyToManyField(blank=True, related_name='custom_users', to='randombox.general'),
        ),
    ]