from django import forms
from products.models import Product, ProductVariation


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


class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['code', 'product', 'name', 'excerpt',
                  'description', 'unit', 'size', 'color', 'image_url', 'quantity_alert']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code', '')
        # name = cleaned_data.get('name', '')

        #
        cleaned_data['code'] = code.upper().replace(' ', '-')
        # cleaned_data['name'] = name.upper()

        return cleaned_data
