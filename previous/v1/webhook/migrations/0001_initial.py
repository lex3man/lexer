# Generated by Django 4.0.1 on 2022-01-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot_config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_name', models.CharField(max_length=50, verbose_name='Имя бота')),
                ('token', models.CharField(max_length=100, verbose_name='API token')),
                ('webhook_host', models.CharField(default='insiderlab.ru', max_length=50, verbose_name='webhook host')),
                ('webhook_port', models.IntegerField(default=443)),
                ('webhook_url_path', models.CharField(default='/bothook', max_length=50, verbose_name='URL path')),
                ('ssl_cert', models.CharField(default='/etc/letsencrypt/live/insiderlab.ru/fullchain.pem', max_length=50, verbose_name='Path to the ssl certificate')),
                ('ssl_private', models.CharField(default='/etc/letsencrypt/live/insiderlab.ru/privkey.pem', max_length=50, verbose_name='Path to the ssl private key')),
                ('webapp_host', models.CharField(default='localhost', max_length=50, verbose_name='LAN address to listen webhooks')),
                ('webapp_port', models.IntegerField(default=3001)),
            ],
        ),
    ]
