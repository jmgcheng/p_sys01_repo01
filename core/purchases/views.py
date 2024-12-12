from audioop import reverse
# from django.shortcuts import redirect, render
# from django.core.exceptions import PermissionDenied
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from .models import Purchase, PurchaseDetail
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseRequestStatus
# from .forms import PurchaseForm, PurchaseDetailFormSet, PurchaseFormSet
from purchases.forms import PurchaseRequestHeaderForm, PurchaseRequestDetailForm, PurchaseRequestModelFormSet, PurchaseRequestInlineFormSet, PurchaseRequestInlineFormSetNoExtra
# from .mixins import AdminRequiredMixin


class PurchaseRequestCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_form.html'
    form_class = PurchaseRequestHeaderForm
    success_url = reverse_lazy('purchases:purchase-request-create')

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
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PurchaseRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseRequestHeader
    template_name = 'purchases/purchase_request_form.html'
    form_class = PurchaseRequestHeaderForm
    success_url = reverse_lazy('purchases:purchase-request-create')

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
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


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
