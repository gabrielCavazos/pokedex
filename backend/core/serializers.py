from rest_framework import serializers
from .models import Pokemon, PokemonAbility, PokemonAbilityPokemon, PokemonType


class PokemonAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonAbility
        fields = ['name']


class PokemonSerializer(serializers.ModelSerializer):
    abilities_count = serializers.SerializerMethodField()
    active_abilities = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = [
            'id',
            'external_id', 
            'name', 
            'weight', 
            'height', 
            'abilities_count', 
            'active_abilities', 
            'favorite'
        ]

    def get_abilities_count(self, obj):
        return obj.abilities.count()

    def get_active_abilities(self, obj):
        active_abilities = PokemonAbility.objects.filter(pokemon=obj, pokemonabilitypokemon__active=True).order_by('pokemonabilitypokemon__slot')
        return [active_abilities.name for active_abilities in active_abilities]


class PokemonDetailSerializer(serializers.ModelSerializer):
    active_abilities = serializers.SerializerMethodField()
    not_active_abilities = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = [
            'id', 
            'external_id', 
            'name', 
            'weight', 
            'height', 
            'active_abilities', 
            'not_active_abilities', 
            'types', 
            'image_url', 
            'favorite', 
            'image_url',
            'hp',
            'attack',
            'defense',
            'special_attack',
            'special_defense',
            'speed',
        ]
        
    def get_active_abilities(self, obj):
        active_abilities = PokemonAbility.objects.filter(pokemon=obj, pokemonabilitypokemon__active=True).order_by('pokemonabilitypokemon__slot')
        return [active_ability.name for active_ability in active_abilities]
    
    def get_not_active_abilities(self, obj):
        not_active_abilities = PokemonAbility.objects.filter(pokemon=obj, pokemonabilitypokemon__active=False).order_by('pokemonabilitypokemon__slot')
        return [not_active_ability.name for not_active_ability in not_active_abilities]
    
    def get_types(self, obj):
        types = PokemonType.objects.filter(pokemon=obj).order_by('pokemontypepokemon__slot')
        return [type.name for type in types]