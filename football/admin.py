from django.contrib import admin
from .models import parentArea, Area, Competition, Season, Team, TeamCompetition, Fixture, Player


class parentAreaAdmin(admin.ModelAdmin):
    list_display = ('parentAreaId', 'parentArea')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'flag', 'parentArea')


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'type', 'emblem', 'area', 'plan', 'current_season_id', 'last_updated')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'current_matchday', 'winner')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'tla', 'crest_url', 'address', 'website', 'founded', 'club_colors', 'venue', 'last_updated')


class TeamCompetitionAdmin(admin.ModelAdmin):
    list_display = ('team', 'competition', 'is_current')


class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'season', 'home_team', 'away_team', 'status', 'matchday', 'kickoff_time', 'venue', 'referee')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'nationality', 'team', 'appearances', 'goals', 'assists')


admin.site.register(parentArea, parentAreaAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamCompetition, TeamCompetitionAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Player, PlayerAdmin)
