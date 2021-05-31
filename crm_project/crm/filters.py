from django_filters import FilterSet
from .models import Client

class ClientFilter(FilterSet):

    class Meta:
        model = Client
        fields = ['first_name', 'company', 'lead_owner__user__username']