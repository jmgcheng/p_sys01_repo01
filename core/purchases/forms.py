from django import forms
from purchases.models import PurchaseRequestHeader, PurchaseRequestDetail


class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequestHeader
        fields = ['code', 'date', 'requestor', 'status']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')

        return cleaned_data
