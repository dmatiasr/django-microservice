from rest_framework import serializers, validators
from api.models import (
    Character,
    Score
)

from django.db.models import (
    Avg,
    Max
)

import traceback
import logging


class CharacterSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')
    slug = serializers.CharField(source='slug_item')
    avg = serializers.SerializerMethodField(read_only=True)
    max_score = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Character
        fields = (
            'pk',
            'slug',
            'avg',
            'max_score'
        )


    def get_avg(self, obj):
        try:
            return obj.related_character_score.aggregate(Avg('score_field'))['score_field__avg']
        except (AttributeError, KeyError):
            logging.info('{}'.format(traceback.format_exc()))
            return 0


    def get_max_score(self, obj):
        try:
            return obj.related_character_score.aggregate(Max('score_field'))['score_field__max']
        except (AttributeError, KeyError):
            logging.info('{}'.format(traceback.format_exc()))
            return 0


class ScoreSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(source='score_field')
    related_character = CharacterSerializer(read_only=True)
    related_character_key = serializers.SlugRelatedField(write_only=True,
                                                         source='related_character',
                                                         slug_field='slug_item',
                                                         queryset=Character.objects.all())

    class Meta:
        model = Score
        fields = (
            'score',
            'related_character',
            'related_character_key'
        )

    def to_internal_value(self, data):
        try:
            if 'related_character' not in data:
                raise validators.ValidationError({'Error': 'missing related character param'})
            if 'score' not in data:
                raise validators.ValidationError({'Error': 'missing score param'})
            if not isinstance(data['score'], int):
                raise validators.ValidationError({'Error': 'score param, type error'})

            data['related_character_key'] = data['related_character']
            try:
                character = Character.objects.get(slug_item=data['related_character_key'])
            except Character.DoesNotExist:
                character = Character.objects.create(
                    slug_item=data['related_character_key']
                )

            data.pop('related_character')
        except Exception:
            logging.error('{}'.format(traceback.format_exc()))

        return super(ScoreSerializer, self).to_internal_value(data)
