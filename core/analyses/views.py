from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from django.db.models import Q, F, Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
# from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
# from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
# from .mixins import AdminRequiredMixin
from django.views import View


class AnalysisTableListView(LoginRequiredMixin, TemplateView):
    template_name = "analyses/analysis_table_list.html"


def ajx_employee_demographics(request):

    results = []

    return JsonResponse({'data': results})


def ajx_top_requested_items(request):

    results = []

    return JsonResponse({'data': results})


def ajx_sales_breakdown(request):

    results = []

    return JsonResponse({'data': results})


def ajx_top_selling_variations(request):

    results = []

    return JsonResponse({'data': results})


def ajx_monthly_sales_vs_purchases(request):

    results = []

    return JsonResponse({'data': results})


def ajx_receipts_payment_status(request):

    results = []

    return JsonResponse({'data': results})


def ajx_patient_purchases(request):

    results = []

    return JsonResponse({'data': results})
