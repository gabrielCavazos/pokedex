# Generated by Django 3.1.14 on 2023-07-06 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230706_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='external_id',
            field=models.IntegerField(default=0),
        ),
    ]