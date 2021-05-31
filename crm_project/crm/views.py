from .serializers import ListClientSerializer, ClientSerializer, DownloadFileSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Client
from rest_framework.views import APIView
from drf_renderer_xlsx.renderers import XLSXRenderer
from drf_renderer_xlsx.mixins import XLSXFileMixin
from rest_framework.decorators import action
from .renderers import MyCSVRenderer
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.shortcuts import render
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ClientViewSet(XLSXFileMixin, viewsets.ModelViewSet):
    """The viewset that lists, edits, creates and deletes the client."""
    queryset = Client.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name', 'lead_owner__user__username', 'company')


    def get_queryset(self, *args, **kwargs):
        if self.request.query_params == {}:
            queryset = Client.objects.all()
        else:
            name = self.request.query_params.get('first_name')
            queryset = Client.objects.filter(first_name=name)
        return queryset

    def get_serializer_class(self):
        # Depending on an self.action, we are returning different serializer_class.
        if self.action in ['create', 'update', 'partial update', 'retrieve']:
            return ClientSerializer
        elif self.action in ['download_xlsx', 'download_csv']:
            return DownloadFileSerializer
        return ListClientSerializer

    @action(
        methods=['GET'],
        detail=False,
        filter_backends=(DjangoFilterBackend,),
        renderer_classes =(XLSXRenderer, ),
        filename='client_list.xlsx',

    )
    def download_xlsx(self, request, *args, **kwargs):
        """Method for downloading xlsx file. It downloads the list of all clients."""
        # filter needs to be provided to url like:
        # ?first_name=Jane&last_name=&lead_owner__user__username=&company=
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer_class()

        data = serializer(filtered_queryset, many=True).data
        response = Response(data)
        return response

    @action(
        detail=False,
        url_path='download_csv',
        renderer_classes = (MyCSVRenderer,),
    )
    def download_csv(self, *args, **kwargs):
        """Method for downloading csv file. It downloads the list of all clients."""
        clients = self.queryset
        content = [{
            'First Name': client.first_name,
            'Last Name': client.last_name,
            'Email': client.email,
            'Phone': client.phone_number,
            'City': client.city,
            'Country':client.country,
            'Company': client.company,
            'Title': client.title,
            'Lead': client.lead,
        } for client in clients]
        response = Response(content)
        response['content-disposition'] = "attachment; filename='my_file.csv'"
        return response

#
# class HomepageViewSet(viewsets.ViewSet):
#     """Viewset for listing existing clients."""
#
#     def list(self, request):
#         queryset = Client.objects.all()
#         serializer = ListClientSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Client.objects.all()
#         client = get_object_or_404(queryset, pk=pk)
#         serializer = ClientSerializer(client)
#         return Response(serializer.data)
#
#
#
# class FilterClientView(ListAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['first_name', 'last_name', 'lead_owner__user__username']












