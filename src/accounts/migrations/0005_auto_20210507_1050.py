# Generated by Django 3.1.3 on 2021-05-07 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210507_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raspdevice',
            name='status',
            field=models.CharField(blank=True, choices=[('online', 'online'), ('offline', 'offline')], default='offline', max_length=50, null=True),
        ),
    ]
