from django.urls import path
from purchases.views import PurchaseRequestCreateView, PurchaseRequestUpdateView, PurchaseRequestListView, PurchaseRequestDetailView, PurchaseRequestApproveView, PurchaseReceiveCreateView, PurchaseReceiveUpdateView, PurchaseReceiveDetailView, PurchaseReceiveListView, ajx_purchase_request_list, ajx_purchase_receive_list

app_name = 'purchases'

urlpatterns = [

    path('requests/create/', PurchaseRequestCreateView.as_view(),
         name='purchase-request-create'),

    path('receives/create/', PurchaseReceiveCreateView.as_view(),
         name='purchase-receive-create'),

    path('requests/<int:pk>/update/', PurchaseRequestUpdateView.as_view(),
         name='purchase-request-update'),

    path('receives/<int:pk>/update/', PurchaseReceiveUpdateView.as_view(),
         name='purchase-receive-update'),


    # path('create/', ProductCreateView.as_view(), name='product-create'),
    # path('variations/create/', ProductVariationCreateView.as_view(),
    #      name='product-variation-create'),

    # path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('requests/<int:pk>/', PurchaseRequestDetailView.as_view(),
         name='purchase-request-detail'),

    path('receives/<int:pk>/', PurchaseReceiveDetailView.as_view(),
         name='purchase-receive-detail'),


    path('requests/<int:pk>/approve/', PurchaseRequestApproveView.as_view(),
         name='purchase-request-approve'),

    # path('variations/<int:pk>/', ProductVariationDetailView.as_view(),
    #      name='product-variation-detail'),

    # path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    # path('variations/<int:pk>/update/',
    #      ProductVariationUpdateView.as_view(), name='product-variation-update'),

    # path('ajx_product_list/', ajx_product_list, name='ajx_product_list'),

    path('requests/ajx_purchase_request_list/',
         ajx_purchase_request_list, name='ajx_purchase_request_list'),

    path('receives/ajx_purchase_receive_list/',
         ajx_purchase_receive_list, name='ajx_purchase_receive_list'),



    # path('variations/ajx_product_variation_list/',
    #      ajx_product_variation_list, name='ajx_product_variation_list'),

    # path('', ProductListView.as_view(), name='product-list'),

    path('requests/', PurchaseRequestListView.as_view(),
         name='purchase-request-list'),


    path('receives/', PurchaseReceiveListView.as_view(),
         name='purchase-receive-list'),



    # path('variations/', ProductVariationListView.as_view(),
    #      name='product-variation-list'),
]
