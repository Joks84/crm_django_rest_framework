from rest_framework import serializers
from .models import Client, Company


class ListClientSerializer(serializers.ModelSerializer):
    """Serializer used for just showing/listing the clients."""

    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'company_name', 'title', 'lead', 'email']

    def get_company_name(self, client: Client):
        # Getting the company name, and not pk.
        if company_name := client.company:
            return company_name.company
        else:
            return " "


class ClientSerializer(serializers.ModelSerializer):
    """Serializer used for creating, updating, retrieving clients' data."""

    lead_owner_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
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
        ]

    def get_lead_owner_name(self, client):
        if lead_owner_name := client.lead_owner:
            return lead_owner_name.user.username
        else:
            return " "

    def get_company_name(self, client: Client):
        """
        In case there is no company attached to a client, return empty string.
        If there is, return full name instead of a pk.
        """
        if company_name := client.company:
            return company_name.company
        else:
            return " "


class DownloadFileSerializer(serializers.ModelSerializer):
    """Serializer for downloading XLSX and CSV files."""
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'city',
            'country',
            'company_name',
            'title',
            'lead',
        ]

    def get_company_name(self, client):
        """
        In case there is no company attached to a client, return empty string.
        If there is, return full name instead of a pk.
        """
        if company_name := client.company:
            return company_name.company
        else:
            return " "

