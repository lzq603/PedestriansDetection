# Generated by Django 2.2.1 on 2019-06-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('atitle', models.CharField(max_length=255)),
                ('acontent', models.CharField(max_length=255)),
                ('atime', models.DateTimeField(auto_now=True)),
                ('aread', models.BooleanField()),
                ('aimage', models.CharField(max_length=255)),
                ('aPop', models.BooleanField()),
                ('aAbnormal', models.BooleanField()),
                ('aVideo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('ckey', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('cvalue', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('rnum', models.IntegerField()),
                ('rtime', models.DateTimeField(auto_now=True)),
                ('rsite', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('sname', models.CharField(max_length=50)),
                ('salarm', models.IntegerField()),
                ('sprincipal', models.CharField(max_length=50)),
                ('sphone', models.CharField(max_length=50)),
                ('sbreakout', models.IntegerField()),
                ('sarithmetic', models.CharField(max_length=50)),
            ],
        ),
    ]
