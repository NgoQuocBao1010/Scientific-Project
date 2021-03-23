# Generated by Django 3.1.3 on 2021-03-04 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_car_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='licenseID',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.profile'),
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
    ]