from django.test import TestCase
from crm.models import Client, Company, Agent, User
from crm.serializers import ListClientSerializer, ClientSerializer, DownloadFileSerializer
import datetime

# from the project directory run: python manage.py test crm.tests.test_serializers

class TestListClientSerializer(TestCase):

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

        self.client = Client.objects.create(
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

    def test_list_serializer_fields(self):
        # Check ListClientSerializer fields.
        serializer = ListClientSerializer(self.client)
        expected_fields = {
            'first_name',
            'last_name',
            'company_name',
            'title',
            'lead',
            'email',
        }
        self.assertEqual(serializer.get_fields().keys(), expected_fields)

    def test_list_serializer_data(self):
        # Check data from ListClientSerializer.
        serializer = ListClientSerializer(self.client)

        data = serializer.data

        self.assertEqual(data['first_name'], self.client.first_name)
        self.assertEqual(data['last_name'], self.client.last_name)
        self.assertEqual(data['company_name'], self.client.company.company)
        self.assertEqual(data['title'], self.client.title)
        self.assertEqual(data['lead'], self.client.lead)
        self.assertEqual(data['email'], self.client.email)


    def test_client_serializer_fields(self):
        # Check ClientSerializer fields.
        serializer = ClientSerializer(self.client)
        expected_fields = {
            'first_name',
            'last_name',
            'email',
            'city',
            'country',
            'phone_number',
            'company_name',
            'date_created',
            'lead',
            'title',
            'notes',
            'source',
            'lead_owner_name',
        }

        self.assertEqual(serializer.get_fields().keys(), expected_fields)


    def test_client_serializer_data(self):
        # Check data from ClientSerializer.
        serializer = ClientSerializer(self.client)
        data = serializer.data

        self.assertEqual(data['first_name'], self.client.first_name)
        self.assertEqual(data['last_name'], self.client.last_name)
        self.assertEqual(data['email'], self.client.email)
        self.assertEqual(data['city'], self.client.city)
        self.assertEqual(data['country'], self.client.country)
        self.assertEqual(data['phone_number'], self.client.phone_number)
        self.assertEqual(data['company_name'], self.client.company.company)
        self.assertEqual(data['date_created'], f"{datetime.date.today():%Y-%m-%d}")
        self.assertEqual(data['lead'], self.client.lead)
        self.assertEqual(data['title'], self.client.title)
        self.assertEqual(data['notes'], self.client.notes)
        self.assertEqual(data['source'], self.client.source)
        self.assertEqual(data['lead_owner_name'], self.user.username)


    def test_download_file_serializer_fields(self):
        # Check DownloadFileSerializer fields
        serializer = DownloadFileSerializer(self.client)

        expected_fields = {
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'city',
            'country',
            'company_name',
            'title',
            'lead',
        }

        self.assertEqual(serializer.get_fields().keys(), expected_fields)

    def test_download_file_serializer_data(self):
        # Check data from DownloadFileSerializer.
        serializer = DownloadFileSerializer(self.client)

        data = serializer.data

        self.assertEqual(data['first_name'], self.client.first_name)
        self.assertEqual(data['last_name'], self.client.last_name)
        self.assertEqual(data['email'], self.client.email)
        self.assertEqual(data['phone_number'], self.client.phone_number)
        self.assertEqual(data['city'], self.client.city)
        self.assertEqual(data['country'], self.client.country)
        self.assertEqual(data['company_name'], self.client.company.company)
        self.assertEqual(data['title'], self.client.title)
        self.assertEqual(data['lead'], self.client.lead)

