# Generated by Django 4.0.1 on 2022-02-18 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0009_text_commands'),
    ]

    operations = [
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name_state', max_length=50, verbose_name='Имя переменной')),
                ('caption', models.CharField(default='Новая позиция', max_length=50, verbose_name='Отображаемое название позиции')),
                ('state_id', models.CharField(max_length=50, verbose_name='ID позиции')),
            ],
        ),
        migrations.CreateModel(
            name='typical_block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='Назавание блока')),
                ('block_id', models.CharField(max_length=50, verbose_name='ID блока')),
                ('from_button', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_content.keyboard_button', verbose_name='По какой кнопке появиться')),
                ('kb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_content.keyboard', verbose_name='Клавиатура')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_content.state', verbose_name='Штатная позиция')),
            ],
        ),
    ]
