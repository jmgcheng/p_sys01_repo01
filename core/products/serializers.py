from products.models import Product, ProductVariation, ProductUnit, ProductSize, ProductColor
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'


# ProductVariationSerializer for id for POST/PUT and more information for GET
    #  another solution is to create a different serialization for POST/PUT and GET
class ProductVariationSerializer(serializers.ModelSerializer):
    # Use ID-based fields for writing (POST/PUT)
    # this will force id base for POST/PUT verb
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True)
    unit = serializers.PrimaryKeyRelatedField(
        queryset=ProductUnit.objects.all(), write_only=True)
    size = serializers.PrimaryKeyRelatedField(queryset=ProductSize.objects.all(
    ), allow_null=True, required=False, write_only=True)
    color = serializers.PrimaryKeyRelatedField(queryset=ProductColor.objects.all(
    ), allow_null=True, required=False, write_only=True)

    class Meta:
        model = ProductVariation
        fields = '__all__'

    # this will force more information for GET verb
    def to_representation(self, instance):
        """Customize GET response to include nested objects instead of just IDs."""
        data = super().to_representation(instance)

        # Replace ID fields with serialized data
        data['product'] = ProductSerializer(instance.product).data
        data['unit'] = ProductUnitSerializer(
            instance.unit).data if instance.unit else None
        data['size'] = ProductSizeSerializer(
            instance.size).data if instance.size else None
        data['color'] = ProductColorSerializer(
            instance.color).data if instance.color else None

        return data
