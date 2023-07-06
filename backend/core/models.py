from django.db import models

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
    # weaknesses = models.ManyToManyField(PokemonType)
    # category = models.CharField(max_length=100)
    # This could be an field in a relation between user and pokemon
    # to keep the favorite related to a user, let it here to make the example simplest
    favorite = models.BooleanField(default=False)
    last_detail_updated = models.DateTimeField(null=True)