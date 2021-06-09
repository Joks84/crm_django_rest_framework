from rest_framework.test import APITestCase
from crm.models import Client, Company, Agent, User
from crm.serializers import ListClientSerializer, ClientSerializer, DownloadFileSerializer
from django.urls import reverse
from rest_framework import status
from datetime import date

# run from project directory: python manage.py test crm.tests.test_client_viewset

class TestClientViewSet(APITestCase):
    def setUp(self):
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
        # Testing GET method for listing clients.
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


    def test_retrieve_client(self):
        # Testing retrieve method for one client.
        # Passing the client's id to the url and checking response.
        response = self.client.get(reverse('clients-detail', args=[self.clients.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(reverse('clients-detail', args=[self.clients.id]), f'/clients/{self.clients.id}/')

       # Testing if the response data matches the data from created client.
        data = response.data
        self.assertEqual(data['first_name'], self.clients.first_name)
        self.assertEqual(data['last_name'], self.clients.last_name)
        self.assertEqual(data['email'], self.clients.email)
        self.assertEqual(data['city'], self.clients.city)
        self.assertEqual(data['country'], self.clients.country)
        self.assertEqual(data['phone_number'], self.clients.phone_number)
        self.assertEqual(data['company'], self.company.id)
        self.assertEqual(data['company_name'], self.company.company)
        self.assertEqual(data['date_created'], f"{date.today():%Y-%m-%d}")
        self.assertEqual(data['lead'], self.clients.lead)
        self.assertEqual(data['title'], self.clients.title)
        self.assertEqual(data['notes'], self.clients.notes)
        self.assertEqual(data['source'], self.clients.source)
        self.assertEqual(data['lead_owner_name'], self.user.username)

        # Testing if response data matches the serializer which is been used.
        serializer = ClientSerializer([self.clients], many=True)
        self.assertEqual([data], serializer.data)

    def test_create_client(self):
        # Testing CREATE method for creating new client manually.
        # Creating data which will be passed to the view.
        create_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@mail.co',
            'city': 'Novi Sad',
            'country': 'Another country',
            'phone_number': '+38178954321',
            'company': self.company.pk,
            'lead': 'Sales',
            'title': 'CTO',
            'notes': 'John Notes',
            'source': 'Newsletter',
            'lead_owner_name': " ",
        }

        # Checking response's status code.
        response = self.client.post(reverse('clients-list'), create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking the response data.
        data = response.data
        self.assertEqual(data['first_name'], create_data['first_name'])
        self.assertEqual(data['last_name'], create_data['last_name'])
        self.assertEqual(data['email'], create_data['email'])
        self.assertEqual(data['city'], create_data['city'])
        self.assertEqual(data['country'], create_data['country'])
        self.assertEqual(data['phone_number'], create_data['phone_number'])
        self.assertEqual(data['company'], create_data['company'])
        self.assertEqual(data['company_name'], self.company.company)
        self.assertEqual(data['date_created'], f"{date.today():%Y-%m-%d}")
        self.assertEqual(data['lead'], create_data['lead'])
        self.assertEqual(data['title'], create_data['title'])
        self.assertEqual(data['notes'], create_data['notes'])
        self.assertEqual(data['source'], create_data['source'])
        self.assertEqual(data['lead_owner_name'], create_data['lead_owner_name'])

