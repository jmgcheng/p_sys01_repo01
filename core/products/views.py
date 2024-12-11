# import pandas as pd
# import os
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.urls import reverse_lazy
# from django.utils import timezone
# # from django.utils.decorators import method_decorator
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
# from django.contrib.auth.models import Group, Permission, User
# from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count, F, Case, When, IntegerField, Value, Prefetch, TextField
# from django.db.models.functions import Coalesce
# from django.contrib.postgres.aggregates import StringAgg
# from employees.models import Employee, EmployeeJobSpecialty, EmployeeJobLevel, EmployeeJob, EmployeeStatus
from products.models import ProductColor, ProductSize, ProductUnit, Product, ProductVariation
# from employees.forms import EmployeeCreationForm, EmployeeUpdateForm, EmployeeExcelUploadForm
# from employees.utils import insert_excel_employees, update_excel_employees, handle_uploaded_file
# # GroupForm, UserGroupForm, PermissionForm
# from employees.tasks import import_employees_task
# from celery.result import AsyncResult
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


class ProductVariationListView(LoginRequiredMixin, ListView):
    model = ProductVariation
    template_name = 'products/product_variation_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['colors'] = ProductColor.objects.all()
        context['sizes'] = ProductSize.objects.all()
        context['units'] = ProductUnit.objects.all()
        context['products'] = Product.objects.all()

        return context


@login_required
def ajx_product_variation_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    product_filter = request.GET.getlist('product[]', [])
    unit_filter = request.GET.getlist('unit[]', [])
    size_filter = request.GET.getlist('size[]', [])
    color_filter = request.GET.getlist('color[]', [])

    #
    product_variations = ProductVariation.objects.all()

    if search_value:
        product_variations = product_variations.filter(
            Q(code__icontains=search_value) |
            Q(product__name__icontains=search_value) |
            Q(name__icontains=search_value) |
            Q(unit__name__icontains=search_value) |
            Q(size__name__icontains=search_value) |
            Q(color__name__icontains=search_value)
        ).distinct()

    if product_filter:
        product_variations = product_variations.filter(
            product__name__in=product_filter)

    if unit_filter:
        product_variations = product_variations.filter(
            unit__name__in=unit_filter)

    if size_filter:
        product_variations = product_variations.filter(
            size__name__in=size_filter)

    if color_filter:
        product_variations = product_variations.filter(
            color__name__in=color_filter)

    # Handle ordering
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    # if order_column == 'last_name':
    #     order_column = 'user__last_name'
    #     if order_direction == 'desc':
    #         product_variations = product_variations.order_by(
    #             F(order_column).desc(nulls_last=True))
    #     else:
    #         product_variations = product_variations.order_by(
    #             F(order_column).asc(nulls_last=True))
    # elif order_column == 'specialties':
    #     order_column = 'specialties_agg'
    #     if order_direction == 'desc':
    #         product_variations = product_variations.order_by(
    #             F(order_column).desc(nulls_last=True))
    #     else:
    #         product_variations = product_variations.order_by(
    #             F(order_column).asc(nulls_last=True))
    # elif order_column == 'first_name':
    #     order_column = 'user__first_name'
    #     if order_direction == 'desc':
    #         product_variations = product_variations.order_by(
    #             F(order_column).desc(nulls_last=True))
    #     else:
    #         product_variations = product_variations.order_by(
    #             F(order_column).asc(nulls_last=True))
    # elif order_column == 'level':
    #     order_column = 'position_level'
    #     if order_direction == 'desc':
    #         product_variations = product_variations.order_by(
    #             F(order_column).desc(nulls_last=True))
    #     else:
    #         product_variations = product_variations.order_by(
    #             F(order_column).asc(nulls_last=True))
    # else:
    #     if order_direction == 'desc':
    #         order_column = f'-{order_column}'
    #     product_variations = product_variations.order_by(order_column)

    if order_direction == 'desc':
        order_column = f'-{order_column}'
    product_variations = product_variations.order_by(order_column)

    #
    product_variations = product_variations.select_related(
        'product', 'unit', 'size', 'color')
    # product_variations = product_variations.prefetch_related('position_specialties')

    paginator = Paginator(product_variations, length)
    total_records = paginator.count
    product_variations_page = paginator.get_page(start // length + 1)

    #
    data = []

    for pv in product_variations_page:
        data.append({
            'code': f"<a href='/products/variations/{pv.id}/'>{pv.code}</a>",
            'name': pv.name,
            'size': pv.size.name if pv.size else '',
            'unit': pv.unit.name if pv.unit else '',
            'color': pv.color.name if pv.color else '',
            'product': pv.product.name if pv.product.name else '',
        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
