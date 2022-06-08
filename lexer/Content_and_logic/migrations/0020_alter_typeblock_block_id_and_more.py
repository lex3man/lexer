# Generated by Django 4.0.4 on 2022-06-08 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_tgbot_active'),
        ('Content_and_logic', '0019_remove_command_input_state_typeblock_save_to_var'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeblock',
            name='block_id',
            field=models.CharField(max_length=50, unique=True, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='typeblock',
            name='from_button',
        ),
        migrations.AddField(
            model_name='typeblock',
            name='from_button',
            field=models.ManyToManyField(blank=True, to='Content_and_logic.keyboard_button', verbose_name='По кнопке'),
        ),
        migrations.CreateModel(
            name='FuncBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_id', models.CharField(max_length=50, unique=True, verbose_name='ID')),
                ('language', models.CharField(choices=[('RUS', 'Русский'), ('ENG', 'English'), ('TUR', 'Turkish'), ('GER', 'German'), ('FR', 'Frankish')], default='RUS', max_length=5, verbose_name='Язык перевода')),
                ('input_state', models.BooleanField(default=False, verbose_name='Назначение переменых')),
                ('save_to_var', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Имя переменной для сохранения')),
                ('value', models.CharField(blank=True, max_length=150, null=True, verbose_name='Значение переменной')),
                ('conditions', models.ManyToManyField(blank=True, to='Content_and_logic.condition', verbose_name='Условия')),
                ('from_bot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tgbot', verbose_name='Через бота')),
                ('from_button', models.ManyToManyField(blank=True, to='Content_and_logic.keyboard_button', verbose_name='По кнопке')),
                ('next_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Content_and_logic.funcblock', verbose_name='Следующий блок')),
            ],
            options={
                'verbose_name': 'Типовой блок',
                'verbose_name_plural': 'Типовые блоки (сообщения от бота)',
            },
        ),
    ]