from rest_framework import generics
from django.db.models import Avg
from core.services import PokemonSyncService
from .models import Pokemon
from .serializers import PokemonSerializer, PokemonDetailSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PokemonListAPIView(generics.ListAPIView):
    queryset = Pokemon.objects.all().order_by("-favorite", "name")
    serializer_class = PokemonSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # This can be a task that will be called maybe every day during the night
        # in this case will only synchronize if there are no saved pokemons or if the last update was 2 days ago
        PokemonSyncService.synchronize_pokemons()

        response = super().list(request, *args, **kwargs)

        # This function will update/sync the detail of the pokemon in this page
        # i do it in this way because is really hard try get the paginated queryset
        # an is better sync just the ones that i want to respond instead of sync all the pokemons
        # we make the response faster and reduce the charge (sync all pokemons in a single call is like 4 mins)
        # This should no be necessary is this were a cron job/task running every day
        have_been_sync =  PokemonSyncService.synchronize_detail_pokemons(response.data["results"])

        # If there were updated pokemons re calculate the response
        if have_been_sync:
            response = super().list(request, *args, **kwargs)

        # Calculate weight and height , (do in this way because django dont like to provide the page queryset :c)
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
        count = queryset.count()
        weight_average = 0
        height_average = 0
        if count > 0:
            weight_average = round(queryset.aggregate(Avg('weight'))['weight__avg'])
            height_average = round(queryset.aggregate(Avg('height'))['height__avg'])

        

        return Response({"weight_average": weight_average, "height_average": height_average, "count": count})