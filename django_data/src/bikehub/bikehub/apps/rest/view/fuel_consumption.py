from django.http import Http404

from fuel_consumption.models import *
from rest_framework import generics, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ...serializer.books.book_serializer import AuthorSerializer


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
