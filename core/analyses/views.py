from datetime import date
from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Prefetch, Count, Case, When, Value, IntegerField, Sum
from django.db.models.functions import Coalesce
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
# from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
from employees.models import Employee
from products.models import ProductVariation
from sales.models import SaleInvoiceDetail, SaleInvoiceCategory
# from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
from inventories.utils import get_quantity_purchase_request_subquery, get_quantity_purchase_receive_subquery, get_quantity_sale_invoice_subquery, get_quantity_official_receipt_subquery
# from .mixins import AdminRequiredMixin
from django.views import View


class AnalysisTableListView(LoginRequiredMixin, TemplateView):
    template_name = "analyses/analysis_table_list.html"


def get_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def ajx_employee_demographics_age(request):
    # Define age groups
    age_groups = [
        (18, 23),
        (24, 29),
        (30, 39),
        (40, 49),
        (50, 57),
        (58, 64),
        (65, 100),
    ]

    #
    results = []

    #
    employees = Employee.objects.filter(
        status__name__in=['PROBATION', 'REGULAR'],
        birth_date__isnull=False
    ).exclude(
        user__is_superuser=True
    )

    # print(f'-------------hermit1------------------')
    # for employee in employees:
    #     print(
    #         f'{employee.company_id} - {employee.gender} - {get_age(employee.birth_date)}')
    # print(f'-------------hermit1------------------')

    #
    for age_min, age_max in age_groups:
        # Filter employees within the current age range
        group_employees = [
            emp for emp in employees
            if age_min <= get_age(emp.birth_date) <= age_max
        ]

        # Count male and female employees
        male_count = sum(1 for emp in group_employees if emp.gender == 'MALE')
        female_count = sum(
            1 for emp in group_employees if emp.gender == 'FEMALE')
        total_count = male_count + female_count

        # Calculate percentages
        male_percentage = (male_count / total_count *
                           100) if total_count else 0
        female_percentage = (female_count / total_count *
                             100) if total_count else 0

        # Append data to results
        results.append({
            'age': f"{age_min}~{age_max}",
            'male': f"{male_count} ({male_percentage:.0f}%)",
            'female': f"{female_count} ({female_percentage:.0f}%)",
            'total': f"{total_count} (100%)" if total_count else "0 (0%)",
        })

    return JsonResponse({'data': results})


def ajx_top_products(request):

    #
    product_variations = ProductVariation.objects.all()

    #
    product_variations = product_variations.annotate(
        purchase_requested=Coalesce(
            get_quantity_purchase_request_subquery(), 0),
        purchase_received=Coalesce(
            get_quantity_purchase_receive_subquery(), 0),
        sale_invoice=Coalesce(get_quantity_sale_invoice_subquery(), 0),
        official_receipt=Coalesce(get_quantity_official_receipt_subquery(), 0),
        product_name=F('product__name'),
    ).values(
        'name',
        'product_name',
        'purchase_requested',
        'purchase_received',
        'sale_invoice',
        'official_receipt',
    )

    #
    results = []

    # Format data for DataTables
    results = [
        {
            'product_variation': pv['name'],
            'product': pv['product_name'],
            'purchase_requested': pv['purchase_requested'],
            'purchase_received': pv['purchase_received'],
            'sale_invoice': pv['sale_invoice'],
            'official_receipt': pv['official_receipt'],
        }
        for pv in product_variations
    ]

    return JsonResponse({'data': results})


def ajx_sales_breakdown_category(request):
    # Annotate totals for each category and overall
    product_variations = SaleInvoiceDetail.objects.values(
        'product_variation__name'
    ).annotate(
        retail=Coalesce(
            Sum(
                Case(
                    When(sale_invoice_header__category__name='RETAIL',
                         then='quantity_request'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            Value(0),
        ),
        patient=Coalesce(
            Sum(
                Case(
                    When(sale_invoice_header__category__name='PATIENT',
                         then='quantity_request'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            Value(0),
        ),
        wholesale=Coalesce(
            Sum(
                Case(
                    When(sale_invoice_header__category__name='WHOLESALE',
                         then='quantity_request'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            Value(0),
        ),
        government=Coalesce(
            Sum(
                Case(
                    When(sale_invoice_header__category__name='GOVERNMENT',
                         then='quantity_request'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            Value(0),
        ),
        corporate=Coalesce(
            Sum(
                Case(
                    When(sale_invoice_header__category__name='CORPORATE',
                         then='quantity_request'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            Value(0),
        ),
        grand_total=Coalesce(Sum('quantity_request'), Value(0)),
    )

    # Format results for DataTables
    results = []
    for pv in product_variations:
        grand_total = pv['grand_total']
        formatted_row = {
            'product_variation': pv['product_variation__name'],
            'retail': f"{pv['retail']} ({(pv['retail'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'patient': f"{pv['patient']} ({(pv['patient'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'wholesale': f"{pv['wholesale']} ({(pv['wholesale'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'government': f"{pv['government']} ({(pv['government'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'corporate': f"{pv['corporate']} ({(pv['corporate'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'grand_total': f"{grand_total} (100%)" if grand_total else "0 (0%)",
        }
        results.append(formatted_row)

    return JsonResponse({'data': results})


# def ajx_top_selling_variations(request):
#     results = []
#     return JsonResponse({'data': results})


# def ajx_monthly_sales_vs_purchases(request):
#     results = []
#     return JsonResponse({'data': results})


# def ajx_receipts_payment_status(request):
#     results = []
#     return JsonResponse({'data': results})


# def ajx_patient_purchases(request):
#     results = []
#     return JsonResponse({'data': results})
