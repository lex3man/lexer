# Generated by Django 4.0.1 on 2022-03-25 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_content', '0023_remove_keyboard_button_another'),
        ('webhook', '0022_alter_usr_profile_data_age_cat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usr_profile_data',
            name='button',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot_content.keyboard'),
        ),
    ]