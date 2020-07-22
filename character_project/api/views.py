from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .models import (
    Character
)

from .serializer import (
    CharacterSerializer,
    ScoreSerializer
)

import requests
import json
import traceback
import logging


class CharacterAPIView(APIView):
    """
        CharacterAPIView class

        Implements post and get methods to Character Model

    """

    authentication_classes = (TokenAuthentication,)
    api_resource = "https://swapi.dev/api/people/"
    lookup_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        try:
            item = '{}'.format(kwargs.get('id', None))
            if item:

                root_response = requests.get(url=self.api_resource+item)
                processed_payload = json.loads(root_response.content)

                try:
                    homeworld_url = json.loads(root_response.content)['homeworld']
                except (AttributeError, KeyError, TypeError):
                    processed_payload['homeworld'] = {}
                else:

                    homeworld_response = requests.get(url=homeworld_url)
                    homeworld_content = json.loads(homeworld_response.content)
                    homeworld_detail = {}
                    homeworld_detail['name'] = homeworld_content['name'] if 'name' in homeworld_content else None
                    homeworld_detail['population'] = homeworld_content['population'] if 'population' in homeworld_content else None
                    homeworld_detail['known_residents_count'] = len([elem for elem in homeworld_content['population']])

                    processed_payload['homeworld'] = homeworld_detail

                try:
                    # Dado que es una lista, se toma como precondicion elegir el 1ero que exista.
                    specie_response = requests.get(url=json.loads(root_response.content)['species'][0])
                except (KeyError, AttributeError, TypeError, IndexError):
                    processed_payload['species'] = ""
                else:
                    processed_payload['species'] = json.loads(specie_response.content)['name']

                try:
                    character = Character.objects.get(slug_item=int(item))

                except Character.DoesNotExist:
                    processed_payload['average_rating'] = None
                    processed_payload['max_rating'] = None

                else:
                    character_serialized = CharacterSerializer(instance=character)
                    processed_payload['average_rating'] = character_serialized.data.get('avg', None)
                    processed_payload['max_rating'] = character_serialized.data.get('max_score', None)

                # Se eliminan campos no necesarios a informar.
                try:
                    processed_payload.pop('films')
                    processed_payload.pop('starships')
                    processed_payload.pop('created')
                    processed_payload.pop('edited')
                    processed_payload.pop('url')
                    processed_payload.pop('vehicles')
                except KeyError:
                    pass
            else:
                processed_payload = {}
        except Exception:
            logging.error("{}".format(traceback.format_exc()))
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(processed_payload, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            item = '{}'.format(kwargs.get('id'))

            score = request.data.get('score', None)

            # score debe encontrarse entre 1 al 5
            if score and int(score) in range(1, 6):

                data = {
                    'score': int(score),
                    'related_character': int(item)
                }
                score_serialized = ScoreSerializer(data=data)
                try:
                    score_serialized.is_valid()
                except Exception:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                score_serialized.save()
                return Response(score_serialized.data, status=status.HTTP_201_CREATED)
            elif not score:
                return Response({'Error': 'missing "score" param'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Error': 'score must be between 1 to 5'},
                                status=status.HTTP_202_ACCEPTED)

        except Exception:
            logging.error("{}".format(traceback.format_exc()))
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
