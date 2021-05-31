from django.test import TestCase
from crm.models import Client, Company, Agent, User
import datetime


class TestModels(TestCase):
    """Testing models."""

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

    def test_company(self):
        # Testing Company model fields.
        self.assertEqual(self.company.company, "Company Name")
        self.assertEqual(self.company.city, "Some City")
        self.assertEqual(self.company.country, "Country")
        self.assertEqual(self.company.website, "https://somecompany.co")
        self.assertEqual(self.company.lead, "Marketing")
        self.assertEqual(self.company.phone_number, "+54789546")

    def test_agent(self):
        # Testing Agent model field.
        self.assertEqual(self.agent.user.username, "jelena")

    def test_client(self):
        # Testing Client model fields.
        self.assertEqual(self.client.first_name, "Jane")
        self.assertEqual(self.client.last_name, "Doe")
        self.assertEqual(self.client.email, "jane@mail.co")
        self.assertEqual(self.client.city, "City")
        self.assertEqual(self.client.country, "Country")
        self.assertEqual(self.client.phone_number, "+5478966555")
        self.assertEqual(self.client.company.company, self.company.company)
        self.assertEqual(self.client.lead, "Marketing")
        self.assertEqual(self.client.title, "CEO")
        self.assertEqual(self.client.source, "YouTube")
        self.assertEqual(self.client.notes, "Some Note")
        self.assertEqual(self.client.lead_owner.user, self.user)
        self.assertEqual(self.client.date_created, datetime.date.today())
