# Generated by Django 4.2 on 2023-05-07 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0002_competition_fixture_remove_goal_match_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='parentArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parentAreaId', models.CharField(max_length=255)),
                ('parentArea', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='code',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='competition',
            name='current_season_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='competition',
            name='emblem',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='competition',
            name='last_updated',
            field=models.DateTimeField(default='1900-01-01'),
        ),
        migrations.AddField(
            model_name='competition',
            name='plan',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='competition',
            name='type',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='team',
            name='address',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='club_colors',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='founded',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='last_updated',
            field=models.DateTimeField(default='1900-01-01'),
        ),
        migrations.AddField(
            model_name='team',
            name='venue',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='website',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='kickoff_time',
            field=models.DateTimeField(default='1900-01-01T00:00:00Z'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='matchday',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='referee',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='status',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='venue',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='crest_url',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='tla',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='TeamCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.competition')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.team')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(default='1900-01-01')),
                ('end_date', models.DateField(default='1900-01-01')),
                ('current_matchday', models.IntegerField(default=0)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='football.team')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(default=1, max_length=255)),
                ('flag', models.URLField()),
                ('parentArea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.parentarea')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='football.area'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.season'),
        ),
    ]
