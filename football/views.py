from django.shortcuts import render
from itertools import groupby
from .models import TeamPosition

def league_standings(request):
    # Retrieve top 10 team positions and order by position
    limit = 1000  # you can set the limit to any value you want
    team_positions = TeamPosition.objects.all().order_by('competition', 'position')[:limit]
    
    # Group team positions by league name
    grouped_positions = groupby(team_positions, lambda pos: pos.competition)
    standings = {area: list(positions) for area, positions in grouped_positions}
    
    # Pass the limit as a context variable to the template
    context = {'standings': standings, 'limit': limit}
    return render(request, 'league_standings.html', context)
