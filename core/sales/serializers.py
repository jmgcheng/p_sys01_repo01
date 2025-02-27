from products.models import Product, ProductVariation
from sales.models import SaleInvoiceHeader, SaleInvoiceDetail, SaleInvoiceCategory, SaleInvoiceStatus, OfficialReceiptHeader, OfficialReceiptDetail, OfficialReceiptStatus
from employees.models import Employee
from vendors.models import Vendor
from customers.models import Customer
from rest_framework import serializers


class SaleInvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleInvoiceStatus
        fields = '__all__'


class SaleInvoiceDetailSerializer(serializers.ModelSerializer):
    product_variation = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariation.objects.all())

    class Meta:
        model = SaleInvoiceDetail
        fields = ('product_variation', 'quantity_request')


class SaleInvoiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=SaleInvoiceCategory.objects.all(), write_only=True)
    status = serializers.PrimaryKeyRelatedField(
        queryset=SaleInvoiceStatus.objects.all(), write_only=True)
    creator = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), allow_null=True, required=False, write_only=True)

    # we don't need to use 'source' below if only we use 'related_name' for sale_invoice_header in SaleInvoiceDetail model
    detail = SaleInvoiceDetailSerializer(
        many=True, source='saleinvoicedetail_set')

    class Meta:
        model = SaleInvoiceHeader
        fields = ('id', 'code', 'date', 'category',
                  'creator', 'customer', 'status', 'detail')

    def create(self, validated_data):
        details_data = validated_data.pop('saleinvoicedetail_set')
        sale_invoice = SaleInvoiceHeader.objects.create(**validated_data)

        for detail_data in details_data:
            SaleInvoiceDetail.objects.create(
                sale_invoice_header=sale_invoice, **detail_data)

        return sale_invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('saleinvoicedetail_set')

        # Update main SaleInvoiceHeader fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle details update
        if details_data is not None:
            instance.saleinvoicedetail_set.all().delete()  # Clear old details
            for detail_data in details_data:
                SaleInvoiceDetail.objects.create(
                    sale_invoice_header=instance, **detail_data)

        return instance
