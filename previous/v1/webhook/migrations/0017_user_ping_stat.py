# Generated by Django 4.0.1 on 2022-03-14 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0016_alter_usr_profile_data_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ping_stat',
            field=models.BooleanField(default=True),
        ),
    ]
