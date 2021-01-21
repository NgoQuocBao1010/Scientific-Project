# Generated by Django 3.1.3 on 2021-01-20 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RaspberryDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline')], max_length=20)),
                ('car', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.car')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activityName', models.CharField(choices=[('Starting', 'Starting'), ('Stopped', 'Stopped'), ('Yawning', 'Yawning'), ('Drowsiness', 'Drowsiness'), ('Unconscious', 'Unconscious')], max_length=50)),
                ('timeOccured', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('isRead', models.BooleanField(blank=True, null=True)),
                ('devices', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.raspberrydevice')),
            ],
        ),
    ]