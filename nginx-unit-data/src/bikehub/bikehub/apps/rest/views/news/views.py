from fuel_consumption.models import *
from rest_framework import generics, renderers,permissions,filters
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
# views.py
from rest_framework_api_key.permissions import HasAPIKey
from news.models import News, MainCategoryTag, SubCategoryTag, SubCategoryTagMap
from ...serializer.news import NewsSerializer, MainCategoryTagSerializer, SubCategoryTagSerializer, SubCategoryTagMapSerializer


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['news_id', 'title']
    
class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['news_id', 'title']

class MainCategoryTagList(generics.ListCreateAPIView):
    queryset = MainCategoryTag.objects.all()
    serializer_class = MainCategoryTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'main_category_tag_id']

class MainCategoryTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MainCategoryTag.objects.all()
    serializer_class = MainCategoryTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']

class SubCategoryTagList(generics.ListCreateAPIView):
    queryset = SubCategoryTag.objects.all()
    serializer_class = SubCategoryTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']

class SubCategoryTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoryTag.objects.all()
    serializer_class = SubCategoryTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    # search_fields = ['username', 'email']

class SubCategoryTagMapList(generics.ListCreateAPIView):
    queryset = SubCategoryTagMap.objects.all()
    serializer_class = SubCategoryTagMapSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    filter_backends = [filters.SearchFilter]
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
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

class SubCategoryTagMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoryTagMap.objects.all()
    serializer_class = SubCategoryTagMapSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
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
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Prefecture.objects.all()
#     serializer_class = PrefectureSerializer


# # class PrefectureDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Prefecture.objects.all()
# #     serializer_class = PrefectureSerializer


# # -----------------------------------------------------------------------
# class MunicipalitiesList(generics.ListCreateAPIView):
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Municipalities.objects.all()
#     serializer_class = MunicipalitiesSerializer


# # class MunicipalitiesDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Municipalities.objects.all()
# #     serializer_class = MunicipalitiesSerializer


# # -----------------------------------------------------------------------
# class StreetNameList(generics.ListCreateAPIView):
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = StreetName.objects.all()
#     serializer_class = StreetNameSerializer


# # class StreetNameDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = StreetName.objects.all()
# #     serializer_class = StreetNameSerializer


# # -----------------------------------------------------------------------
# class AddressList(generics.ListCreateAPIView):
#     search_fields = '__all__'
#     filter_fields = '__all__'
#     filterset_fields = '__all__'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer


# # class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Address.objects.all()
# #     serializer_class = AddressSerializer


# # -----------------------------------------------------------------------
# class RestaurantList(generics.ListCreateAPIView):
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
#         'limit_to': ['gte', 'lt', 'contains', 'exact'],
#         'name': ['gte', 'exact'],
#         'owner': ['gte', 'exact'],
#         'address__prefecture': ['gte', 'exact'],
#         'user': ['gte', 'exact'],
#         'restaurant_id': ['gte', 'exact'],
#     }
#     ordering = ['-created_at']
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantReadOnlySerializer


# class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
#     ]
