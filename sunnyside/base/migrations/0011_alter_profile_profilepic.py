# Generated by Django 4.0.6 on 2022-10-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_item_wavfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profilepic',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
