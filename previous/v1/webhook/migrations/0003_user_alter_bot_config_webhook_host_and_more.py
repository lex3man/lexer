# Generated by Django 4.0.1 on 2022-02-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0002_alter_bot_config_ssl_cert_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('tg_nickname', models.CharField(max_length=50)),
                ('caption', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='bot_config',
            name='webhook_host',
            field=models.CharField(default='insiderlab.ru/', max_length=50, verbose_name='webhook host'),
        ),
        migrations.AlterField(
            model_name='bot_config',
            name='webhook_url_path',
            field=models.CharField(default='bothook/', max_length=100, verbose_name='URL path'),
        ),
    ]
