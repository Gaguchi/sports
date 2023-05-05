import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
from football.models import LeagueTable, Team, Match, Goal, Card, Player
import os
import sys
sys.path.append(os.path.abspath(__file__).rsplit('/', 2)[0])

# Define a function to scrape match data from the Premier League website
def scrape_matches():
    url = "https://www.premierleague.com/results"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    match_results = soup.find_all("div", {"class": "matchFixtureContainer"})

    # Iterate over each match and extract the relevant data
    for match in match_results:
        # Get the home team name and score
        home_team_name = match.find("span", {"class": "shortname"}).text.strip()
        home_team_score = match.find("span", {"class": "score"}).text.strip()

        # Get the away team name and score
        away_team_name = match.find("span", {"class": "shortname"}).find_next_sibling("span").text.strip()
        away_team_score = match.find("span", {"class": "score"}).find_next_sibling("span").text.strip()

        # Get the match date and time
        match_time = match.find("span", {"class": "matchDate"}).text.strip()
        match_date = datetime.strptime(match_time, "%a %d %b %Y %H:%M:%S")
        match_date = timezone.make_aware(match_date)

        # Get the league name and season
        league_name = "English Premier League"
        season = "2022/23"

        # Get or create the league table object
        league_table, created = LeagueTable.objects.get_or_create(league_name=league_name, seasons=season)

        # Get or create the home team object
        home_team, created = Team.objects.get_or_create(name=home_team_name, league=league_table)

        # Get or create the away team object
        away_team, created = Team.objects.get_or_create(name=away_team_name, league=league_table)

        # Create the match object
        match_obj = Match.objects.create(home_team=home_team, away_team=away_team, home_goals=home_team_score,
                                         away_goals=away_team_score, date=match_date, league=league_table)

        # Print the match details for debugging purposes
        print(f"{home_team_name} {home_team_score} - {away_team_score} {away_team_name} - {match_date}")

        # Scrape additional match data (goals, cards) from the match page
        match_url = match.find("a", {"class": "matchFixtureContainer"}).get("href")
        match_response = requests.get(match_url)
        match_soup = BeautifulSoup(match_response.content, "html.parser")

               # Get the goal scorers and their times
        goal_data = match_soup.find_all("div", {"class": "eventLine--goal"})
        for goal in goal_data:
            player_name = goal.find("span", {"class": "name"}).text.strip()
            team_name = goal.find("span", {"class": "clubName"}).text.strip()
            goal_time = goal.find("span", {"class": "minute"}).text.strip()

            # Get or create the player object
            player, created = Player.objects.get_or_create(name=player_name, team__name=team_name)

            # Create the goal object
            goal_obj = Goal.objects.create(match=match_obj, team=home_team if team_name == home_team_name else away_team,
                                           player=player, time=goal_time)

        # Get the cards and their times
        card_data = match_soup.find_all("div", {"class": "eventLine--card"})
        for card in card_data:
            player_name = card.find("span", {"class": "name"}).text.strip()
            team_name = card.find("span", {"class": "clubName"}).text.strip()
            card_type = card.find("span", {"class": "card"})["class"][1]
            card_time = card.find("span", {"class": "minute"}).text.strip()

            # Get or create the player object
            player, created = Player.objects.get_or_create(name=player_name, team__name=team_name)

            # Create the card object
            card_obj = Card.objects.create(match=match_obj, team=home_team if team_name == home_team_name else away_team,
                                           player=player, type=card_type, time=card_time)

    print("Match data has been scraped and saved to the database.")
