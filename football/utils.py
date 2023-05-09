from django.db import IntegrityError
import requests
from .models import *

def fetch_and_create():
    url = 'http://api.football-data.org/v4/areas'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return

    data = response.json()

    # Process parent areas
    for areas_data in data['areas']:
        try:
            # Check if an object with this parentAreaId already exists
            obj = parentArea.objects.filter(parentAreaId=areas_data['parentAreaId']).first()
            if not obj:
                # Create the object if it does not exist
                parentArea.objects.create(
                    parentAreaId=areas_data['parentAreaId'],
                    parentArea=areas_data['parentArea'],
                )
            else:
                # print(f"Parent area object {obj} already exists.")
                pass
        except IntegrityError:
            # Handle the case where a competition with the same id already exists
            pass


        
    # Process areas
    for areas_data in data['areas']:
        try:
            # Get the parent area object for this area, if it exists
            try:
                parent_area = parentArea.objects.get(parentAreaId=areas_data['parentAreaId'])
            except parentArea.DoesNotExist:
                parent_area = None

            flag_url = areas_data['flag'] if areas_data['flag'] else ''

            Area.objects.create(
                id=areas_data['id'],
                name=areas_data['name'],
                code=areas_data['countryCode'],
                flag=flag_url,
                parentArea=parent_area,
            )
        except IntegrityError:
            # Handle the case where a competition with the same id already exists
            pass


    url = 'http://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        return

    data = response.json()

    # Process seasons
    for season_data in data['competitions']:
        try:
            # Get the area object for this area, if it exists
            # try:
            #     area = Area.objects.get(id=competition_data['area']['id'])
            # except parentArea.DoesNotExist:
            #     area = None


            Season.objects.create(
                id=season_data['currentSeason']['id'],
                start_date=season_data['currentSeason']['startDate'],
                end_date=season_data['currentSeason']['endDate'],
                current_matchday=season_data['currentSeason']['currentMatchday'],
                winner=season_data['currentSeason']['winner'],
            )
        except IntegrityError:
            # Handle the case where a competition with the same id already exists
            pass

    # Process competitions
    for competition_data in data['competitions']:
        try:
            # Get the area object for this area, if it exists
            try:
                comp_area = Area.objects.get(id=competition_data['area']['id'])
            except Area.DoesNotExist:
                comp_area = None


            Competition.objects.create(
                id=competition_data['id'],
                name=competition_data['name'],
                area=comp_area,
                code=competition_data['code'],
                type=competition_data['type'],
                emblem=competition_data['emblem'],
                plan=competition_data['plan'],
                current_season=Season.objects.get(id=competition_data['currentSeason']['id']),
                last_updated=competition_data['lastUpdated'],
            )
        except IntegrityError:
            # Handle the case where a competition with the same id already exists
            pass


    
    # Process teams
    url = 'http://api.football-data.org/v4/teams?limit=1000'
    headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # Handle the error here
        pass

    data = response.json()

    for team_data in data['teams']:
        team_id = team_data['id']
        try:
            # Try to get the team object from the database
            team_obj = Team.objects.get(id=team_id)
            # Update the existing team object with the new data
            team_obj.name = team_data['name']
            team_obj.short_name = team_data['shortName']
            team_obj.tla = team_data['tla']
            team_obj.crest = team_data['crest']
            team_obj.address = team_data['address']
            team_obj.website = team_data['website']
            team_obj.founded = team_data['founded']
            team_obj.club_colors = team_data['clubColors']
            team_obj.venue = team_data['venue']
            team_obj.last_updated = team_data['lastUpdated']
            team_obj.save()
        except Team.DoesNotExist:
            # If the team object doesn't exist, create a new one
            Team.objects.create(
                id=team_data['id'],
                name=team_data['name'],
                short_name=team_data['shortName'],
                tla=team_data['tla'],
                crest=team_data['crest'],
                address=team_data['address'],
                website=team_data['website'],
                founded=team_data['founded'],
                club_colors=team_data['clubColors'],
                venue=team_data['venue'],
                last_updated=team_data['lastUpdated'],
            )
        except IntegrityError:
            # Handle the case where a team with the same id already exists
            pass

    # Process standings
    competitions = Competition.objects.all()

    for competition in competitions:
        url = f'http://api.football-data.org/v4/competitions/{competition.code}/standings'
        headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            # Handle the error here
            continue
        
        data = response.json()

        standings = data['standings'][0]['table']

        # Process the standings datastandings = data['standings'][0]['table']
        for standings_data in standings:
            team_id = standings_data['team']['id']

            try:
                season = Season.objects.get(id=data['season']['id'])
            except Season.DoesNotExist:
                season = None

            try:
                competition = Competition.objects.get(id=data['competition']['id'])
            except Season.DoesNotExist:
                competition = None

            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                # Handle missing team here
                pass
            else:
                try:
                    TeamPosition.objects.create(
                        season=season,
                        competition=competition,
                        team=team,
                        position=standings_data['position'],
                        played=standings_data['playedGames'],
                        form=standings_data['form'],
                        won=standings_data['won'],
                        drawn=standings_data['draw'],
                        lost=standings_data['lost'],
                        points=standings_data['points'],
                        goals_for=standings_data['goalsFor'],
                        goals_against=standings_data['goalsAgainst'],
                        goal_difference=standings_data['goalDifference'],
                    )
                except IntegrityError:
                    # Handle duplicate key error here
                    pass


    # Process fixtures
    # url = 'http://api.football-data.org/v4/competitions/PL/matches'
    # headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    # response = requests.get(url, headers=headers)

    # if response.status_code != 200:
    #     # Handle the error here
    #     return
    
    # data = response.json()

    # for fixture_data in data['matches']:
    #     competition_id = fixture_data['competition']['id']
    #     home_team_id = fixture_data['homeTeam']['id']
    #     away_team_id = fixture_data['awayTeam']['id']

    #     try:
    #         competition = Competition.objects.get(id=competition_id)
    #         home_team = Team.objects.get(id=home_team_id)
    #         away_team = Team.objects.get(id=away_team_id)

    #         Fixture.objects.create(
    #             id=fixture_data['id'],
    #             competition=competition,
    #             home_team=home_team,
    #             away_team=away_team,
    #             status=fixture_data['status'],
    #             matchday=fixture_data['matchday'],
    #             season=fixture_data['season'],
    #             kickoff_time=fixture_data['utcDate'],
    #             venue=fixture_data.get('venue'),
    #             referee=fixture_data.get('referee'),
    #         )
    #     except (Competition.DoesNotExist, Team.DoesNotExist, IntegrityError):
    #         # Handle the case where the competition, home team, or away team does not exist
    #         # or where a fixture with the same id already exists
    #         pass

    # Process players
    
    # url = 'http://api.football-data.org/v4/teams'
    # headers = {'X-Auth-Token': '0104ea3ca43a4bd2a32bf841c5c1e107'}
    # response = requests.get(url, headers=headers)

    # if response.status_code != 200:
    #     # Handle the error here
    #     return

    # data = response.json()

    # for team_data in data['teams']:
    #     team_id = team_data['id']
    #     squad_url = f'http://api.football-data.org/v4/teams/{team_id}'
    #     squad_response = requests.get(squad_url, headers=headers)

    #     if squad_response.status_code != 200:
    #         # Handle the error here
    #         continue

    #     squad_data = squad_response.json().get('squad', [])

    #     for player_data in squad_data:
    #         try:
    #             player = Player.objects.create(
    #                 id=player_data['id'],
    #                 name=player_data['name'],
    #                 position=player_data.get('position'),
    #                 nationality=player_data.get('nationality'),
    #                 team_id=team_id,
    #                 appearances=player_data.get('appearances', {}).get('total', 0),
    #                 goals=player_data.get('goals', {}).get('total', 0),
    #                 assists=player_data.get('goals', {}).get('assists', 0),
    #             )
    #         except IntegrityError:
    #             # Handle the case where a player with the same id already exists
    #             pass