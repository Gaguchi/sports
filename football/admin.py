from django.contrib import admin
from .models import Competition, Team, Fixture, Player

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'tla', 'crest_url')
    ordering = ('id',)

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'home_team', 'away_team', 'status', 'matchday', 'season', 'kickoff_time', 'venue', 'referee')
    ordering = ('id',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'nationality', 'team', 'appearances', 'goals', 'assists')
    ordering = ('id',)
