from django.urls import path
from products.views import ProductListCreateViewApi, ProductRetrieveUpdateDestroyViewApi

app_name = 'api'

urlpatterns = [

    path('products/', ProductListCreateViewApi.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyViewApi.as_view()),

]
