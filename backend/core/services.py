import requests
from .models import GeneralUpdate, Pokemon, PokemonAbility, PokemonAbilityPokemon, PokemonType, PokemonTypePokemon
from django.utils import timezone
from datetime import timedelta
from django.db import transaction


class PokemonSyncService():
    @classmethod
    def synchronize_pokemons(cls):
        total_count = Pokemon.objects.count()


        if total_count < 1:
            cls.insert_update_pokemon()
        else:
            last_general_update = GeneralUpdate.objects.first()

            two_days_ago = timezone.now() - timedelta(days=2)

            # 2 minutes just to test the code without need to wait to much
            #two_days_ago = timezone.now() - timedelta(minutes=2)

            if not last_general_update or last_general_update.last_updated <= two_days_ago:
                cls.insert_update_pokemon()

    @classmethod
    def synchronize_detail_pokemons(cls, pokemons):
        have_sync_pokemons = False

        for pokemon_data in pokemons:
            pokemon = Pokemon.objects.get(name=pokemon_data["name"])
            
            two_days_ago = timezone.now() - timedelta(days=2)

            if pokemon.last_detail_updated is None or pokemon.last_detail_updated <= two_days_ago:
                cls.insert_update_pokemon_detail(pokemon)
                have_sync_pokemons = True

        return have_sync_pokemons

    @classmethod
    @transaction.atomic
    def insert_update_pokemon(cls):

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

    @classmethod
    @transaction.atomic
    def insert_update_pokemon_detail(cls, pokemon: Pokemon):
        endpoint = "https://pokeapi.co/api/v2/pokemon/"+pokemon.name
        pokemon_data = requests.get(endpoint).json()

        weight = pokemon_data["weight"]
        height = pokemon_data["height"]
        external_id = pokemon_data["id"]
        image_url = pokemon_data["sprites"]["front_default"]

        pokemon_stats = cls.get_pokemon_stats(pokemon_data["stats"])


        abilities = pokemon_data["abilities"]
        cls.insert_update_abilities(abilities, pokemon)

        types = pokemon_data["types"]
        cls.insert_update_types(types, pokemon)
        
        pokemon.set_pokemon_detail(weight, height, image_url, external_id, pokemon_stats)

    @classmethod
    def get_pokemon_stats(cls, stats):
        dictionaty_stats = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "special-attack": 0,
            "special-defense": 0,
            "speed": 0,
        }

        for stat in stats:
            dictionaty_stats[stat["stat"]["name"]] = stat["base_stat"]

        return dictionaty_stats


    # Maybe this two method could be moved to the model but at the same time use the avilities array so 
    # will require more changes to move it
    @classmethod
    def insert_update_abilities(cls, abilities, pokemon: Pokemon):
        for ability in abilities:
            name = ability["ability"]["name"]
            slot = ability["slot"]
            active = not ability["is_hidden"]
            ability, _ = PokemonAbility.objects.get_or_create(name=name)
            pokemon_ability, _ = PokemonAbilityPokemon.objects.get_or_create(pokemon=pokemon, ability=ability)
            pokemon_ability.active = active
            pokemon_ability.slot = slot
            pokemon_ability.save()

    @classmethod
    def insert_update_types(cls, types, pokemon: Pokemon):
        for type in types:
            name = type["type"]["name"]
            slot = type["slot"]
            type, _ = PokemonType.objects.get_or_create(name=name)
            pokemon_type, _ = PokemonTypePokemon.objects.get_or_create(pokemon=pokemon, type=type)
            pokemon_type.slot = slot
            pokemon_type.save()

