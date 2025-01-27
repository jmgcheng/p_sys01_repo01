from datetime import date
from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Prefetch, Count, Case, When, Value, IntegerField
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
# from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
from employees.models import Employee
# from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
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

    results = []

    return JsonResponse({'data': results})


def ajx_sales_breakdown_category(request):

    results = []

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
