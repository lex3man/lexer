# Generated by Django 4.0.4 on 2022-06-08 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Content_and_logic', '0020_alter_typeblock_block_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FuncBlock',
        ),
    ]