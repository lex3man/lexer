# Generated by Django 4.0.4 on 2022-05-22 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tgbot_active'),
        ('Users_assets', '0004_alter_user_tg_id_alter_usertag_tag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='from_bot',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgbot', verbose_name='Через бота'),
        ),
    ]