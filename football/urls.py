from django.urls import path
from .views import league_standings

urlpatterns = [
    path('league-standings/', league_standings, name='league_standings'),
    # other URL patterns...
]
