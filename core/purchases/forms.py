from django import forms
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail, PurchaseReceiveHeader, PurchaseReceiveDetail
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


# to be deleted
PurchaseRequestModelFormSet = modelformset_factory(
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
)

# in use for extra 1
PurchaseRequestInlineFormSet = inlineformset_factory(
    PurchaseRequestHeader,
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
PurchaseRequestInlineFormSetNoExtra = inlineformset_factory(
    PurchaseRequestHeader,
    PurchaseRequestDetail,
    form=PurchaseRequestDetailForm,
    fields=['product_variation', 'quantity_request'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)


class PurchaseReceiveHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = PurchaseReceiveHeader
        fields = ['code', 'date',
                  'purchase_request_header', 'receiver', 'status']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class PurchaseReceiveDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseReceiveDetail
        fields = ['product_variation', 'quantity_received']


# in use for extra 1
PurchaseReceiveInlineFormSet = inlineformset_factory(
    PurchaseReceiveHeader,
    PurchaseReceiveDetail,
    form=PurchaseReceiveDetailForm,
    fields=['product_variation', 'quantity_received'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
PurchaseReceiveInlineFormSetNoExtra = inlineformset_factory(
    PurchaseReceiveHeader,
    PurchaseReceiveDetail,
    form=PurchaseReceiveDetailForm,
    fields=['product_variation', 'quantity_received'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)
