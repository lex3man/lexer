# Generated by Django 4.0.4 on 2022-05-23 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Content_and_logic', '0008_alter_command_from_bot_alter_keyboard_from_bot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='keyboard',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Content_and_logic.keyboard', verbose_name='Клавиатура'),
        ),
    ]