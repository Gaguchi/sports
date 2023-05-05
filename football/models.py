from django.db import models
from django.db import IntegrityError
import requests

class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def fetch_and_create(cls):
        url = 'http://api.football-data.org/v2/competitions'
        headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for item in data['competitions']:
                competition = cls.objects.create(
                    id=item['id'],
                    name=item['name']
                )
                competition.save()

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    tla = models.CharField(max_length=255, null=True, blank=True)
    crest_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Fixture(models.Model):
    id = models.IntegerField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_fixtures', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_fixtures', on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    matchday = models.IntegerField()
    season = models.CharField(max_length=255)
    kickoff_time = models.DateTimeField()
    venue = models.CharField(max_length=255, null=True, blank=True)
    referee = models.CharField(max_length=255, null=True, blank=True)

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

