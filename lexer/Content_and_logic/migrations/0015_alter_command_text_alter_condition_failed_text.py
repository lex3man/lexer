# Generated by Django 4.0.4 on 2022-05-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Content_and_logic', '0014_condition_failed_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст реакции'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='failed_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст при неудаче'),
        ),
    ]
