# Generated by Django 5.1.3 on 2024-11-27 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_rename_name_menuitem_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reciperequirement',
            old_name='Ingredient_Id',
            new_name='ingredient',
        ),
        migrations.RenameField(
            model_name='reciperequirement',
            old_name='menu_item_id',
            new_name='menuitem',
        ),
    ]