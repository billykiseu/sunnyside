# Generated by Django 4.0.6 on 2022-10-02 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_ipmodel_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipmodel',
            name='ip',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
