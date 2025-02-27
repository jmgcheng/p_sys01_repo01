from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus, PurchaseReceiveHeader, PurchaseReceiveDetail
from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra, PurchaseReceiveHeaderForm, PurchaseReceiveDetailForm, PurchaseReceiveInlineFormSet, PurchaseReceiveInlineFormSetNoExtra
# from .mixins import AdminRequiredMixin
from django.views import View
from purchases.serializers import PurchaseRequestStatusSerializer, PurchaseRequestDetailSerializer, PurchaseRequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as drf_status
from rest_framework import generics


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

        # Fetch PurchaseRequestDetails for the current header
        context['details'] = PurchaseRequestDetail.objects.filter(
            purchase_request_header=self.object)

        # Fetch PurchaseReceiveHeaders linked to the current PurchaseRequestHeader
        receive_headers = PurchaseReceiveHeader.objects.filter(
            purchase_request_header=self.object
        )

        # Include corresponding PurchaseReceiveDetails for the above headers
        receive_headers_with_details = receive_headers.prefetch_related(
            Prefetch(
                'purchasereceivedetail_set',
                queryset=PurchaseReceiveDetail.objects.select_related(
                    'product_variation'),
                to_attr='receive_details'
            )
        )
        context['receive_headers'] = receive_headers_with_details

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


# --- api ----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

class PurchaseRequestListCreateViewApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchase_requests = PurchaseRequestHeader.objects.all()
        serializer = PurchaseRequestSerializer(purchase_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class PurchaseRequestRetrieveUpdateDestroyViewApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return PurchaseRequestHeader.objects.get(pk=pk)
        except PurchaseRequestHeader.DoesNotExist:
            return None

    def get(self, request, pk):
        purchase_request = self.get_object(pk)
        if not purchase_request:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = PurchaseRequestSerializer(purchase_request)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_request = self.get_object(pk)
        if not purchase_request:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = PurchaseRequestSerializer(
            purchase_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     purchase_request = self.get_object(pk)
    #     if not purchase_request:
    #         return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)
    #     purchase_request.delete()
    #     return Response(status=drf_status.HTTP_204_NO_CONTENT)


# --- ajax ---------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


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
            Q(date__icontains=search_value) |
            Q(vendor__name__icontains=search_value) |
            Q(requestor__user__first_name__icontains=search_value) |
            Q(requestor__user__last_name__icontains=search_value) |
            Q(requestor__user__employee__middle_name__icontains=search_value) |
            Q(approver__user__first_name__icontains=search_value) |
            Q(approver__user__last_name__icontains=search_value) |
            Q(approver__user__employee__middle_name__icontains=search_value) |
            Q(status__name__icontains=search_value)

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
    elif order_column == 'status':
        order_column = 'status__name'
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
        'requestor', 'approver', 'vendor', 'status')

    paginator = Paginator(purchase_requests, length)
    total_records = paginator.count
    purchase_requests_page = paginator.get_page(start // length + 1)

    #
    data = []

    for pr in purchase_requests_page:
        fullname_requestor = f'{pr.requestor.user.first_name} {
            pr.requestor.user.last_name}'
        fullname_requestor = f'{fullname_requestor} {
            pr.requestor.user.employee.middle_name}' if pr.requestor.user.employee.middle_name else fullname_requestor
        fullname_approver = ''
        if pr.approver:
            fullname_approver = f'{pr.approver.user.first_name} {
                pr.approver.user.last_name}'
            fullname_approver = f'{fullname_approver} {
                pr.approver.user.employee.middle_name}' if pr.approver.user.employee.middle_name else fullname_approver

        data.append({

            'code': f"<a href='/purchases/requests/{pr.id}/'>{pr.code}</a>",
            'date': pr.date,
            'requestor': fullname_requestor,
            'vendor': pr.vendor.name if pr.vendor else '',
            'status': pr.status.name if pr.status else '',
            'approver': fullname_approver

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
            Q(date__icontains=search_value) |
            Q(purchase_request_header__code__icontains=search_value) |
            Q(receiver__user__first_name__icontains=search_value) |
            Q(receiver__user__last_name__icontains=search_value) |
            Q(receiver__user__employee__middle_name__icontains=search_value) |
            Q(status__name__icontains=search_value)

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
    elif order_column == 'status':
        order_column = 'status__name'
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
        'receiver', 'purchase_request_header', 'status')

    paginator = Paginator(purchase_receives, length)
    total_records = paginator.count
    purchase_receives_page = paginator.get_page(start // length + 1)

    #
    data = []

    for pr in purchase_receives_page:
        fullname_receiver = f'{pr.receiver.user.first_name} {
            pr.receiver.user.last_name}'
        fullname_receiver = f'{fullname_receiver} {
            pr.receiver.user.employee.middle_name}' if pr.receiver.user.employee.middle_name else fullname_receiver

        data.append({

            'code': f"<a href='/purchases/receives/{pr.id}/'>{pr.code}</a>",
            'request_code': f"<a href='/purchases/requests/{pr.purchase_request_header.id}/'>{pr.purchase_request_header.code}</a>" if pr.purchase_request_header else '',
            'date': pr.date,
            'receiver': fullname_receiver,
            'status': pr.status.name if pr.status else '',

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
