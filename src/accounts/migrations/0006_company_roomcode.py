# Generated by Django 3.1.3 on 2021-05-07 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210507_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='roomCode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
