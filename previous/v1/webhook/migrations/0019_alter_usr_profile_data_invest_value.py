# Generated by Django 4.0.1 on 2022-03-18 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0018_user_additional_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usr_profile_data',
            name='invest_value',
            field=models.CharField(max_length=50, verbose_name='Инвестиционный капитал'),
        ),
    ]