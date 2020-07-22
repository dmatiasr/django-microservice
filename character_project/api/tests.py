import json

from django.contrib.auth.models import User
from django.db.models import (
    Avg,
    Max
)

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    Character,
    Score
)
from .serializer import (
    CharacterSerializer,
    ScoreSerializer
)


class EndPointTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='matias',
            password='password'
        )

        self.token = Token.objects.create(
            user=self.user
        )
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_get_request_character(self):

        response = self.client.get(
            '/character/3/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "R2-D2")

    def test_post_request_character(self):

        response = self.client.post(
            '/character/1/rating/',
            {'score': '3'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_request_character_bad_request(self):
        response = self.client.post(
            '/character/1/rating/',
            {'': '3'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_character_just_acepted_request(self):
        response = self.client.post(
            '/character/1/rating/',
            {'score': '6'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(json.loads(response.content), {"Error": "score must be between 1 to 5"})

    def test_post_request_character_creation(self):

        response = self.client.post(
            '/character/222/rating/',
            {'score': '3'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

