from django.db.models import OuterRef, Subquery, Sum, IntegerField
from django.db.models.functions import Coalesce
from purchases.models import PurchaseRequestDetail, PurchaseReceiveDetail
from sales.models import SaleInvoiceDetail, OfficialReceiptDetail
from inventories.models import InventoryAddDetail, InventoryDeductDetail


def get_quantity_purchasing_subquery():
    return Subquery(
        PurchaseRequestDetail.objects.filter(
            product_variation=OuterRef('pk'),
            purchase_request_header__status__name="OPEN (PURCHASING)"
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_request')
        ).values('total_quantity'),
        output_field=IntegerField()
    )


def get_quantity_purchasing_receive_subquery():
    return Subquery(
        PurchaseReceiveDetail.objects.filter(
            product_variation=OuterRef('pk'),
            purchase_receive_header__status__name__in=[
                "RECEIVED (NO ISSUE)", "RECEIVED (WITH ISSUE)"
            ]
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_received')
        ).values('total_quantity'),
        output_field=IntegerField()
    )


def get_quantity_sale_releasing_subquery():
    return Subquery(
        SaleInvoiceDetail.objects.filter(
            product_variation=OuterRef('pk'),
            sale_invoice_header__status__name="OPEN (FOR PAYMENT)"
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_request')
        ).values('total_quantity'),
        output_field=IntegerField()
    )


def get_quantity_sold_subquery():
    return Subquery(
        OfficialReceiptDetail.objects.filter(
            product_variation=OuterRef('pk'),
            official_receipt_header__status__name="PAID"
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_paid')
        ).values('total_quantity'),
        output_field=IntegerField()
    )


def get_quantity_inventory_add_subquery():
    return Subquery(
        InventoryAddDetail.objects.filter(
            product_variation=OuterRef('pk')
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_added')
        ).values('total_quantity'),
        output_field=IntegerField()
    )


def get_quantity_inventory_deduct_subquery():
    return Subquery(
        InventoryDeductDetail.objects.filter(
            product_variation=OuterRef('pk')
        ).values('product_variation').annotate(
            total_quantity=Sum('quantity_deducted')
        ).values('total_quantity'),
        output_field=IntegerField()
    )
