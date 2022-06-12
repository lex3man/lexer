# Generated by Django 4.0.1 on 2022-02-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0002_alter_start_content_data_access_error_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='start_content',
            name='new_name_please',
            field=models.TextField(default='', verbose_name='Проедложение ввести новое имя, если сохранено неверное'),
        ),
        migrations.AddField(
            model_name='start_content',
            name='right_name',
            field=models.TextField(default='', verbose_name='Сообщение после того, как пользователь подтвердил своё имя'),
        ),
        migrations.AddField(
            model_name='start_content',
            name='user_reg_error_message',
            field=models.TextField(default='', verbose_name='Сообщение при ошибке захвата имени пользователя'),
        ),
        migrations.AddField(
            model_name='start_content',
            name='welcome_message_with_name',
            field=models.TextField(default='', verbose_name='Сообщение от бота, после того, как пользователь представился'),
        ),
    ]
