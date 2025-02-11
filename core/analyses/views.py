from datetime import date
from django.utils.timezone import now
from collections import defaultdict
from django.shortcuts import redirect, render
from django.db.models.functions import ExtractMonth
# from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Prefetch, Count, Case, When, Value, IntegerField, Sum
from django.db.models.functions import Coalesce
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.template.loader import get_template
from django.urls import reverse_lazy
# from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
from employees.models import Employee
from products.models import ProductVariation
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseReceiveHeader, PurchaseReceiveDetail
from sales.models import SaleInvoiceHeader, SaleInvoiceDetail, SaleInvoiceCategory, OfficialReceiptHeader, OfficialReceiptDetail
# from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
from inventories.utils import get_quantity_purchase_request_subquery, get_quantity_purchase_receive_subquery, get_quantity_sale_invoice_subquery, get_quantity_official_receipt_subquery
# from .mixins import AdminRequiredMixin
from django.views import View
from xhtml2pdf import pisa


class AnalysisTableListView(LoginRequiredMixin, TemplateView):
    template_name = "analyses/analysis_table_list.html"


class AnalysisChartListView(LoginRequiredMixin, TemplateView):
    template_name = "analyses/analysis_chart_list.html"


def get_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


# --- AJXs ----------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------


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


def ajx_chart_employee_demographics_age(request):

    # Define age ranges
    age_ranges = {
        "18-23": (18, 23),
        "24-29": (24, 29),
        "30-39": (30, 39),
        "40-49": (40, 49),
        "50-57": (50, 57),
        "58-64": (58, 64),
        "65-100": (65, 100),
    }

    # Query eligible employees
    employees = Employee.objects.filter(
        status__name__in=["PROBATION", "REGULAR"],
        user__is_superuser=False,
        birth_date__isnull=False,
    )

    # Calculate age and gender distribution
    today = date.today()
    age_gender_distribution = defaultdict(lambda: {"MALE": 0, "FEMALE": 0})

    for employee in employees:
        age = today.year - employee.birth_date.year - \
            ((today.month, today.day) <
             (employee.birth_date.month, employee.birth_date.day))
        gender = employee.gender.upper()
        for range_name, (min_age, max_age) in age_ranges.items():
            if min_age <= age <= max_age:
                age_gender_distribution[range_name][gender] += 1
                break

    # Prepare data for the chart
    labels = list(age_ranges.keys())
    male_data = [age_gender_distribution[label]["MALE"] for label in labels]
    female_data = [age_gender_distribution[label]["FEMALE"]
                   for label in labels]

    response_data = {
        "labels": labels,
        "datasets": [
            {"label": "Male", "data": male_data, "backgroundColor": "#36A2EB"},
            {"label": "Female", "data": female_data, "backgroundColor": "#FF6384"},
        ],
    }
    return JsonResponse(response_data)


def ajx_chart_top_products(request):
    # Get the current year
    current_year = now().year
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    # Identify the most popular product variation
    top_variation = ProductVariation.objects.annotate(
        total_request=get_quantity_purchase_request_subquery(),
        total_receive=get_quantity_purchase_receive_subquery(),
        total_sale=get_quantity_sale_invoice_subquery(),
        total_receipt=get_quantity_official_receipt_subquery(),
    ).annotate(
        total_transactions=Sum(
            F("total_request") + F("total_receive") +
            F("total_sale") + F("total_receipt")
        )
    ).order_by("total_transactions").first()  # -total_transactions

    # If no product variation found, return empty data
    if not top_variation:
        return JsonResponse({"labels": months, "datasets": []})

    # Fetch monthly quantities for the top product variation
    def get_monthly_data(detail_model, header_relation, header_model, field_name):
        monthly_data = detail_model.objects.filter(
            product_variation=top_variation,
            **{f"{header_relation}__date__year": current_year}
        ).annotate(month=ExtractMonth(f"{header_relation}__date")).values("month").annotate(
            total_quantity=Sum(field_name)
        )
        return {entry["month"]: entry["total_quantity"] for entry in monthly_data}

    purchase_request_data = get_monthly_data(
        PurchaseRequestDetail, "purchase_request_header", PurchaseRequestHeader, "quantity_request"
    )
    purchase_receive_data = get_monthly_data(
        PurchaseReceiveDetail, "purchase_receive_header", PurchaseReceiveHeader, "quantity_received"
    )
    sale_invoice_data = get_monthly_data(
        SaleInvoiceDetail, "sale_invoice_header", SaleInvoiceHeader, "quantity_request"
    )
    official_receipt_data = get_monthly_data(
        OfficialReceiptDetail, "official_receipt_header", OfficialReceiptHeader, "quantity_paid"
    )

    # Prepare dataset for the chart
    labels = months
    datasets = [
        {
            "label": "Purchase Requests",
            "data": [purchase_request_data.get(i + 1, 0) for i in range(12)],
            "borderColor": "#36A2EB",
            "fill": False,
        },
        {
            "label": "Purchase Receives",
            "data": [purchase_receive_data.get(i + 1, 0) for i in range(12)],
            "borderColor": "#FF6384",
            "fill": False,
        },
        {
            "label": "Sales",
            "data": [sale_invoice_data.get(i + 1, 0) for i in range(12)],
            "borderColor": "#FFCE56",
            "fill": False,
        },
        {
            "label": "Official Receipts",
            "data": [official_receipt_data.get(i + 1, 0) for i in range(12)],
            "borderColor": "#4BC0C0",
            "fill": False,
        },
    ]

    response_data = {"labels": labels, "datasets": datasets}
    return JsonResponse(response_data)


