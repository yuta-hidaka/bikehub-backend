from django.contrib import admin
from django.urls import include, path

from .views import (MainCategoryTagDetail, MainCategoryTagList, NewsDetail,
                    NewsIdList, NewsList, SubCategoryTagDetail,
                    SubCategoryTagList, SubCategoryTagMapDetail,
                    SubCategoryTagMapList)

urlpatterns = [
    # ---------------------------------------------------------
    path(
        'ids',
        NewsIdList.as_view(),
        name='news-id-list'
    ),
    path(
        '',
        NewsList.as_view(),
        name='news-list'
    ),
    path(
        '<uuid:pk>/',
        NewsDetail.as_view(),
        name='news-detail'
    ),
    # ---------------------------------------------------------
    path(
        'mainTags/',
        MainCategoryTagList.as_view(),
        name='main-tag-list'
    ),
    path(
        'mainTags/<uuid:pk>/',
        MainCategoryTagDetail.as_view(),
        name='main-tag-detail'
    ),
    # ---------------------------------------------------------
    path(
        'subTags/',
        SubCategoryTagList.as_view(),
        name='sub-tag-list'
    ),
    # path(
    #     'Municipalities/<uuid:pk>/',
    #     MunicipalitiesDetail.as_view(),
    #     name='municipalities-detail'
    # ),
    # ---------------------------------------------------------
    path(
        'subTagsMap/',
        SubCategoryTagMapList.as_view(),
        name='sub-tag-map-list'
    ),
    # path(
    #     'street-name/<uuid:pk>/',
    #     StreetNameDetail.as_view(),
    #     name='street-name-detail'
    # ),
    # ---------------------------------------------------------
    # path(
    #     'address/',
    #     AddressList.as_view(),
    #     name='address-list'
    # ),
    # path(
    #     'zip-code/<uuid:pk>/',
    #     AddressDetail.as_view(),
    #     name='zip-code-detail'
    # ),
    # ---------------------------------------------------------
]
