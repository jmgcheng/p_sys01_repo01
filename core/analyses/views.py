from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
# from django.core.paginator import Paginator
# from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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
