# Generated by Django 5.1.3 on 2024-11-27 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_purchase_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='name',
            new_name='title',
        ),
    ]
