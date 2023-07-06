from rest_framework import serializers
from .models import Pokemon, PokemonAbility, PokemonAbilityPokemon


class PokemonAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonAbility
        fields = ['name']


class PokemonSerializer(serializers.ModelSerializer):
    abilities_count = serializers.SerializerMethodField()
    active_abilities = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'weight', 'height', 'abilities_count', 'active_abilities', 'favorite']

    def get_abilities_count(self, obj):
        return obj.abilities.count()

    def get_active_abilities(self, obj):
        active_abilities = PokemonAbility.objects.filter(pokemon=obj, pokemonabilitypokemon__active=True).order_by('pokemonabilitypokemon__slot')
        return [active_abilities.name for active_abilities in active_abilities]


class PokemonDetailSerializer(serializers.ModelSerializer):
    abilities = PokemonAbilitySerializer(many=True, read_only=True)
    types = serializers.StringRelatedField(many=True)

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'weight', 'height', 'abilities', 'types', 'image_url', 'favorite', 'image_url']