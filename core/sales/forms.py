from django import forms
from sales.models import SaleInvoiceHeader, SaleInvoiceDetail, OfficialReceiptHeader, OfficialReceiptDetail
from django.forms import modelformset_factory, inlineformset_factory


class SaleInvoiceHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = SaleInvoiceHeader
        fields = ['code', 'date', 'category', 'creator', 'customer', 'status']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class SaleInvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = SaleInvoiceDetail
        fields = ['product_variation', 'quantity_request']


# in use for extra 1
SaleInvoiceInlineFormSet = inlineformset_factory(
    SaleInvoiceHeader,
    SaleInvoiceDetail,
    form=SaleInvoiceDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
SaleInvoiceInlineFormSetNoExtra = inlineformset_factory(
    SaleInvoiceHeader,
    SaleInvoiceDetail,
    form=SaleInvoiceDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)


class OfficialReceiptHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = OfficialReceiptHeader
        fields = ['code', 'date', 'sale_invoice_header']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class OfficialReceiptDetailForm(forms.ModelForm):
    class Meta:
        model = OfficialReceiptDetail
        fields = ['product_variation', 'quantity_paid']


# in use for extra 1
OfficialReceiptInlineFormSet = inlineformset_factory(
    OfficialReceiptHeader,
    OfficialReceiptDetail,
    form=OfficialReceiptDetailForm,
    fields=['product_variation', 'quantity_paid'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
OfficialReceiptInlineFormSetNoExtra = inlineformset_factory(
    OfficialReceiptHeader,
    OfficialReceiptDetail,
    form=OfficialReceiptDetailForm,
    fields=['product_variation', 'quantity_paid'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)
