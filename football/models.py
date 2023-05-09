from django.db import models
from django.db import IntegrityError
import requests

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True, default='')
    tla = models.CharField(max_length=255, null=True, blank=True, default='')
    crest = models.URLField(null=True, blank=True, default='')
    address = models.TextField(null=True, blank=True, default='')
    website = models.URLField(null=True, blank=True, default='')
    founded = models.IntegerField(null=True, blank=True, default=0)
    club_colors = models.CharField(max_length=255, null=True, blank=True, default='')
    venue = models.CharField(max_length=255, null=True, blank=True, default='')
    last_updated = models.DateTimeField(null=True, default='1900-01-01')

    def __str__(self):
        return self.name

class parentArea(models.Model):
    parentAreaId = models.CharField(max_length=255)
    parentArea = models.CharField(max_length=255)

    def __str__(self):
        return self.parentArea

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, default=1)
    flag = models.URLField()
    parentArea = models.ForeignKey(parentArea, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Season(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateField(default='1900-01-01')
    end_date = models.DateField(default='1900-01-01')
    current_matchday = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, default=1)
    type = models.CharField(max_length=255, default=1)
    emblem = models.URLField(default='')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=1)
    plan = models.CharField(max_length=255, default='')
    current_season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='competitions')
    last_updated = models.DateTimeField(null=True, default='1900-01-01')

    # standings = models.ManyToManyField(Season, through='Standings')

    def __str__(self):
        return self.name

# class Standings(models.Model):
#     season = models.ForeignKey(Season, on_delete=models.CASCADE)
#     competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='standings_set')
#     stage = models.CharField(max_length=255, null=True, blank=True, default='')
#     type = models.CharField(max_length=255, null=True, blank=True, default='')
#     group = models.CharField(max_length=255, null=True, blank=True, default='')

#     def __str__(self):
#         return f"{self.competition.name} - {self.season.start_date} - {self.season.end_date} - {self.stage} - {self.type} - {self.group}"

class TeamPosition(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, default=None)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    form = models.CharField(max_length=255)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.position} - {self.points}pts"


class TeamCompetition(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team.name} - {self.competition.name}"


class Fixture(models.Model):
    id = models.IntegerField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_fixtures', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_fixtures', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='')
    matchday = models.IntegerField(default=0)
    kickoff_time = models.DateTimeField(default='1900-01-01T00:00:00Z')
    venue = models.CharField(max_length=255, null=True, blank=True, default='')
    referee = models.CharField(max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    def __str__(self):
        return self.name

