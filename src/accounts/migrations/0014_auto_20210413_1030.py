# Generated by Django 3.1.3 on 2021-04-13 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_raspdevice_lastactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='boughtDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='licensePlate',
            field=models.CharField(max_length=10, null=True),
        ),
    ]