import requests
from football.models import *

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
