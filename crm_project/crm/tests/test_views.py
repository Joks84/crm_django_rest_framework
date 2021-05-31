from rest_framework.test import APITestCase
from crm.models import Client, Company, Agent, User
from crm.serializers import ListClientSerializer, ClientSerializer, DownloadFileSerializer
from django.urls import reverse
from rest_framework import status


class TestClientViewSet(APITestCase):
    def setUp(self):
        #self.test_client = django_client()
        self.company = Company.objects.create(
            company="Company Name",
            city="Some City",
            country="Country",
            website="https://somecompany.co",
            lead="Marketing",
            phone_number="+54789546",
        )

        self.user = User.objects.create(username="jelena")
        self.agent = Agent.objects.create(user=self.user)

        self.clients = Client.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@mail.co",
            city="City",
            country="Country",
            phone_number="+5478966555",
            company=self.company,
            lead="Marketing",
            title="CEO",
            notes="Some Note",
            source="YouTube",
            lead_owner=self.agent,
        )

    def test_list_clients(self):
        # Testing GET method.
        response = self.client.get(reverse('clients-list'))
        data = response.data[0]

        # Check response data.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 6)
        self.assertEqual(data['first_name'], self.clients.first_name)
        self.assertEqual(data['last_name'], self.clients.last_name)
        self.assertEqual(data['company_name'], self.clients.company.company)
        self.assertEqual(data['title'], self.clients.title)
        self.assertEqual(data['lead'], self.clients.lead)
        self.assertEqual(data['email'], self.clients.email)

        # Check serializer data.
        serializer = ListClientSerializer([self.clients], many=True)
        self.assertEqual([data], serializer.data)

