# Generated by Django 3.1.14 on 2023-07-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_pokemon_last_detail_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='attack',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='hp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='special_attack',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='special_defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='speed',
            field=models.IntegerField(default=0),
        ),
    ]
