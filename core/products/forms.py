from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'excerpt', 'description', 'image_url']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')
        name = cleaned_data.get('name', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')
        cleaned_data['name'] = name.upper()

        return cleaned_data
