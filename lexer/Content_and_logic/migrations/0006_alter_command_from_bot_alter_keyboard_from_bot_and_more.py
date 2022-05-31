# Generated by Django 4.0.4 on 2022-05-23 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tgbot_active'),
        ('Content_and_logic', '0005_alter_command_caption_alter_command_delay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='from_bot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgbot', verbose_name='Через бота'),
        ),
        migrations.AlterField(
            model_name='keyboard',
            name='from_bot',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgbot', verbose_name='Через бота'),
        ),
        migrations.AlterField(
            model_name='keyboard_button',
            name='from_bot',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgbot', verbose_name='Через бота'),
        ),
    ]