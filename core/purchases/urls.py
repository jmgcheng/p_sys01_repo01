from django.urls import path
from purchases.views import PurchaseRequestCreateView, PurchaseRequestUpdateView

app_name = 'purchases'

urlpatterns = [

    path('requests/create/', PurchaseRequestCreateView.as_view(),
         name='purchase-request-create'),


    path('requests/<int:pk>/update/', PurchaseRequestUpdateView.as_view(),
         name='purchase-request-update'),

    # path('create/', ProductCreateView.as_view(), name='product-create'),
    # path('variations/create/', ProductVariationCreateView.as_view(),
    #      name='product-variation-create'),

    # path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # path('variations/<int:pk>/', ProductVariationDetailView.as_view(),
    #      name='product-variation-detail'),

    # path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    # path('variations/<int:pk>/update/',
    #      ProductVariationUpdateView.as_view(), name='product-variation-update'),

    # path('ajx_product_list/', ajx_product_list, name='ajx_product_list'),
    # path('variations/ajx_product_variation_list/',
    #      ajx_product_variation_list, name='ajx_product_variation_list'),

    # path('', ProductListView.as_view(), name='product-list'),
    # path('variations/', ProductVariationListView.as_view(),
    #      name='product-variation-list'),
]
