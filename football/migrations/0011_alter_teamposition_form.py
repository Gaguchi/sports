# Generated by Django 4.1.3 on 2023-05-09 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0010_remove_competition_standings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamposition',
            name='form',
            field=models.CharField(max_length=255),
        ),
    ]
