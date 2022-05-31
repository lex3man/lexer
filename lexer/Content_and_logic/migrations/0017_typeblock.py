# Generated by Django 4.0.4 on 2022-05-27 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_tgbot_first_message'),
        ('Content_and_logic', '0016_alter_command_conditions_firsttouch'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_id', models.CharField(max_length=10, unique=True, verbose_name='ID')),
                ('language', models.CharField(choices=[('RUS', 'Русский'), ('ENG', 'English'), ('TUR', 'Turkish'), ('GER', 'German'), ('FR', 'Frankish')], default='RUS', max_length=5, verbose_name='Язык перевода')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст реакции')),
                ('input_state', models.BooleanField(default=False, verbose_name='Ожидание ввода?')),
                ('next_block', models.CharField(blank=True, default='-', max_length=50, null=True, verbose_name='Следующий блок')),
                ('delay', models.IntegerField(default=0, verbose_name='Задержка перед реакцией (секунды)')),
                ('conditions', models.ManyToManyField(blank=True, to='Content_and_logic.condition', verbose_name='Условия')),
                ('from_bot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tgbot', verbose_name='Через бота')),
                ('from_button', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Content_and_logic.keyboard_button', verbose_name='По кнопке')),
                ('keyboard', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Content_and_logic.keyboard', verbose_name='Клавиатура')),
            ],
            options={
                'verbose_name': 'Типовой блок',
                'verbose_name_plural': 'Типовые блоки (сообщения от бота)',
            },
        ),
    ]