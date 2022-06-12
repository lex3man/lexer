# Generated by Django 4.0.1 on 2022-02-22 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0019_alter_keyboard_button_another_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyboard_button',
            name='visibls_for',
            field=models.CharField(choices=[('all', 'Для всех'), ('client', 'Только для клиентов'), ('partner', 'Только для партнеров (не только активных)'), ('active', 'Только для активных партнеров'), ('admin', 'Только для админов'), ('other', 'Для другой группы')], default='all', max_length=10, verbose_name='Для каких пользователей доступна кнопка'),
        ),
    ]