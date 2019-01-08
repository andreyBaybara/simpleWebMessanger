# Generated by Django 2.1.4 on 2019-01-07 13:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sended_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 7, 13, 41, 48, 693229, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]