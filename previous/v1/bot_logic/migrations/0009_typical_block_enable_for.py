# Generated by Django 4.0.1 on 2022-03-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_logic', '0008_alter_text_command_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='typical_block',
            name='enable_for',
            field=models.CharField(default='all', max_length=10, verbose_name='Контент для'),
        ),
    ]
