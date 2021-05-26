from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
# views.py
from rest_framework.permissions import IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey

from news.models import (MainCategoryTag, News, SubCategoryTag,
                         SubCategoryTagMap)

from ...serializer.news import (MainCategoryTagSerializer, NewsIdSerializer,
                                NewsSerializer, SubCategoryTagMapSerializer,
                                SubCategoryTagSerializer)


class NewsList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    serializer_class = NewsSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = [
        'news_id',
        'title',
        'sub_category_tag_map__sub_category_tag__name'
    ]
    filter_fields = {
        'sub_category_tag_map__sub_category_tag__main_category_tag_id': ['exact'],
    }
    ordering_fields = [
        'created_at',
        'title',
    ]

    def get_queryset(self):

        main_tag = self.request.query_params\
            .get('sub_category_tag_map__sub_category_tag__main_category_tag_id', None)

        if main_tag:
            queryset = News.objects.filter(
                sub_category_tag_map__sub_category_tag__main_category_tag_id=main_tag,
                show=True
            ).distinct()
        else:
            queryset = News.objects.filter(show=True).all()

        return queryset


class NewsIdList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = News.objects.all()
    serializer_class = NewsIdSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['news_id']


class NewsDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['news_id', 'title']


class MainCategoryTagList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = MainCategoryTag.objects.all()
    serializer_class = MainCategoryTagSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = ['name', 'main_category_tag_id']
    filter_fields = {
        'is_active': ['exact'],
    }


class MainCategoryTagDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = MainCategoryTag.objects.all()
    serializer_class = MainCategoryTagSerializer

    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']

    def partial_update(self, request, pk, *args, **kwargs):
        q = MainCategoryTag.objects.get(
            pk=pk
        )
        q.push_counter = q.push_counter + 1
        q.save()
        return HttpResponse(status=201)


class SubCategoryTagList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = SubCategoryTag.objects.all()
    serializer_class = SubCategoryTagSerializer

    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']


class SubCategoryTagDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = SubCategoryTag.objects.all()
    serializer_class = SubCategoryTagSerializer

    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']


class SubCategoryTagMapList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = SubCategoryTagMap.objects.all()
    serializer_class = SubCategoryTagMapSerializer

    filter_backends = [filters.SearchFilter]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'sub_category_tag__main_category_tag_id',
        'news__title'
    ]
    ordering_fields = [
        'news__created_at'
    ]
    filter_fields = {
        'news__title': ['gte', 'lt', 'contains', 'exact'],
        'sub_category_tag__main_category_tag_id': ['exact'],
    }


class SubCategoryTagMapDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    read_only = True
    queryset = SubCategoryTagMap.objects.all()
    serializer_class = SubCategoryTagMapSerializer

    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']


# from rest_framework import generics, renderers, filters
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from restaurant.models import *
# from ...serializer.serializer_restaulant import *
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import permissions
# from ...permissions import IsOwnerOrReadOnly

# # -----------------------------------------------------------------------


# class PrefectureList(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Prefecture.objects.all()
#     serializer_class = PrefectureSerializer


# # class PrefectureDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
# #     queryset = Prefecture.objects.all()
# #     serializer_class = PrefectureSerializer


# # -----------------------------------------------------------------------
# class MunicipalitiesList(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Municipalities.objects.all()
#     serializer_class = MunicipalitiesSerializer


# # class MunicipalitiesDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
# #     queryset = Municipalities.objects.all()
# #     serializer_class = MunicipalitiesSerializer


# # -----------------------------------------------------------------------
# class StreetNameList(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = StreetName.objects.all()
#     serializer_class = StreetNameSerializer


# # class StreetNameDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
# #     queryset = StreetName.objects.all()
# #     serializer_class = StreetNameSerializer


# # -----------------------------------------------------------------------
# class AddressList(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer


# # class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
# #     queryset = Address.objects.all()
# #     serializer_class = AddressSerializer


# # -----------------------------------------------------------------------
# class RestaurantList(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = [
#         'name', 'owner', 'address__prefecture__name', 'address__municipalities__name',
#         'comment', 'benefits', 'email', 'limit_to'
#     ]
#     # filterset_fields = [
#     filter_fields = [
#         'name', 'owner', 'address__prefecture', 'user', 'limit_to'
#     ]
#     ordering_fields = [
#         'name', 'owner', 'address__prefecture', 'user', 'created_at', 'limit_to'
#     ]
#     filter_backends = [
#         DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
#     ]
#     ordering = ['-created_at']
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer


# class RestaurantListReadOnly(generics.ListCreateAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     search_fields = [
#         'name', 'owner', 'address__prefecture__name', 'address__municipalities__name',
#         'comment', 'benefits', 'email', 'limit_to'
#     ]
#     # filterset_fields = [
#     # filter_fields = [

#     #     'name', 'owner', 'address__prefecture', 'user', 'restaurant', 'limit_to'
#     # ]
#     ordering_fields = [
#         'name', 'owner', 'address__prefecture', 'user', 'created_at', 'limit_to'
#     ]
#     filter_backends = [
#         DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
#     ]
#     filter_fields = {
#         'limit_to':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'lt', 'contains', 'exact'],
#         'name':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'exact'],
#         'owner':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'exact'],
#         'address__prefecture':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'exact'],
#         'user':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'exact'],
#         'restaurant_id':
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True ['gte', 'exact'],
#     }
#     ordering = ['-created_at']
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantReadOnlySerializer


# class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes =[IsAdminUser|HasAPIKey]
    # read_only=True
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#
#         permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
#     ]
