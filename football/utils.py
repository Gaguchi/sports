from django.db import models
from django.db import IntegrityError
import requests
from .models import *

def fetch_and_create():
    url = 'http://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return

    data = response.json()

    # Process competitions
    for competition_data in data['competitions']:
        try:
            Competition.objects.create(
                id=competition_data['id'],
                name=competition_data['name'],
            )
        except IntegrityError:
            # Handle the case where a competition with the same id already exists
            pass

    # Process teams
    url = 'http://api.football-data.org/v4/teams'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return

    data = response.json()

    for team_data in data['teams']:
        try:
            Team.objects.create(
                id=team_data['id'],
                name=team_data['name'],
                short_name=team_data.get('shortName'),
                tla=team_data.get('tla'),
                crest_url=team_data.get('crestUrl'),
            )
        except IntegrityError:
            # Handle the case where a team with the same id already exists
            pass

    # Process fixtures
    url = 'http://api.football-data.org/v4/competitions/PL/matches'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return
    
    data = response.json()

    for fixture_data in data['matches']:
        competition_id = fixture_data['competition']['id']
        home_team_id = fixture_data['homeTeam']['id']
        away_team_id = fixture_data['awayTeam']['id']

        try:
            competition = Competition.objects.get(id=competition_id)
            home_team = Team.objects.get(id=home_team_id)
            away_team = Team.objects.get(id=away_team_id)

            Fixture.objects.create(
                id=fixture_data['id'],
                competition=competition,
                home_team=home_team,
                away_team=away_team,
                status=fixture_data['status'],
                matchday=fixture_data['matchday'],
                season=fixture_data['season'],
                kickoff_time=fixture_data['utcDate'],
                venue=fixture_data.get('venue'),
                referee=fixture_data.get('referee'),
            )
        except (Competition.DoesNotExist, Team.DoesNotExist, IntegrityError):
            # Handle the case where the competition, home team, or away team does not exist
            # or where a fixture with the same id already exists
            pass

    # Process players
    
    url = 'http://api.football-data.org/v4/teams'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return

    data = response.json()

    for team_data in data['teams']:
        team_id = team_data['id']
        squad_url = f'http://api.football-data.org/v4/teams/{team_id}'
        squad_response = requests.get(squad_url, headers=headers)

        if squad_response.status_code != 200:
            # Handle the error here
            continue

        squad_data = squad_response.json().get('squad', [])

        for player_data in squad_data:
            try:
                player = Player.objects.create(
                    id=player_data['id'],
                    name=player_data['name'],
                    position=player_data.get('position'),
                    nationality=player_data.get('nationality'),
                    team_id=team_id,
                    appearances=player_data.get('appearances', {}).get('total', 0),
                    goals=player_data.get('goals', {}).get('total', 0),
                    assists=player_data.get('goals', {}).get('assists', 0),
                )
            except IntegrityError:
                # Handle the case where a player with the same id already exists
                pass