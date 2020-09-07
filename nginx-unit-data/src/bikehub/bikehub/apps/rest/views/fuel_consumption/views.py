from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment
from rest_framework import generics
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ...serializer.fuel_consumption import *
from rest.views.custom_permission.is_owner import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
import json
from fuel_consumption.models import Fc
from django.db.models import Q
from django.db.models import Min, Max, Avg
from django.http import HttpResponse, Http404


def get_fc_detail(request):
    if request.method == 'GET':
        fc_ave = 0
        fc_max = 0
        fc_min = 0
        fc_max_user = None

        request_json = json.loads(request.body)
        bike_id = request_json.get("bike_id", default=None)
        user_id = request_json.get("user_id", default=None)
        model_year = request_json.get("model_year", default=None)

        if bike_id is None:
            return Http404

        query = Q(bike_id=bike_id)

        if user_id:
            query.add(Q(user_id=user_id), Q.AND)

        if model_year:
            query.add(Q(model_year=model_year), Q.AND)

        queryset = Fc.objects.filter(query)

        avg_min = list(queryset.annotate(
            min=Min('fc'),
            avg=Avg('fc'),
        ))

        fc_max = list(queryset.order_by('fc').first())

        response_data = {
            avg_min: avg_min,
            fc_max: fc_max
        }

        return HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            content_type="application/json"
        )
    return Http404


class MakerList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer


class MakerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer


class CountryList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class EdaList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer


class EdaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer


class BikeList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class FuelTypeList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer


class FuelTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer


class FcList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = Fc.objects.all()
    serializer_class = FcSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'bike',
    ]
    filter_fields = {
        'bike': ['exact'],
        'bike__maker': ['exact'],
        'bike__maker__country': ['exact'],
        'user': ['exact'],
        'fuel_type': ['exact'],
    }
    ordering_fields = [
        'created_at',
        'model_year',
        'fc'
    ]


class FcDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = Fc.objects.all()
    serializer_class = FcSerializer


class FcCommentList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer


class FcCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
