from rest_framework.test import APITestCase
from crm.models import Company
from crm.serializers import CompanySerializer, CompanyListSerializer
from django.urls import reverse
from rest_framework import status
from collections import OrderedDict


class TestCompanyViewSet(APITestCase):
    def setUp(self):
        self.company_1 = Company.objects.create(
            company='Company One',
            city='Novi Sad',
            country='Serbia',
            website='https://companyone.co',
            phone_number='8795479965',
        )
        self.company_2 = Company.objects.create(
            company='Company Two',
            city='Xian',
            country='China',
            website='https://companytwo.co',
            phone_number='8755622222',
        )

    def test_list_companies(self):
        # Testing get method which returns all the companies we have in our db.
        response = self.client.get(reverse('companies-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Getting the data for company_1 and company_2 defined in setUp().
        data_1 = response.data[0]
        data_2 = response.data[1]

        # Checking the values.
        # Company 1.
        self.assertEqual(data_1['company'], self.company_1.company)
        self.assertEqual(data_1['country'], self.company_1.country)
        self.assertEqual(data_1['lead'], self.company_1.lead)
        # Company 2.
        self.assertEqual(data_2['company'], self.company_2.company)
        self.assertEqual(data_2['country'], self.company_2.country)
        self.assertEqual(data_2['lead'], self.company_2.lead)
        # Testing serializer and serializer.data
        serializer = CompanyListSerializer([self.company_1, self.company_2], many=True)
        self.assertEqual(serializer.data, response.data)

    def test_retrieve_companies(self):
        # Testing retrieve method.

        # Checking response status code.
        # Company 1.
        response_1 = self.client.get(reverse('companies-detail', args=[self.company_1.id]))

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(reverse('companies-detail', args=[self.company_1.id]), f'/companies/{self.company_1.id}/')

        # Checking data.
        data_1 = response_1.data
        self.assertEqual(data_1['id'], self.company_1.id)
        self.assertEqual(data_1['company'], self.company_1.company)
        self.assertEqual(data_1['city'], self.company_1.city)
        self.assertEqual(data_1['country'], self.company_1.country)
        self.assertEqual(data_1['website'], self.company_1.website)
        self.assertEqual(data_1['lead'], self.company_1.lead)
        self.assertEqual(data_1['phone_number'], self.company_1.phone_number)
        # Check serializer and serializer data.
        serializer = CompanySerializer([self.company_1], many=True)
        self.assertEqual(serializer.data, [OrderedDict(response_1.data)])

        # Checking response status code.
        # Company 2.
        response_2 = self.client.get(reverse('companies-detail', args=[self.company_2.id]))
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(reverse('companies-detail', args=[self.company_2.id]), f'/companies/{self.company_2.id}/')

        # Checking data.
        data_2 = response_2.data
        self.assertEqual(data_2['id'], self.company_2.id)
        self.assertEqual(data_2['company'], self.company_2.company)
        self.assertEqual(data_2['city'], self.company_2.city)
        self.assertEqual(data_2['country'], self.company_2.country)
        self.assertEqual(data_2['website'], self.company_2.website)
        self.assertEqual(data_2['lead'], self.company_2.lead)
        self.assertEqual(data_2['phone_number'], self.company_2.phone_number)
        # Check serializer and serializer data.
        serializer = CompanySerializer([self.company_2], many=True)
        self.assertEqual(serializer.data, [OrderedDict(response_2.data)])

    def test_create_company(self):
        create_data = {
            'company': 'Company Three',
            'city': 'Belgrade',
            'country': 'Serbia',
            'website': 'https://companythree.co',
            'lead': 'Marketing',
            'phone_number': '+38178954321',
        }
        # Checking the number of companies in the db before creating the new one.
        response = self.client.get(reverse('companies-list'))
        self.assertEqual(len(response.data), 2)

        # Creating the company.
        response = self.client.post(reverse('companies-list'), create_data)

        # Checking status code, number of objects in db and data for the new company.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)

        self.assertEqual(response.data['company'], create_data['company'])
        self.assertEqual(response.data['city'], create_data['city'])
        self.assertEqual(response.data['country'], create_data['country'])
        self.assertEqual(response.data['website'], create_data['website'])
        self.assertEqual(response.data['lead'], create_data['lead'])
        self.assertEqual(response.data['phone_number'], create_data['phone_number'])

    def test_delete_companies(self):
        # Test delete companies.
        # Before deleting, there are 2 companies in the db.
        response = self.client.get(reverse('companies-list'))
        self.assertEqual(len(response.data), 2)

        response = self.client.delete(reverse('companies-detail', args=[self.company_1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # After deleting, there is 1 company in the db.
        response = self.client.get(reverse('companies-list'))
        self.assertEqual(len(response.data), 1)

