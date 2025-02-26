from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q, Count, F, Case, When, IntegerField, Value, Prefetch, TextField
from django.db.models.functions import Coalesce
from products.models import ProductColor, ProductSize, ProductUnit, Product, ProductVariation
from products.forms import ProductForm, ProductVariationForm
from inventories.utils import get_quantity_purchasing_subquery, get_quantity_purchasing_receive_subquery, get_quantity_sale_releasing_subquery, get_quantity_sold_subquery, get_quantity_inventory_add_subquery, get_quantity_inventory_deduct_subquery
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from products.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as drf_status


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product-list')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product-list')

    def form_valid(self, form):
        #
        messages.success(self.request, 'Product updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        #
        messages.warning(self.request, 'Please check errors below')
        return super().form_invalid(form)


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


class ProductVariationCreateView(LoginRequiredMixin, CreateView):
    model = ProductVariation
    form_class = ProductVariationForm
    template_name = 'products/product_variation_form.html'
    success_url = reverse_lazy('products:product-variation-list')


class ProductVariationDetailView(LoginRequiredMixin, DetailView):
    model = ProductVariation
    template_name = 'products/product_variation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_variation = get_object_or_404(
            ProductVariation, pk=self.kwargs['pk'])

        # Annotate the object with reusable subqueries
        product_variation = ProductVariation.objects.filter(pk=product_variation.pk).annotate(
            quantity_manual_add=Coalesce(
                get_quantity_inventory_add_subquery(), 0),
            quantity_manual_deduct=Coalesce(
                get_quantity_inventory_deduct_subquery(), 0),
            quantity_purchasing=Coalesce(
                get_quantity_purchasing_subquery(), 0),
            quantity_purchasing_receive=Coalesce(
                get_quantity_purchasing_receive_subquery(), 0),
            quantity_sale_releasing=Coalesce(
                get_quantity_sale_releasing_subquery(), 0),
            quantity_sold=Coalesce(get_quantity_sold_subquery(), 0),
            quantity_on_hand=(
                Coalesce(get_quantity_purchasing_receive_subquery(), 0)
                + Coalesce(get_quantity_inventory_add_subquery(), 0)
                - Coalesce(get_quantity_inventory_deduct_subquery(), 0)
                - Coalesce(get_quantity_sold_subquery(), 0)
            )
        ).first()

        # Add the annotated object to the context
        context['annotated_product_variation'] = product_variation
        return context


class ProductVariationUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductVariation
    form_class = ProductVariationForm
    template_name = 'products/product_variation_form.html'
    success_url = reverse_lazy('products:product-variation-list')

    def form_valid(self, form):
        #
        messages.success(
            self.request, 'Product Variation updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        #
        messages.warning(self.request, 'Please check errors below')
        return super().form_invalid(form)


# --- api ----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

class ProductListCreateViewApi(APIView):
    # takes care of listing products. Eg. GET domain.com/api/products/
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # takes care of creating a single new product. Eg. POST domain.com/api/products/
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyViewApi(APIView):
    def get_object(self, pk):
        # try:
        #     return Product.objects.get(pk=self.kwargs['pk'])
        # except Product.DoesNotExist:
        #     raise Http404
        return get_object_or_404(Product, pk=pk)

    # takes care of getting single product detail. Eg. GET domain.com/api/products/1
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # takes care of updating single product detail. Eg. PUT domain.com/api/products/1
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #     product = self.get_object()
    #     product.delete()
    #     return Response(status=drf_status.HTTP_204_NO_CONTENT)

# --- ajax ---------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


@login_required
def ajx_product_list(request):

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    #
    products = Product.objects.all()

    if search_value:
        products = products.filter(
            Q(code__icontains=search_value) |
            Q(name__icontains=search_value)
        ).distinct()

    # Handle ordering
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    order_column = request.GET.get(
        f'columns[{order_column_index}][data]', 'id')

    # print(f'----------------hermit1------------------')
    # print(order_column)
    # print(f'----------------hermit1------------------')

    if order_direction == 'desc':
        order_column = f'-{order_column}'
    products = products.order_by(order_column)

    paginator = Paginator(products, length)
    total_records = paginator.count
    products_page = paginator.get_page(start // length + 1)

    #
    data = []

    for p in products_page:
        data.append({
            'code': f"<a href='/products/{p.id}/'>{p.code}</a>",
            'name': p.name,
        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)


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

    if order_column == 'product':
        order_column = 'product__name'
        if order_direction == 'desc':
            product_variations = product_variations.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            product_variations = product_variations.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'unit':
        order_column = 'unit__name'
        if order_direction == 'desc':
            product_variations = product_variations.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            product_variations = product_variations.order_by(
                F(order_column).asc(nulls_last=True))
    elif order_column == 'color':
        order_column = 'color__name'
        if order_direction == 'desc':
            product_variations = product_variations.order_by(
                F(order_column).desc(nulls_last=True))
        else:
            product_variations = product_variations.order_by(
                F(order_column).asc(nulls_last=True))
    else:
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        product_variations = product_variations.order_by(order_column)

    #
    product_variations = product_variations.select_related(
        'product', 'unit', 'size', 'color')

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
            'quantity_alert': pv.quantity_alert if pv.quantity_alert else '',
        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    }

    return JsonResponse(response)
