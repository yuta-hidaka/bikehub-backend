from rest.views.custom_permission.product_editable import \
    ProductEditableOrReadOnly
from rest_framework import generics

from seller.models import ProductComments, ProductImages, Products

from ...serializer.seller import (ProductCommentsSerializer,
                                  ProductImagesSerializer, ProductsSerializer)


class ProductsList(generics.ListCreateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProductsDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    read_only = True
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProductImagesList(generics.ListCreateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer


class ProductImagesDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    read_only = True
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer


class ProductCommentsList(generics.ListCreateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    queryset = ProductComments.objects.all()
    serializer_class = ProductCommentsSerializer


class ProductCommentsDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [ProductEditableOrReadOnly]
    read_only = True
    queryset = ProductComments.objects.all()
    serializer_class = ProductCommentsSerializer
