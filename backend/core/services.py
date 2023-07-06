import requests
from .models import GeneralUpdate, Pokemon, PokemonAbility, PokemonAbilityPokemon, PokemonType, PokemonTypePokemon
from .serializers import PokemonSerializer
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

def synchronize_pokemons():
    total_count = Pokemon.objects.count()


    if total_count < 1:
        insert_update_pokemon()
    else:
        last_general_update = GeneralUpdate.objects.first()

        two_days_ago = timezone.now() - timedelta(days=2)

        # 2 minutes just to test the code without need to wait to much
        #two_days_ago = timezone.now() - timedelta(minutes=2)

        if not last_general_update or last_general_update.last_updated <= two_days_ago:
            insert_update_pokemon()


def synchronize_detail_pokemons(pokemons):
    have_sync_pokemons = False

    for pokemon_data in pokemons:
        pokemon = Pokemon.objects.get(name=pokemon_data["name"])
        
        two_days_ago = timezone.now() - timedelta(days=2)

        if pokemon.last_detail_updated is None or pokemon.last_detail_updated <= two_days_ago:
            insert_update_pokemon_detail(pokemon)
            have_sync_pokemons = True

    return have_sync_pokemons

@transaction.atomic
def insert_update_pokemon():

    #fetch all the pokemons in a single call
    endpoint = "https://pokeapi.co/api/v2/pokemon?limit=3000"
    response = requests.get(endpoint)
    data = response.json()

    results = data["results"]
    for result in results:

        name = result["name"]

        _, _ = Pokemon.objects.get_or_create(name=name)


    update_register = GeneralUpdate.objects.first()
    
    if not update_register:
        update_register = GeneralUpdate.objects.create()
        
    update_register.last_updated = timezone.now()
    update_register.save()

@transaction.atomic
def insert_update_pokemon_detail(pokemon):
    print("test asdasd")
    endpoint = "https://pokeapi.co/api/v2/pokemon/"+pokemon.name
    pokemon_data = requests.get(endpoint).json()

    weight = pokemon_data["weight"]
    height = pokemon_data["height"]
    image_url = pokemon_data["sprites"]["front_default"]
    pokemon.weight = weight
    pokemon.height = height
    pokemon.image_url = image_url


    abilities = pokemon_data["abilities"]
    insert_update_abilities(abilities, pokemon)

    types = pokemon_data["types"]
    insert_update_types(types, pokemon)
    pokemon.last_detail_updated = timezone.now()
    pokemon.save()

def insert_update_abilities(abilities, pokemon: Pokemon):
    for ability in abilities:
        name = ability["ability"]["name"]
        slot = ability["slot"]
        active = not ability["is_hidden"]
        ability, _ = PokemonAbility.objects.get_or_create(name=name)
        pokemon_ability, _ = PokemonAbilityPokemon.objects.get_or_create(pokemon=pokemon, ability=ability)
        pokemon_ability.active = active
        pokemon_ability.slot = slot
        pokemon_ability.save()

def insert_update_types(types, pokemon: Pokemon):
    for type in types:
        name = type["type"]["name"]
        slot = type["slot"]
        type, _ = PokemonType.objects.get_or_create(name=name)
        pokemon_type, _ = PokemonTypePokemon.objects.get_or_create(pokemon=pokemon, type=type)
        pokemon_type.slot = slot
        pokemon_type.save()

