# Generated by Django 4.1.1 on 2022-10-04 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_item_views_alter_profile_profilepic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='targetfile',
            new_name='filetarget',
        ),
    ]
