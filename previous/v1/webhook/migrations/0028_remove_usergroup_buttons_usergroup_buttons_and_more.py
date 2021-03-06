# Generated by Django 4.0.1 on 2022-03-28 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0024_alter_keyboard_buttons'),
        ('webhook', '0027_usergroup_buttons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='buttons',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='buttons',
            field=models.ManyToManyField(blank=True, null=True, to='bot_content.keyboard_button', verbose_name='По каким кнопкам добавлять в группу'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to='webhook.User', verbose_name='Члены группы'),
        ),
    ]
