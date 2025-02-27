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
from django.template.loader import get_template
from django.urls import reverse_lazy
from sales.models import SaleInvoiceCategory, SaleInvoiceStatus, SaleInvoiceHeader, SaleInvoiceDetail, OfficialReceiptStatus, OfficialReceiptHeader, OfficialReceiptDetail
from sales.forms import SaleInvoiceHeaderForm, SaleInvoiceDetailForm, SaleInvoiceInlineFormSet, SaleInvoiceInlineFormSetNoExtra, OfficialReceiptHeaderForm, OfficialReceiptDetailForm, OfficialReceiptInlineFormSet, OfficialReceiptInlineFormSetNoExtra
from django.views import View
from xhtml2pdf import pisa
from sales.serializers import SaleInvoiceStatusSerializer, SaleInvoiceDetailSerializer, SaleInvoiceSerializer, OfficialReceiptStatusSerializer, OfficialReceiptDetailSerializer, OfficialReceiptSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as drf_status


class SaleInvoiceCreateView(LoginRequiredMixin, CreateView):
    model = SaleInvoiceHeader
    template_name = 'sales/sale_invoice_form.html'
    form_class = SaleInvoiceHeaderForm
    success_url = reverse_lazy('sales:sale-invoice-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SaleInvoiceInlineFormSet(
                self.request.POST, prefix='sale_invoice_detail', instance=self.object)
        else:
            context['formset'] = SaleInvoiceInlineFormSet(
                prefix='sale_invoice_detail', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.creator = self.request.user.employee
        form.instance.status = SaleInvoiceStatus.objects.get(
            name='OPEN (FOR PAYMENT)')

        formset = context['formset']

        if formset.is_valid():
            sales_invoice_header = form.save()
            formset.instance = sales_invoice_header
            formset.save()

            #
            messages.success(
                self.request, 'Sales Invoice created successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class SaleInvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = SaleInvoiceHeader
    template_name = 'sales/sale_invoice_form.html'
    form_class = SaleInvoiceHeaderForm
    success_url = reverse_lazy('sales:sale-invoice-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load existing SaleInvoiceDetail objects for the header instance
            context['formset'] = SaleInvoiceInlineFormSetNoExtra(
                self.request.POST, instance=self.object, prefix='sale_invoice_detail', )
        else:
            # Populate the formset with the existing details for the header instance
            context['formset'] = SaleInvoiceInlineFormSetNoExtra(
                instance=self.object, prefix='sale_invoice_detail',)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save the updated header instance
            sale_header = form.save()

            # Save the updated details for the header instance
            formset.instance = sale_header
            formset.save()

            #
            messages.success(
                self.request, 'Sale Invoice updated successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class SaleInvoiceDetailView(LoginRequiredMixin, DetailView):
    model = SaleInvoiceHeader
    template_name = 'sales/sale_invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch SaleInvoiceDetails for the current header
        context['details'] = SaleInvoiceDetail.objects.filter(
            sale_invoice_header=self.object)

        # Fetch OfficialReceiptHeaders linked to the current SaleInvoiceHeader
        receipt_headers = OfficialReceiptHeader.objects.filter(
            sale_invoice_header=self.object)

        # Include corresponding OfficialReceiptDetails for the above headers
        receipt_headers_with_details = receipt_headers.prefetch_related(
            Prefetch(
                'officialreceiptdetail_set',
                queryset=OfficialReceiptDetail.objects.select_related(
                    'product_variation'),
                to_attr='receipt_details'
            )
        )
        context['receipt_headers'] = receipt_headers_with_details

        return context


def SaleInvoiceDetailPdfView(request, pk):
    template_path = "sales/sale_invoice_detail_pdf.html"
    sale_invoice = SaleInvoiceHeader.objects.get(pk=pk)
    details = SaleInvoiceDetail.objects.filter(
        sale_invoice_header=sale_invoice)
    receipt_headers = OfficialReceiptHeader.objects.filter(
        sale_invoice_header=sale_invoice).prefetch_related(
            Prefetch(
                'officialreceiptdetail_set',
                queryset=OfficialReceiptDetail.objects.select_related(
                    'product_variation'),
                to_attr='receipt_details'
            )
    )

    context = {
        'object': sale_invoice,
        'details': details,
        'receipt_headers': receipt_headers
    }

    # Render HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="sale_invoice_{
        pk}.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Return response if no errors
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


class SaleInvoiceListView(LoginRequiredMixin, ListView):
    model = SaleInvoiceHeader
    template_name = 'sales/sale_invoice_list.html'


class OfficialReceiptCreateView(LoginRequiredMixin, CreateView):
    model = OfficialReceiptHeader
    template_name = 'sales/official_receipt_form.html'
    form_class = OfficialReceiptHeaderForm
    success_url = reverse_lazy('sales:official-receipt-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OfficialReceiptInlineFormSet(
                self.request.POST, prefix='official_receipt_detail', instance=self.object)
        else:
            context['formset'] = OfficialReceiptInlineFormSet(
                prefix='official_receipt_detail', instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.creator = self.request.user.employee
        form.instance.status = OfficialReceiptStatus.objects.get(
            name='PAID')

        formset = context['formset']

        if formset.is_valid():
            official_receipt_header = form.save()
            formset.instance = official_receipt_header
            formset.save()

            #
            messages.success(
                self.request, 'Official Receipt created successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class OfficialReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = OfficialReceiptHeader
    template_name = 'sales/official_receipt_form.html'
    form_class = OfficialReceiptHeaderForm
    success_url = reverse_lazy('sales:official-receipt-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Load existing OfficialReceiptDetail objects for the header instance
            context['formset'] = OfficialReceiptInlineFormSetNoExtra(
                self.request.POST, instance=self.object, prefix='official_receipt_detail', )
        else:
            # Populate the formset with the existing details for the header instance
            context['formset'] = OfficialReceiptInlineFormSetNoExtra(
                instance=self.object, prefix='official_receipt_detail',)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Save the updated header instance
            receipt_header = form.save()

            # Save the updated details for the header instance
            formset.instance = receipt_header
            formset.save()

            #
            messages.success(
                self.request, 'Official Receipt updated successfully.')

            return super().form_valid(form)
        else:
            #
            messages.warning(self.request, 'Please check errors below')

            return self.form_invalid(form)


class OfficialReceiptDetailView(LoginRequiredMixin, DetailView):
    model = OfficialReceiptHeader
    template_name = 'sales/official_receipt_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = OfficialReceiptDetail.objects.filter(
            official_receipt_header=self.object)
        return context


class OfficialReceiptListView(LoginRequiredMixin, ListView):
    model = OfficialReceiptHeader
    template_name = 'sales/official_receipt_list.html'


# --- api ----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


class SaleInvoiceListCreateViewApi(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sale_invoices = SaleInvoiceHeader.objects.all()
        serializer = SaleInvoiceSerializer(sale_invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SaleInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class SaleInvoiceRetrieveUpdateDestroyViewApi(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return SaleInvoiceHeader.objects.get(pk=pk)
        except SaleInvoiceHeader.DoesNotExist:
            return None

    def get(self, request, pk):
        sale_invoice = self.get_object(pk)
        if not sale_invoice:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = SaleInvoiceSerializer(sale_invoice)
        return Response(serializer.data)

    def put(self, request, pk):
        sale_invoice = self.get_object(pk)
        if not sale_invoice:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = SaleInvoiceSerializer(
            sale_invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     sale_invoice = self.get_object(pk)
    #     if not sale_invoice:
    #         return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)
    #     sale_invoice.delete()
    #     return Response(status=drf_status.HTTP_204_NO_CONTENT)


class OfficialReceiptListCreateViewApi(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        official_receipts = OfficialReceiptHeader.objects.all()
        serializer = OfficialReceiptSerializer(official_receipts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfficialReceiptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class OfficialReceiptRetrieveUpdateDestroyViewApi(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OfficialReceiptHeader.objects.get(pk=pk)
        except OfficialReceiptHeader.DoesNotExist:
            return None

    def get(self, request, pk):
        official_receipt = self.get_object(pk)
        if not official_receipt:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = OfficialReceiptSerializer(official_receipt)
        return Response(serializer.data)

    def put(self, request, pk):
        official_receipt = self.get_object(pk)
        if not official_receipt:
            return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = OfficialReceiptSerializer(
            official_receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     official_receipt = self.get_object(pk)
    #     if not official_receipt:
    #         return Response({'error': 'Not found'}, status=drf_status.HTTP_404_NOT_FOUND)
    #     official_receipt.delete()
    #     return Response(status=drf_status.HTTP_204_NO_CONTENT)


# --- ajax ---------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


@login_required
def ajx_sale_invoice_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    sales_invoices = SaleInvoiceHeader.objects.all()

    if search_value:
        sales_invoices = sales_invoices.filter(

            Q(code__icontains=search_value) |
            Q(date__icontains=search_value) |
            Q(category__name__icontains=search_value) |
            Q(customer__first_name__icontains=search_value) |
            Q(customer__last_name__icontains=search_value) |
            Q(customer__middle_name__icontains=search_value) |
            Q(creator__user__first_name__icontains=search_value) |
            Q(creator__user__last_name__icontains=search_value) |
            Q(creator__user__employee__middle_name__icontains=search_value) |
            Q(status__name__icontains=search_value)

        ).distinct()

    #
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    if order_column == 'creator':
        order_column = 'creator__user__first_name'
        if order_direction == 'desc':
            sales_invoices = sales_invoices.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            sales_invoices = sales_invoices.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'customer':
        order_column = 'customer__first_name'
        if order_direction == 'desc':
            sales_invoices = sales_invoices.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            sales_invoices = sales_invoices.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'category':
        order_column = 'category__name'
        if order_direction == 'desc':
            sales_invoices = sales_invoices.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            sales_invoices = sales_invoices.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'status':
        order_column = 'status__name'
        if order_direction == 'desc':
            sales_invoices = sales_invoices.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            sales_invoices = sales_invoices.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        sales_invoices = sales_invoices.order_by(order_column)

    #
    sales_invoices = sales_invoices.select_related(
        'creator', 'customer', 'category', 'status')

    paginator = Paginator(sales_invoices, length)
    total_records = paginator.count
    sales_invoices_page = paginator.get_page(start // length + 1)

    #
    data = []

    for si in sales_invoices_page:
        fullname_creator = f'{si.creator.user.first_name} {
            si.creator.user.last_name}'
        fullname_creator = f'{fullname_creator} {
            si.creator.user.employee.middle_name}' if si.creator.user.employee.middle_name else fullname_creator
        fullname_customer = ''
        if si.customer:
            fullname_customer = f'{si.customer.first_name} {
                si.customer.last_name}'
            fullname_customer = f'{fullname_customer} {
                si.customer.middle_name}' if si.customer.middle_name else fullname_customer

        data.append({

            'code': f"<a href='/sales/invoices/{si.id}/'>{si.code}</a>",
            'date': si.date,
            'category': si.category.name if si.category else '',
            'customer': fullname_customer,
            'creator': fullname_creator,
            'status': si.status.name if si.status else '',

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)


@login_required
def ajx_official_receipt_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    official_receipts = OfficialReceiptHeader.objects.all()

    if search_value:
        official_receipts = official_receipts.filter(

            Q(code__icontains=search_value) |
            Q(date__icontains=search_value) |
            Q(creator__user__first_name__icontains=search_value) |
            Q(creator__user__last_name__icontains=search_value) |
            Q(creator__user__employee__middle_name__icontains=search_value) |
            Q(status__name__icontains=search_value)


        ).distinct()

    #
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    if order_column == 'creator':
        order_column = 'creator__user__first_name'
        if order_direction == 'desc':
            official_receipts = official_receipts.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            official_receipts = official_receipts.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'status':
        order_column = 'status__name'
        if order_direction == 'desc':
            official_receipts = official_receipts.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            official_receipts = official_receipts.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        official_receipts = official_receipts.order_by(order_column)

    #
    official_receipts = official_receipts.select_related('creator', 'status')

    paginator = Paginator(official_receipts, length)
    total_records = paginator.count
    official_receipts_page = paginator.get_page(start // length + 1)

    #
    data = []

    for ord in official_receipts_page:
        fullname_creator = f'{ord.creator.user.first_name} {
            ord.creator.user.last_name}'
        fullname_creator = f'{fullname_creator} {
            ord.creator.user.employee.middle_name}' if ord.creator.user.employee.middle_name else fullname_creator

        data.append({

            'code': f"<a href='/sales/receipts/{ord.id}/'>{ord.code}</a>",
            'date': ord.date,
            'creator': fullname_creator,
            'status': ord.status.name if ord.status else '',

        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
