from django.db import models
from django.utils import timezone

class GeneralUpdate(models.Model):
    last_updated = models.DateTimeField(auto_now=True)

class PokemonAbility(models.Model):
    name = models.CharField(max_length=100, unique=True)

class PokemonAbilityPokemon(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE)
    ability = models.ForeignKey(PokemonAbility, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    slot = models.IntegerField(default=0)


class PokemonType(models.Model):
    name = models.CharField(max_length=100, unique=True)

class PokemonTypePokemon(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE)
    type = models.ForeignKey(PokemonType, on_delete=models.CASCADE)
    slot = models.IntegerField(default=0)

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    abilities = models.ManyToManyField(PokemonAbility, through=PokemonAbilityPokemon)
    types = models.ManyToManyField(PokemonType, through=PokemonTypePokemon)
    image_url = models.URLField(null=True)
    
    external_id = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    
    # to keep the favorite related to a user, let it here to make the example simplest
    favorite = models.BooleanField(default=False)
    last_detail_updated = models.DateTimeField(null=True)


    def set_pokemon_detail(self, weight, height, image_url, external_id, pokemon_stats):
        self.weight = weight
        self.height = height
        self.image_url = image_url
        self.external_id = external_id

        self.hp = pokemon_stats["hp"]
        self.attack = pokemon_stats["attack"]
        self.defense = pokemon_stats["defense"]
        self.special_attack = pokemon_stats["special-attack"]
        self.special_defense = pokemon_stats["special-defense"]
        self.speed = pokemon_stats["speed"]
        self.last_detail_updated = timezone.now()
        self.save()
        