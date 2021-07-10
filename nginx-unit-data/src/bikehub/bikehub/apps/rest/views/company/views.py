from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from fuel_consumption.models import *
from rest_framework import filters, generics, permissions, renderers
# views.py
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from company.models import Company, CompanyGroup, CompanyUserGroup, Evaluation

from ...serializer.company import CompanySerializer, CompanyUserGroupSerializer, CompanyGroupSerializer, EvaluationSerializer
from rest.views.custom_permission.is_owner import IsOwnerOrReadOnly


class EvaluationList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class EvaluationDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer


class CompanyUserGroupList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CompanyUserGroup.objects.all()
    serializer_class = CompanyUserGroupSerializer


class CompanyUserGroupDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = CompanyUserGroup.objects.all()
    serializer_class = CompanyUserGroupSerializer


class CompanyGroupList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CompanyGroup.objects.all()
    serializer_class = CompanyUserGroupSerializer


class CompanyGroupDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = CompanyGroup.objects.all()
    serializer_class = CompanyUserGroupSerializer


class CompanyList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    read_only = True
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    