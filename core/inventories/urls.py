from django.urls import path
from inventories.views import InventoryAddCreateView, InventoryAddUpdateView, InventoryAddDetailView, InventoryAddListView, ajx_inventory_add_list

app_name = 'inventories'

urlpatterns = [

    path('adds/create/', InventoryAddCreateView.as_view(),
         name='inventory-add-create'),

    path('adds/<int:pk>/update/', InventoryAddUpdateView.as_view(),
         name='inventory-add-update'),

    path('adds/<int:pk>/', InventoryAddDetailView.as_view(),
         name='inventory-add-detail'),

    path('adds/', InventoryAddListView.as_view(),
         name='inventory-add-list'),

    path('adds/ajx_inventory_add_list/',
         ajx_inventory_add_list, name='ajx_inventory_add_list'),

]
