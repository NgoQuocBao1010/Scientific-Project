# Generated by Django 3.1.3 on 2021-03-08 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_raspdevice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raspdevice',
            name='status',
            field=models.CharField(blank=True, choices=[('online', 'online'), ('offline', 'offline')], max_length=50, null=True),
        ),
    ]
