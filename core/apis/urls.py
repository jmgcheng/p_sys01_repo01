from django.urls import path
from products.views import ProductListCreateViewApi

app_name = 'api'

urlpatterns = [

    path('products/', ProductListCreateViewApi.as_view()),

]
