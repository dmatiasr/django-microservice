from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import (
    Character,
    Score
)

from django.db.models import (
    Avg,
    Max
)

import requests
import json
def index(request, id):

    return Response("Hola "+ id)



class CharacterAPIView(APIView):

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
                    # Aqui habria que hacer un tratamiento de LOG de porqué falló.

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

                # Conexion a DB
                try:
                    print(item)
                    character = Character.objects.get(slug_item=int(item))
                    print(character)
                except Character.DoesNotExist:
                    processed_payload['average_rating'] = None
                    processed_payload['max_rating'] = None

                else:
                    try:
                        avg = character.related_character_score.aggregate(Avg('score_field'))['score_field__avg']
                        max_rating = character.related_character_score.aggregate(Max('score_field'))['score_field__max']
                    except (AttributeError, KeyError):
                        avg = 0
                        max_rating = 0
                    processed_payload['average_rating'] = avg if avg else 0
                    processed_payload['max_rating'] = max_rating if max_rating else 0

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
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(processed_payload, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            item = '{0}'.format(*kwargs.get('id'))

            score = request.data.get('score', None)

            # score debe encontrarse entre 1 al 5
            if score and int(score) in range(1, 6):
                try:
                    current_character = Character.objects.get(slug_item=int(item))
                except Character.DoesNotExist:
                    new_char = Character.objects.create(slug_item=int(item))
                    Score.objects.create(
                        score_field=int(score) if score else 0,
                        related_character=new_char
                    )
                else:
                    Score.objects.create(
                        score_field=int(score) if score else 0,
                        related_character=current_character
                    )

                finally:
                    return Response({}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Validation Error': 'score must be between 1 to 5'},
                                status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
