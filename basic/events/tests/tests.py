from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import User,Events

class EventsTestCase(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('events/', include('events.urls')),
    ]

    def setUp(self) -> None:
        u1 = User.objects.create(username="atharva", password="payoda@123")
        self.valid_payload = {"type": "PARTY",
                              "start_date": "2020-09-01",
                              "end_date": "2020-09-10",
                              "city": "COIMBATORE",
                              "participants" : [{'id':u1.id}], # Users need to be created
                              "created_by" : 1
                             }
        self.invalid_payload = {"type": "",
                              "start_date": "",
                              "end_date": "2020-09-10",
                              "city": "COIMBATORE",
                              "participants" : [], # Users need to be created
                              "created_by" : 1
                             }

        token, created = Token.objects.get_or_create(user=u1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get(self):
        """To get the Event and participant list"""
        url = reverse('events:EventView')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Events.objects.all().count(), 0)

    def test_post(self):
        """ To add the Event and Participant List"""
        url = reverse('events:EventView')
        response = self.client.post(url, self.valid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Events.objects.count(), 1)

        invalid_response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_put(self):
        """ To update the Event and Participant List"""
        url = reverse('events:EventView')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('events:EventUpdateDeleteView', args={response.data['id']})
        response = self.client.post(url, self.valid_payload, format='json')

        response = self.client.put(url, self.valid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url, self.valid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)