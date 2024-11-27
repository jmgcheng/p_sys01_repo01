import pandas as pd
import os
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
# from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, Permission, User
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count, F, Case, When, IntegerField
from employees.models import Employee, EmployeeJobSpecialty, EmployeeJobLevel, EmployeeJob, EmployeeStatus
from employees.forms import EmployeeCreationForm
# , EmployeeUpdateForm, GroupForm, UserGroupForm, PermissionForm, EmployeeExcelUploadForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['positions'] = EmployeeJob.objects.all()
        context['specialties'] = EmployeeJobSpecialty.objects.all()
        context['genders'] = ['MALE', 'FEMALE']
        context['employee_status'] = EmployeeStatus.objects.filter(
            name__in=['REGULAR', 'PROBATION', 'SEPARATED'])

        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee-list')


@login_required
def ajx_employee_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    position_filter = request.GET.getlist('position[]', [])
    specialty_filter = request.GET.getlist('specialty[]', [])
    gender_filter = request.GET.getlist('gender[]', [])
    employee_status_filter = request.GET.getlist('employee_status[]', [])

    #
    employees = Employee.objects.all()

    print(f'---------hermit1----------')
    print(position_filter)
    print(specialty_filter)
    print(gender_filter)
    print(employee_status_filter)
    print(f'---------hermit1----------')

    if search_value:
        employees = employees.filter(

            Q(company_id__icontains=search_value) |
            # Q(last_name__icontains=search_value) |
            # Q(first_name__icontains=search_value) |
            Q(middle_name__icontains=search_value) |
            Q(position__name__icontains=search_value) |
            Q(position_specialties__name__icontains=search_value) |
            Q(position_level__name__icontains=search_value) |
            Q(gender__icontains=search_value) |
            Q(status__name__icontains=search_value)

        ).distinct()

    if position_filter:
        employees = employees.filter(position__name__in=position_filter)

    if specialty_filter:
        employees = employees.filter(
            position_specialties__name__in=specialty_filter)

    if gender_filter:
        employees = employees.filter(gender__in=gender_filter)

    if employee_status_filter:
        employees = employees.filter(status__name__in=employee_status_filter)

    #
    employees = employees.filter(user__is_active=True)

    # Handle ordering
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    #
    employees = employees.select_related(
        'status', 'position', 'position_level', 'user')
    employees = employees.prefetch_related('position_specialties')

    paginator = Paginator(employees, length)
    total_records = paginator.count
    employees_page = paginator.get_page(start // length + 1)

    #
    data = []

    for emp in employees_page:

        specialties = ', '.join([specialty.name for specialty in emp.position_specialties.all(
        )]) if emp.position_specialties else ''

        data.append({

            'company_id': emp.company_id,
            'start_date': emp.start_date,
            'last_name': emp.user.last_name,
            'first_name': emp.user.first_name,
            'middle_name': emp.middle_name,
            'position': emp.position.name,
            'specialties': specialties,
            'level': emp.position_level.name,
            'gender': emp.gender,
            'status': emp.status.name

        })

    # print(f'---------hermit2----------')
    # print(employees_page)
    # print(f'---------hermit2----------')

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
