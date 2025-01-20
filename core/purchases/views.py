# from audioop import reverse
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
# from .models import Purchase, PurchaseDetail
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
# from .forms import PurchaseForm, PurchaseDetailFormSet, PurchaseFormSet
from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
# from .mixins import AdminRequiredMixin
from django.views import View


class PurchaseRequestCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_form.html'
    form_class = PurchaseRequestHeaderForm
    success_url = reverse_lazy('purchases:purchase-request-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseRequestInlineFormSet(
                self.request.POST, prefix='purchase_request_detail', instance=self.object)
        else:
            context['formset'] = PurchaseRequestInlineFormSet(
                prefix='purchase_request_detail', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.requestor = self.request.user.employee
        form.instance.status = PurchaseRequestStatus.objects.get(
            name='OPEN (FOR APPROVAL)')

        formset = context['formset']

        if formset.is_valid():
            purchase_request_header = form.save()
            formset.instance = purchase_request_header
            formset.save()

            #
            messages.success(
                self.request, 'Purchase Request created successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class PurchaseRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_form.html'
    form_class = PurchaseRequestHeaderForm
    success_url = reverse_lazy('purchases:purchase-request-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load existing PurchaseRequestDetail objects for the header instance
            context['formset'] = PurchaseRequestInlineFormSetNoExtra(
                self.request.POST, instance=self.object, prefix='purchase_request_detail', )
        else:
            # Populate the formset with the existing details for the header instance
            context['formset'] = PurchaseRequestInlineFormSetNoExtra(
                instance=self.object, prefix='purchase_request_detail',)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save the updated header instance
            purchase_header = form.save()

            # Save the updated details for the header instance
            formset.instance = purchase_header
            formset.save()

            #
            messages.success(
                self.request, 'Purchase Request updated successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class PurchaseRequestDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = PurchaseRequestDetail.objects.filter(
            purchase_request_header=self.object)
        return context


class PurchaseRequestListView(LoginRequiredMixin, ListView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_list.html'


class PurchaseRequestApproveView(LoginRequiredMixin, View):
    template_name = 'purchases/purchase_request_confirm_approve.html'
    success_url = reverse_lazy('purchases:purchase-request-list')

    def get(self, request, *args, **kwargs):
        purchase_request = PurchaseRequestHeader.objects.get(
            pk=self.kwargs['pk'])
        return render(request, self.template_name, {'object': purchase_request})

    def post(self, request, *args, **kwargs):
        purchase_request = PurchaseRequestHeader.objects.get(
            pk=self.kwargs['pk'])
        purchase_request.status = PurchaseRequestStatus.objects.get(
            name='OPEN (PURCHASING)')
        purchase_request.approver = request.user.employee
        purchase_request.save()

        return redirect(self.success_url)


class PurchaseReceiveCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseReceiveHeader
    template_name = 'purchases/purchase_receive_form.html'
    form_class = PurchaseReceiveHeaderForm
    success_url = reverse_lazy('purchases:purchase-receive-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseReceiveInlineFormSet(
                self.request.POST, prefix='purchase_receive_detail', instance=self.object)
        else:
            context['formset'] = PurchaseReceiveInlineFormSet(
                prefix='purchase_receive_detail', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # form.instance.receiver = self.request.user.employee

        formset = context['formset']

        if formset.is_valid():
            purchase_receive_header = form.save()
            formset.instance = purchase_receive_header
            formset.save()

            #
            messages.success(
                self.request, 'Purchase Receive created successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class PurchaseReceiveUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseReceiveHeader
    template_name = 'purchases/purchase_receive_form.html'
    form_class = PurchaseReceiveHeaderForm
    success_url = reverse_lazy('purchases:purchase-receive-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load existing PurchaseReceiveDetail objects for the header instance
            context['formset'] = PurchaseReceiveInlineFormSetNoExtra(
                self.request.POST, instance=self.object, prefix='purchase_receive_detail', )
        else:
            # Populate the formset with the existing details for the header instance
            context['formset'] = PurchaseReceiveInlineFormSetNoExtra(
                instance=self.object, prefix='purchase_receive_detail',)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save the updated header instance
            purchase_header = form.save()

            # Save the updated details for the header instance
            formset.instance = purchase_header
            formset.save()

            #
            messages.success(
                self.request, 'Purchase Receive updated successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class PurchaseReceiveDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseReceiveHeader
    template_name = 'purchases/purchase_receive_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = PurchaseReceiveDetail.objects.filter(
            purchase_receive_header=self.object)
        return context


class PurchaseReceiveListView(LoginRequiredMixin, ListView):
    model = PurchaseReceiveHeader
    template_name = 'purchases/purchase_receive_list.html'


@login_required
def ajx_purchase_request_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    purchase_requests = PurchaseRequestHeader.objects.all()

    if search_value:
        purchase_requests = purchase_requests.filter(

            Q(code__icontains=search_value) |
            Q(requestor__user__first_name__icontains=search_value) |
            Q(vendor__name__icontains=search_value) |
            Q(approver__user__first_name__icontains=search_value)

        ).distinct()

    #
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    if order_column == 'requestor':
        order_column = 'requestor__user__first_name'
        if order_direction == 'desc':
            purchase_requests = purchase_requests.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            purchase_requests = purchase_requests.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'vendor':
        order_column = 'vendor__name'
        if order_direction == 'desc':
            purchase_requests = purchase_requests.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            purchase_requests = purchase_requests.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'approver':
        order_column = 'approver__user__first_name'
        if order_direction == 'desc':
            purchase_requests = purchase_requests.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            purchase_requests = purchase_requests.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        purchase_requests = purchase_requests.order_by(order_column)

    #
    purchase_requests = purchase_requests.select_related(
        'requestor', 'vendor', 'status')

    paginator = Paginator(purchase_requests, length)
    total_records = paginator.count
    purchase_requests_page = paginator.get_page(start // length + 1)

    #
    data = []

    for pr in purchase_requests_page:

        data.append({

            'code': f"<a href='/purchases/requests/{pr.id}/'>{pr.code}</a>",
            'date': pr.date,
            'requestor': pr.requestor.user.first_name,
            'vendor': pr.vendor.name if pr.vendor else '',
            'status': pr.status.name if pr.status else '',
            'approver': pr.approver.user.username if pr.approver else '',

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)


@login_required
def ajx_purchase_receive_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    purchase_receives = PurchaseReceiveHeader.objects.all()

    if search_value:
        purchase_receives = purchase_receives.filter(

            Q(code__icontains=search_value) |
            Q(receiver__user__first_name__icontains=search_value)

        ).distinct()

    #
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    if order_column == 'receiver':
        order_column = 'receiver__user__first_name'
        if order_direction == 'desc':
            purchase_receives = purchase_receives.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            purchase_receives = purchase_receives.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        purchase_receives = purchase_receives.order_by(order_column)

    #
    purchase_receives = purchase_receives.select_related(
        'receiver', 'purchase_request_header')

    paginator = Paginator(purchase_receives, length)
    total_records = paginator.count
    purchase_receives_page = paginator.get_page(start // length + 1)

    #
    data = []

    for pr in purchase_receives_page:

        data.append({

            'code': f"<a href='/purchases/receives/{pr.id}/'>{pr.code}</a>",
            'request_code': f"<a href='/purchases/requests/{pr.purchase_request_header.id}/'>{pr.purchase_request_header.code}</a>" if pr.purchase_request_header else '',
            'date': pr.date,
            'receiver': pr.receiver.user.first_name,

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)


# to be deleted
# class PurchaseRequestCreateView(LoginRequiredMixin, CreateView):
#     model = PurchaseRequestHeader
#     template_name = 'purchases/purchase_request_form.html'
#     form_class = PurchaseRequestHeaderForm
#     success_url = reverse_lazy('purchases:purchase-request-create')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # prefix
#         #   - the prefix name of input type hidden fields auto created in your template {{ formset.management_form }}
#         #   - also used for every input element for the detail
#         if self.request.POST:
#             context['formset'] = PurchaseRequestModelFormSet(self.request.POST, prefix='purchase_request_detail')

#             print('-----------------hermit1-------------------')
#             print(self.request.POST)
#             print('-----------------hermit1-------------------')

#         else:
#             # Pass an empty formset when not POST
#             context['formset'] = PurchaseRequestModelFormSet(prefix='purchase_request_detail', queryset=PurchaseRequestDetail.objects.none())
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']

#         print(f'-----------hermit2---------------')
#         print(formset)
#         print(f'-----------hermit2---------------')

#         # Process the PurchaseDetail formset
#         if formset.is_valid():
#             purchase_header = form.save()

#             for purchase_detail_form in formset:
#                 if purchase_detail_form.cleaned_data.get('product_variation'):
#                     purchase_detail = purchase_detail_form.save(commit=False)

#                     purchase_detail.purchase_request_header = purchase_header

#                     purchase_detail.save()

#         else:
#             # If formset is not valid, you can access formset.errors
#             print(f'-----------hermit3---------------')
#             print(formset.errors)
#             print(f'-----------hermit3---------------')
#             return render(
#                 self.request,
#                 self.template_name,
#                 context={'form': form, 'formset': formset},
#             )

#         return super().form_valid(form)
