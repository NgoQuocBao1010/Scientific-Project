# Generated by Django 3.1.3 on 2021-03-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210308_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='raspdevice',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
