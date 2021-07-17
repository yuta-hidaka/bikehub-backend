from django.contrib import admin
from django.urls import include, path

from .views import (CompanyDetail, CompanyGroupDetail, CompanyGroupList,
                    CompanyList, CompanyUserGroupDetail, CompanyUserGroupList,
                    EvaluationDetail, EvaluationList)

urlpatterns = [

    path('', CompanyList.as_view(), name='company-list'),
    path('<uuid:pk>/', CompanyDetail.as_view(), name='company-detail'),

    path('group/', CompanyGroupList.as_view(), name='company-group-list'),
    path('group/<uuid:pk>/', CompanyGroupDetail.as_view(), name='company-group-detail'),

    path('user/group/', CompanyUserGroupList.as_view(), name='company-user-group-list'),
    path('user/group/<uuid:pk>/', CompanyUserGroupDetail.as_view(), name='company-user-group-detail'),

    path('evaluation/', EvaluationList.as_view(), name='evaluation-list'),
    path('evaluation/<uuid:pk>/', EvaluationDetail.as_view(), name='evaluation-detail'),

]
