# Generated by Django 3.1.3 on 2021-03-13 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_raspdevice_lastactive'),
        ('realtime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('ongoing', 'ongoing'), ('ended', 'ended')], max_length=20)),
                ('endTime', models.DateTimeField(null=True)),
                ('devices', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.raspdevice')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detect', models.CharField(choices=[('Yawning', 'Yawning'), ('Drowsiness', 'Drowsiness'), ('MissingFace', 'MissingFace')], max_length=50)),
                ('timeOccured', models.DateTimeField(null=True)),
                ('drive', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realtime.drive')),
            ],
        ),
    ]