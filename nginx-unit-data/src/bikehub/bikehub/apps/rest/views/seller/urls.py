from django.urls import path

from .views import (ProductCommentsDetail, ProductCommentsList,
                    ProductImagesDetail, ProductImagesList, ProductsDetail,
                    ProductsList)

urlpatterns = [
    path('products', ProductsList.as_view(), name='product-list'),
    path('product/<uuid:pk>/', ProductsDetail.as_view(), name='product-detail'),

    path('product/comments', ProductCommentsList.as_view(), name='product-comment-list'),
    path('product/comment/<uuid:pk>/', ProductCommentsDetail.as_view(), name='product-comment-detail'),

    path('product/images', ProductImagesList.as_view(), name='product-image-list'),
    path('product/image/<uuid:pk>/', ProductImagesDetail.as_view(), name='product-image-detail'),
]
