# Generated by Django 4.0.1 on 2022-03-23 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0022_alter_keyboard_options_alter_keyboard_button_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyboard_button',
            name='another',
        ),
    ]