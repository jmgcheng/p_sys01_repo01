from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from inventories.models import InventoryAddHeader, InventoryAddDetail
from inventories.forms import InventoryAddHeaderForm, InventoryAddDetailForm, InventoryAddInlineFormSet, InventoryAddInlineFormSetNoExtra
# from .mixins import AdminRequiredMixin
from django.views import View


class InventoryAddCreateView(LoginRequiredMixin, CreateView):
    model = InventoryAddHeader
    template_name = 'inventories/inventory_add_form.html'
    form_class = InventoryAddHeaderForm
    success_url = reverse_lazy('inventories:inventory-add-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InventoryAddInlineFormSet(
                self.request.POST, prefix='inventory_add_detail', instance=self.object)
        else:
            context['formset'] = InventoryAddInlineFormSet(
                prefix='inventory_add_detail', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # form.instance.receiver = self.request.user.employee

        formset = context['formset']

        if formset.is_valid():
            inventory_add_header = form.save()
            formset.instance = inventory_add_header
            formset.save()

            #
            messages.success(
                self.request, 'Inventory added successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class InventoryAddUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryAddHeader
    template_name = 'inventories/inventory_add_form.html'
    form_class = InventoryAddHeaderForm
    success_url = reverse_lazy('inventories:inventory-add-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load existing InventoryAddDetail objects for the header instance
            context['formset'] = InventoryAddInlineFormSetNoExtra(
                self.request.POST, instance=self.object, prefix='inventory_add_detail', )
        else:
            # Populate the formset with the existing details for the header instance
            context['formset'] = InventoryAddInlineFormSetNoExtra(
                instance=self.object, prefix='inventory_add_detail',)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save the updated header instance
            inventory_add_header = form.save()

            # Save the updated details for the header instance
            formset.instance = inventory_add_header
            formset.save()

            #
            messages.success(
                self.request, 'Inventory Add updated successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class InventoryAddDetailView(LoginRequiredMixin, DetailView):
    model = InventoryAddHeader
    template_name = 'inventories/inventory_add_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = InventoryAddDetail.objects.filter(
            inventory_add_header=self.object)
        return context


class InventoryAddListView(LoginRequiredMixin, ListView):
    model = InventoryAddHeader
    template_name = 'inventories/inventory_add_list.html'


@login_required
def ajx_inventory_add_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    inventory_adds = InventoryAddHeader.objects.all()

    if search_value:
        inventory_adds = inventory_adds.filter(

            Q(code__icontains=search_value) |
            Q(adder__user__first_name__icontains=search_value)

        ).distinct()

    #
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    if order_column == 'adder':
        order_column = 'adder__user__first_name'
        if order_direction == 'desc':
            inventory_adds = inventory_adds.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            inventory_adds = inventory_adds.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        inventory_adds = inventory_adds.order_by(order_column)

    #
    inventory_adds = inventory_adds.select_related('adder')

    paginator = Paginator(inventory_adds, length)
    total_records = paginator.count
    inventory_adds_page = paginator.get_page(start // length + 1)

    #
    data = []

    for ia in inventory_adds_page:

        data.append({

            'code': f"<a href='/inventories/adds/{ia.id}/'>{ia.code}</a>",
            'date': ia.date,
            'adder': ia.adder.user.first_name,

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
