# Generated by Django 4.2.3 on 2023-08-14 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_general'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='p_amount',
            field=models.IntegerField(default=0),
        ),
    ]