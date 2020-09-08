from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment
from rest_framework import generics
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ...serializer.fuel_consumption import *
from rest.views.custom_permission.is_owner import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
import json
from django.db.models import Q
from django.db.models import Avg, F, Max, Min
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core import serializers


@csrf_exempt
def get_fc_detail(request):
    if request.method == 'POST':
        fc_ave = 0
        fc_max = 0
        fc_min = 0
        fc_max_user = None

        request_json = json.loads(request.body)
        bike_id = request_json.get("bike_id", None)
        user_id = request_json.get("user_id", None)
        model_year = request_json.get("model_year", None)

        if bike_id is None:
            return HttpResponse('Unauthorized', status=401)

        query = Q(bike_id=bike_id)

        if user_id:
            query.add(Q(user_id=user_id), Q.AND)

        if model_year:
            query.add(Q(model_year=model_year), Q.AND)

        q = Fc.objects.filter(query).order_by('-fc').all()

        fc_min = (q.values('fc', 'user__disp_name').aggregate(
            min=Min('fc'),
        ))

        fc_avg = (q.values('fc', 'user__disp_name').aggregate(
            avg=Avg('fc'),
        ))

        fc_max = (q.values('fc').aggregate(
            max=Max('fc'),
        ))

        try:
            fc_max_user = (q.values('user__disp_name').first())
        except Exception as e:
            fc_max_user = f'{e}'

        response_data = {}
        response_data["fc_min"] = fc_min
        response_data["fc_avg"] = fc_avg
        response_data["fc_max"] = fc_max
        response_data["fc_max_user"] = fc_max_user

        return JsonResponse(response_data)
    return HttpResponse('Unauthorized', status=401)


class MakerList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer


class MakerDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer


class CountryList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class EdaList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer


class EdaDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Eda.objects.all()
    serializer_class = EdaSerializer


class BikeList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class BikeDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class FuelTypeList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    read_only = True
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer


class FuelTypeDetail(generics.RetrieveUpdateAPIView):
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


class FcCommentDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = FcComment.objects.all()
    serializer_class = FcCommentSerializer
