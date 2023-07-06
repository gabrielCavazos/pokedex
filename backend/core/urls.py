from django.urls import path
from .views import PokemonListAPIView, PokemonDetailAPIView

urlpatterns = [
    path('pokemon/', PokemonListAPIView.as_view(), name='pokemon-list'),
    path('pokemon/<int:id>/', PokemonDetailAPIView.as_view(), name='pokemon-detail'),

]