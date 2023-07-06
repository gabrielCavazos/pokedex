from rest_framework import generics
from django.db.models import Avg
from core.services import synchronize_pokemons, synchronize_detail_pokemons
from .models import GeneralUpdate, Pokemon
from .serializers import PokemonSerializer, PokemonDetailSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action


class PokemonListAPIView(generics.ListAPIView):
    queryset = Pokemon.objects.all().order_by("-favorite", "name")
    serializer_class = PokemonSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # This can be a task that will be called maybe every day during the night
        # in this case will only synchronize if there are no saved pokemons or if the last update was 2 days ago
        synchronize_pokemons()

        response = super().list(request, *args, **kwargs)
        print("test asdasd")

        have_been_sync =  synchronize_detail_pokemons(response.data["results"])
        print("test sd", have_been_sync)

        if have_been_sync:
            response = super().list(request, *args, **kwargs)

        # Calculate weight and height averages
        results = response.data["results"]
        weight_average = sum(d['weight'] for d in results) / len(results)
        height_average = sum(d['height'] for d in results) / len(results)

        # Add averages to the response data
        response.data['weight_average'] = round(weight_average)
        response.data['height_average'] = round(height_average)

        return response

class PokemonDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonDetailSerializer
    lookup_field = 'id'


    def partial_update(self, request, id=None):
        instance = self.get_object()
        instance.favorite = not instance.favorite
        instance.save()


        queryset = Pokemon.objects.filter(favorite=True)
        # Calculate averages for the current page only
        count = Pokemon.objects.filter(favorite=True).count()
        weight_average = 0
        height_average = 0
        if count > 0:
            weight_average = round(queryset.aggregate(Avg('weight'))['weight__avg'])
            height_average = round(queryset.aggregate(Avg('height'))['height__avg'])

        

        return Response({"weight_average": weight_average, "height_average": height_average, "count": count})