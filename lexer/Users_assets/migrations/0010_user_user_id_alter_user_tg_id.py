# Generated by Django 4.0.4 on 2022-05-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users_assets', '0009_var'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_ID',
            field=models.CharField(default=2425, max_length=15, unique=True, verbose_name='Телеграм ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_ID',
            field=models.CharField(max_length=15, verbose_name='Телеграм ID'),
        ),
    ]