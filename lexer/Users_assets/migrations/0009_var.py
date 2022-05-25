# Generated by Django 4.0.4 on 2022-05-25 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users_assets', '0008_alter_user_from_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='Переменная (латиницей)')),
                ('value', models.CharField(max_length=150, verbose_name='Значение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users_assets.user', verbose_name='Собеседник')),
            ],
            options={
                'verbose_name': 'Переменная',
                'verbose_name_plural': 'Переменные',
            },
        ),
    ]
