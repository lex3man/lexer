# Generated by Django 4.0.5 on 2022-06-17 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Communications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sending',
            name='in_order',
            field=models.BooleanField(default=False, verbose_name='В очереди'),
        ),
    ]