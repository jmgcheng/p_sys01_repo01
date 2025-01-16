from django import forms
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail
from django.forms import modelformset_factory, inlineformset_factory


class PurchaseRequestHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = PurchaseRequestHeader
        # fields = ['code', 'date', 'requestor', 'status']
        fields = ['code', 'date', 'vendor']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class PurchaseRequestDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequestDetail
        fields = ['product_variation', 'quantity_request']


PurchaseRequestModelFormSet = modelformset_factory(
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
)


PurchaseRequestInlineFormSet = inlineformset_factory(
    PurchaseRequestHeader,
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

PurchaseRequestInlineFormSetNoExtra = inlineformset_factory(
    PurchaseRequestHeader,
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)
