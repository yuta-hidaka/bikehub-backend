from django.http import Http404
from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment

from rest_framework import generics, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_api_key.permissions import HasAPIKey

from ...serializer.books.book_serializer import AuthorSerializer


class MakerList(generics.ListCreateAPIView):
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class MakerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class EdaList(generics.ListCreateAPIView):
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class EdaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class fuelTypeList(generics.ListCreateAPIView):
    queryset = fuelType.objects.all()
    serializer_class = fuelTypeSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class FuelTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class FcList(generics.ListCreateAPIView):
    queryset = Fc.objects.all()
    serializer_class = FcSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class FcDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fc.objects.all()
    serializer_class = FcSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class FcCommentList(generics.ListCreateAPIView):
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]


class FcCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
    permission_classes = [HasAPIKey &permissions.IsAuthenticatedOrReadOnly]