def ajx_chart_sales_breakdown_category(request):
    # Aggregate sales data by category
    category_data = SaleInvoiceHeader.objects.values("category__name").annotate(
        total_sales=Sum("saleinvoicedetail__quantity_request")
    )

    # Prepare data for the pie chart
    labels = [entry["category__name"] for entry in category_data]
    data = [entry["total_sales"] for entry in category_data]

    response_data = {
        "labels": labels,
        "datasets": [
            {
                "data": data,
                "backgroundColor": [
                    "#FF6384",  # Color for RETAIL
                    "#36A2EB",  # Color for PATIENT
                    "#FFCE56",  # Color for WHOLESALE
                    "#4BC0C0",  # Color for GOVERNMENT
                    "#9966FF",  # Color for CORPORATE
                ],
            }
        ],
    }

    return JsonResponse(response_data)


# --- PDFs ----------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def EmployeeDemographicsAgePdfView(request):
    template_path = "analyses/analysis_employee_demographics_age_pdf.html"

    age_groups = [
        (18, 23),
        (24, 29),
        (30, 39),
        (40, 49),
        (50, 57),
        (58, 64),
        (65, 100),
    ]
    results = []
    employees = Employee.objects.filter(
        status__name__in=['PROBATION', 'REGULAR'],
        birth_date__isnull=False
    ).exclude(user__is_superuser=True)

    for age_min, age_max in age_groups:
        group_employees = [emp for emp in employees if age_min <= get_age(
            emp.birth_date) <= age_max]
        male_count = sum(1 for emp in group_employees if emp.gender == 'MALE')
        female_count = sum(
            1 for emp in group_employees if emp.gender == 'FEMALE')
        total_count = male_count + female_count

        results.append({
            'age': f"{age_min}~{age_max}",
            'male': f"{male_count} ({(male_count / total_count * 100) if total_count else 0:.0f}%)",
            'female': f"{female_count} ({(female_count / total_count * 100) if total_count else 0:.0f}%)",
            'total': f"{total_count} (100%)" if total_count else "0 (0%)",
        })

    context = {'data': results}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="employee_demographic_age.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f"Error generating PDF: <pre>{html}</pre>")

    return response


def TopProductsPdfView(request):
    template_path = "analyses/analysis_top_products_pdf.html"

    product_variations = ProductVariation.objects.annotate(
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

    product_variations = product_variations.order_by(
        F('official_receipt').desc(nulls_last=True))

    context = {'data': product_variations}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="top_products.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f"Error generating PDF: <pre>{html}</pre>")

    return response


def SalesBreakdownCategoryPdfView(request):
    template_path = "analyses/analysis_sales_breakdown_category_pdf.html"

    product_variations = SaleInvoiceDetail.objects.values(
        'product_variation__name'
    ).annotate(
        retail=Coalesce(Sum(Case(When(sale_invoice_header__category__name='RETAIL',
                        then='quantity_request'), default=Value(0), output_field=IntegerField())), Value(0)),
        patient=Coalesce(Sum(Case(When(sale_invoice_header__category__name='PATIENT',
                         then='quantity_request'), default=Value(0), output_field=IntegerField())), Value(0)),
        wholesale=Coalesce(Sum(Case(When(sale_invoice_header__category__name='WHOLESALE',
                           then='quantity_request'), default=Value(0), output_field=IntegerField())), Value(0)),
        government=Coalesce(Sum(Case(When(sale_invoice_header__category__name='GOVERNMENT',
                            then='quantity_request'), default=Value(0), output_field=IntegerField())), Value(0)),
        corporate=Coalesce(Sum(Case(When(sale_invoice_header__category__name='CORPORATE',
                           then='quantity_request'), default=Value(0), output_field=IntegerField())), Value(0)),
        grand_total=Coalesce(Sum('quantity_request'), Value(0)),
    )

    for pv in product_variations:
        grand_total = pv['grand_total']
        pv.update({
            'retail': f"{pv['retail']} ({(pv['retail'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'patient': f"{pv['patient']} ({(pv['patient'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'wholesale': f"{pv['wholesale']} ({(pv['wholesale'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'government': f"{pv['government']} ({(pv['government'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'corporate': f"{pv['corporate']} ({(pv['corporate'] / grand_total * 100) if grand_total else 0:.0f}%)",
            'grand_total': f"{grand_total} (100%)" if grand_total else "0 (0%)",
        })

    context = {'data': product_variations}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="sales_breakdown_category.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f"Error generating PDF: <pre>{html}</pre>")

    return response
