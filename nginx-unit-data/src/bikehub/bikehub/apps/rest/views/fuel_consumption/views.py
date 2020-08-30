from django.http import Http404
from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment

from rest_framework import generics, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_api_key.permissions import HasAPIKey
from ...serializer.books.book_serializer import AuthorSerializer
from rest.views.custonm_permission.is_owner import IsOwnerOrReadOnly

class MakerList(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
    


class MakerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
    


class CountryList(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    


class EdaList(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer
    


class EdaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer
    


class BikeList(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    


class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    


class fuelTypeList(generics.ListCreateAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = fuelType.objects.all()
    serializer_class = fuelTypeSerializer
    


class FuelTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAdminUser]
    read_only=True 
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    


class FcList(generics.ListCreateAPIView):
    permission_classes =[IsOwnerOrReadOnly]
    read_only=True 
    queryset = Fc.objects.all()
    serializer_class = FcSerializer
    


class FcDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsOwnerOrReadOnly]
    read_only=True 
    queryset = Fc.objects.all()
    serializer_class = FcSerializer
    


class FcCommentList(generics.ListCreateAPIView):
    permission_classes =[IsOwnerOrReadOnly]
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
    


class FcCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsOwnerOrReadOnly]
    read_only=True 
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
    
