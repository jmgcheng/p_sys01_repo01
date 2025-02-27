from rest_framework import serializers
from inventories.utils import (
    get_quantity_inventory_add_subquery,
    get_quantity_inventory_deduct_subquery,
    get_quantity_purchasing_subquery,
    get_quantity_purchasing_receive_subquery,
    get_quantity_sale_releasing_subquery,
    get_quantity_sold_subquery
)
from products.models import ProductVariation


class InventorySummarySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    qty_manual_add = serializers.IntegerField(
        source='quantity_manual_add_annotated', read_only=True)
    qty_manual_deduct = serializers.IntegerField(
        source='quantity_manual_deduct_annotated', read_only=True)
    qty_purchasing = serializers.IntegerField(
        source='quantity_purchasing_annotated', read_only=True)
    qty_purchasing_receive = serializers.IntegerField(
        source='quantity_purchasing_receive_annotated', read_only=True)
    qty_sale_releasing = serializers.IntegerField(
        source='quantity_sale_releasing_annotated', read_only=True)
    qty_sold = serializers.IntegerField(
        source='quantity_sold_annotated', read_only=True)
    qty_on_hand = serializers.IntegerField(
        source='quantity_on_hand_annotated', read_only=True)

    class Meta:
        model = ProductVariation
        fields = ('id', 'code', 'name', 'product_name',
                  'qty_manual_add', 'qty_manual_deduct', 'qty_purchasing',
                  'qty_purchasing_receive', 'qty_sale_releasing', 'qty_sold', 'qty_on_hand')
