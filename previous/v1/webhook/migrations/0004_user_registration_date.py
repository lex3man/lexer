# Generated by Django 4.0.1 on 2022-02-14 12:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0003_user_alter_bot_config_webhook_host_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registration_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
