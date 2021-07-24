from django.test import TestCase
from crm.models import Client, Company, Agent, User, Tasks
from crm.serializers import ListClientSerializer, \
    ClientSerializer, DownloadFileSerializer, CompanySerializer, \
    CompanyListSerializer, TaskListSerializer, TaskDetailSerializer
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
            'company',
            'company_name',
            'date_created',
            'lead',
            'title',
            'notes',
            'source',
            'lead_owner_name',
            'lead_owner',
        }

        self.assertEqual(serializer.get_fields().keys(), expected_fields)


    def test_client_serializer_data(self):
        # Check data from ClientSerializer.
        serializer = ClientSerializer(self.client)
        data = serializer.data

        self.assertEqual(len(data), 15)
        self.assertEqual(data['first_name'], self.client.first_name)
        self.assertEqual(data['last_name'], self.client.last_name)
        self.assertEqual(data['email'], self.client.email)
        self.assertEqual(data['city'], self.client.city)
        self.assertEqual(data['country'], self.client.country)
        self.assertEqual(data['phone_number'], self.client.phone_number)
        self.assertEqual(data['company'], self.company.id)
        self.assertEqual(data['company_name'], self.client.company.company)
        self.assertEqual(data['date_created'], f"{datetime.date.today():%Y-%m-%d}")
        self.assertEqual(data['lead'], self.client.lead)
        self.assertEqual(data['title'], self.client.title)
        self.assertEqual(data['notes'], self.client.notes)
        self.assertEqual(data['source'], self.client.source)
        self.assertEqual(data['lead_owner_name'], self.user.username)
        self.assertEqual(data['lead_owner'], self.agent.id)


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


class TestCompanySerializer(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            company="Company One",
            city="Novi Sad",
            country="Serbia",
            website="https://companyone.co",
            lead="Marketing",
            phone_number="54789546",
            )

    def test_company_list_serializer(self):
        # Testing fields and data of CompanyListSerializer.
        serializer = CompanyListSerializer(self.company)

        expected_fields = {
            'company',
            'country',
            'lead',
        }

        self.assertEqual(serializer.get_fields().keys(), expected_fields)

        data = serializer.data

        self.assertEqual(data['company'], self.company.company)
        self.assertEqual(data['country'], self.company.country)
        self.assertEqual(data['lead'], self.company.lead)

    def test_company_serializer(self):
        # Testing fields and data of CompanySerializer.
        serializer = CompanySerializer(self.company)

        expected_fields = {
            'id',
            'company',
            'city',
            'country',
            'website',
            'lead',
            'phone_number',
        }
        self.assertEqual(serializer.get_fields().keys(), expected_fields)

        data = serializer.data

        self.assertEqual(data['id'], self.company.id)
        self.assertEqual(data['company'], self.company.company)
        self.assertEqual(data['city'], self.company.city)
        self.assertEqual(data['country'], self.company.country)
        self.assertEqual(data['website'], self.company.website)
        self.assertEqual(data['lead'], self.company.lead)
        self.assertEqual(data['phone_number'], self.company.phone_number)


class TestTasksSerializer(TestCase):
    """Test Case for testing Task's serializers."""
    def setUp(self):

        self.user = User.objects.create(username="jelena")
        self.agent = Agent.objects.create(user=self.user)
        self.task = Tasks.objects.create(
            headline="Test Task",
            body="Body of the Test Task",
            owner=self.agent,
        )

    def test_task_list_serializer(self):
        # Testing fields and data of TaskListSerializer.
        serializer = TaskListSerializer(self.task)
        expected_fields = {
            'headline',
            'task_owner_name',
            'progress',
        }
        self.assertEqual(serializer.get_fields().keys(), expected_fields)

        data = serializer.data

        self.assertEqual(data['headline'], self.task.headline)
        self.assertEqual(data['task_owner_name'], self.task.owner.user.username)
        self.assertEqual(data['progress'], "Opened")

    def test_task_detail_serializer(self):
        # Testing fields and data of TaskDetailSerializer.
        serializer = TaskDetailSerializer(self.task)
        expected_fields = {
            'headline',
            'body',
            'task_owner_name',
            'owner',
            'progress',
            'date_created',
        }
        self.assertEqual(serializer.get_fields().keys(), expected_fields)

        data = serializer.data

        self.assertEqual(len(data), 6)
        self.assertEqual(data['headline'], self.task.headline)
        self.assertEqual(data['body'], self.task.body)
        self.assertEqual(data['owner'], self.task.owner.id)
        self.assertEqual(data['task_owner_name'], self.task.owner.user.username)
        self.assertEqual(data['progress'], 'Opened')
        self.assertEqual(data['date_created'], f"{datetime.date.today():%Y-%m-%d}")