# Generated by Django 3.1.3 on 2021-05-06 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210506_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='licensePlate',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='raspdevice',
            name='ipaddress',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]