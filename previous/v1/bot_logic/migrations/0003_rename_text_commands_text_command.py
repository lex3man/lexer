# Generated by Django 4.0.1 on 2022-02-21 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_logic', '0002_text_commands'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='text_commands',
            new_name='text_command',
        ),
    ]
