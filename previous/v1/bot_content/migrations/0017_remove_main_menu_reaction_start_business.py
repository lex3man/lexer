# Generated by Django 4.0.1 on 2022-02-21 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0016_delete_text_commands'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='main_menu_reaction',
            name='start_business',
        ),
    ]
