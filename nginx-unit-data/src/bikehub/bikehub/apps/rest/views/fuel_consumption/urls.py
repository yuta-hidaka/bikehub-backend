from django.contrib import admin
from django.urls import path, include
from .views import (
 MakerList,
 MakerDetail,
 CountryList,
 CountryDetail,
 BikeList,
 BikeDetail,
 FuelTypeList,
 FuelTypeDetail,
 FcList,
 FcDetail,
 FcCommentList,
 FcCommentDetail,
)

urlpatterns = [
    # ---------------------------------------------------------
    path(
        'maker',
        MakerList.as_view(),
        name='maker-list'
    ),
    path(
        'maker/<uuid:pk>/',
        MakerDetail.as_view(),
        name='maker-detail'
    ),
    # ---------------------------------------------------------
    path(
        'country/',
        CountryList.as_view(),
        name='country-list'
    ),
    path(
        'country/<uuid:pk>/',
        CountryDetail.as_view(),
        name='country-detail'
    ),
    # ---------------------------------------------------------
    path(
        '',
        BikeList.as_view(),
        name='bike-list'
    ),
    path(
        '<uuid:pk>/',
        BikeDetail.as_view(),
        name='bike-detail'
    ),
    # ---------------------------------------------------------
    path(
        'fuel-type/',
        FuelTypeList.as_view(),
        name='fuel-type-list'
    ),
    # ---------------------------------------------------------
    path(
        'fc/',
        FcList.as_view(),
        name='fc-list'
    ),
    path(
        'fc/<uuid:pk>/',
        FcDetail.as_view(),
        name='fc-detail'
    ),
    # ---------------------------------------------------------
    path(
        'fc/comment/',
        FcCommentList.as_view(),
        name='fc-comment-list'
    ),
    path(
        'fc/comment/<uuid:pk>/',
        FcCommentDetail.as_view(),
        name='fx-comment-detail'
    )
    # ---------------------------------------------------------
]
