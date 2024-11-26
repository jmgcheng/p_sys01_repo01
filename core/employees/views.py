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
# from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, Permission, User
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count, F, Case, When, IntegerField
from employees.models import Employee, EmployeeJobSpecialty, EmployeeJobLevel, EmployeeJob, EmployeeStatus
# from .forms import EmployeeCreationForm, EmployeeUpdateForm, GroupForm, UserGroupForm, PermissionForm, EmployeeExcelUploadForm
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
