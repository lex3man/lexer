# Generated by Django 4.0.1 on 2022-02-16 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0004_keyboard_button_keyboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyboard_button',
            name='order',
            field=models.IntegerField(default=1, verbose_name='Порядковый номер сортировки'),
        ),
    ]
