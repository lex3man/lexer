# Generated by Django 4.0.4 on 2022-05-19 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tgbot_rename_envvars_envvar'),
    ]

    operations = [
        migrations.AddField(
            model_name='tgbot',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
