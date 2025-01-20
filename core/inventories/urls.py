from django.urls import path
from inventories.views import InventoryAddCreateView, InventoryAddUpdateView, InventoryAddDetailView, InventoryAddListView, InventoryDeductCreateView, InventoryDeductUpdateView, InventoryDeductDetailView, InventoryDeductListView, ajx_inventory_add_list, ajx_inventory_deduct_list

app_name = 'inventories'

urlpatterns = [

    path('adds/create/', InventoryAddCreateView.as_view(),
         name='inventory-add-create'),

    path('deducts/create/', InventoryDeductCreateView.as_view(),
         name='inventory-deduct-create'),

    path('adds/<int:pk>/update/', InventoryAddUpdateView.as_view(),
         name='inventory-add-update'),

    path('deducts/<int:pk>/update/', InventoryDeductUpdateView.as_view(),
         name='inventory-deduct-update'),

    path('adds/<int:pk>/', InventoryAddDetailView.as_view(),
         name='inventory-add-detail'),

    path('deducts/<int:pk>/', InventoryDeductDetailView.as_view(),
         name='inventory-deduct-detail'),

    path('adds/', InventoryAddListView.as_view(),
         name='inventory-add-list'),

    path('deducts/', InventoryDeductListView.as_view(),
         name='inventory-deduct-list'),

    path('adds/ajx_inventory_add_list/',
         ajx_inventory_add_list, name='ajx_inventory_add_list'),

    path('deducts/ajx_inventory_deduct_list/',
         ajx_inventory_deduct_list, name='ajx_inventory_deduct_list'),

]
