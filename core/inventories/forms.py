from django import forms
from inventories.models import InventoryAddHeader, InventoryAddDetail, InventoryDeductHeader, InventoryDeductDetail
from django.forms import modelformset_factory, inlineformset_factory


class InventoryAddHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = InventoryAddHeader
        fields = ['code', 'date', 'adder']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class InventoryAddDetailForm(forms.ModelForm):
    class Meta:
        model = InventoryAddDetail
        fields = ['product_variation', 'quantity_added']


# in use for extra 1
InventoryAddInlineFormSet = inlineformset_factory(
    InventoryAddHeader,
    InventoryAddDetail,
    form=InventoryAddDetailForm,
    fields=['product_variation', 'quantity_added'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
InventoryAddInlineFormSetNoExtra = inlineformset_factory(
    InventoryAddHeader,
    InventoryAddDetail,
    form=InventoryAddDetailForm,
    fields=['product_variation', 'quantity_added'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)


class InventoryDeductHeaderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)

    class Meta:
        model = InventoryDeductHeader
        fields = ['code', 'date', 'deducter']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data


class InventoryDeductDetailForm(forms.ModelForm):
    class Meta:
        model = InventoryDeductDetail
        fields = ['product_variation', 'quantity_deducted']


# in use for extra 1
InventoryDeductInlineFormSet = inlineformset_factory(
    InventoryDeductHeader,
    InventoryDeductDetail,
    form=InventoryDeductDetailForm,
    fields=['product_variation', 'quantity_deducted'],
    extra=1,  # Set the number of empty forms to display
    can_delete=True,
)

# in use for extra is 0
InventoryDeductInlineFormSetNoExtra = inlineformset_factory(
    InventoryDeductHeader,
    InventoryDeductDetail,
    form=InventoryDeductDetailForm,
    fields=['product_variation', 'quantity_deducted'],
    extra=0,  # Set the number of empty forms to display
    can_delete=True,
)
