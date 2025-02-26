from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail, PurchaseReceiveStatus
from employees.models import Employee
from rest_framework import serializers


class PurchaseRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestStatus
        fields = '__all__'


class PurchaseRequestDetailSerializer(serializers.ModelSerializer):
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
        queryset=Employee.objects.all(), allow_null=True, required=False, write_only=True)
    detail = PurchaseRequestDetailSerializer(many=True)

    class Meta:
        model = PurchaseRequestHeader
        fields = ('id', 'code', 'date', 'requestor',
                  'approver', 'vendor', 'status', 'detail')
