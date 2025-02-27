from products.models import Product, ProductVariation
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail, PurchaseReceiveStatus
from employees.models import Employee
from vendors.models import Vendor
from rest_framework import serializers


class PurchaseRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestStatus
        fields = '__all__'


class PurchaseRequestDetailSerializer(serializers.ModelSerializer):
    product_variation = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariation.objects.all())

    class Meta:
        model = PurchaseRequestDetail
        fields = ('product_variation', 'quantity_request')


class PurchaseRequestSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseRequestStatus.objects.all(), write_only=True)
    requestor = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True)
    approver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), allow_null=True, required=False, write_only=True)
    vendor = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), allow_null=True, required=False, write_only=True)

    # we don't need to use 'source' below if only we use 'related_name' for purchase_request_header in PurchaseRequestDetail model
    detail = PurchaseRequestDetailSerializer(
        many=True, source='purchaserequestdetail_set')

    class Meta:
        model = PurchaseRequestHeader
        fields = ('id', 'code', 'date', 'requestor',
                  'approver', 'vendor', 'status', 'detail')

    def create(self, validated_data):
        details_data = validated_data.pop('purchaserequestdetail_set')
        purchase_request = PurchaseRequestHeader.objects.create(
            **validated_data)

        for detail_data in details_data:
            PurchaseRequestDetail.objects.create(
                purchase_request_header=purchase_request, **detail_data)

        return purchase_request

    def update(self, instance, validated_data):
        details_data = validated_data.pop('purchaserequestdetail_set')

        # Update main PurchaseRequestHeader fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle details update
        if details_data is not None:
            instance.purchaserequestdetail_set.all().delete()  # Clear old details
            for detail_data in details_data:
                PurchaseRequestDetail.objects.create(
                    purchase_request_header=instance, **detail_data)

        return instance


class PurchaseReceiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReceiveStatus
        fields = '__all__'


class PurchaseReceiveDetailSerializer(serializers.ModelSerializer):
    product_variation = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariation.objects.all())

    class Meta:
        model = PurchaseReceiveDetail
        fields = ('product_variation', 'quantity_received')


class PurchaseReceiveSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseReceiveStatus.objects.all(), write_only=True)
    purchase_request_header = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseRequestHeader.objects.all(), write_only=True)
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True)

    # we don't need to use 'source' below if only we use 'related_name' for purchase_request_header in PurchaseReceiveDetail model
    detail = PurchaseReceiveDetailSerializer(
        many=True, source='purchasereceivedetail_set')

    class Meta:
        model = PurchaseReceiveHeader
        fields = ('id', 'code', 'date', 'receiver',
                  'purchase_request_header', 'status', 'detail')

    def create(self, validated_data):
        details_data = validated_data.pop('purchasereceivedetail_set')
        purchase_receive = PurchaseReceiveHeader.objects.create(
            **validated_data)

        for detail_data in details_data:
            PurchaseReceiveDetail.objects.create(
                purchase_receive_header=purchase_receive, **detail_data)

        return purchase_receive

    def update(self, instance, validated_data):
        details_data = validated_data.pop('purchasereceivedetail_set')

        # Update main PurchaseReceiveHeader fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle details update
        if details_data is not None:
            instance.purchasereceivedetail_set.all().delete()  # Clear old details
            for detail_data in details_data:
                PurchaseReceiveDetail.objects.create(
                    purchase_receive_header=instance, **detail_data)

        return instance
