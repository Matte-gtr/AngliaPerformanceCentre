from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        })
    )

    field_order = [
        'category',
        'name',
        'product_code',
        'make',
        'model',
        'discount_code',
        'manufacturer',
        'price_incl_vat',
        'fitting_cost',
        'description',
        'image',
        ]

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'product_code',
            'make',
            'model',
            'discount_code',
            'manufacturer',
            'price_incl_vat',
            'description',
            'fitting_cost',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'category': 'Category',
            'name': 'Name',
            'product_code': 'Product Code',
            'make': 'Vehicle Make',
            'model': 'Vehicle Model',
            'manufacturer': 'Item Manufacturer',
            'price_incl_vat': 'Price (incl vat)',
            'description': 'Item Description',
            'fitting_cost': 'Installation Cost',
            'image': 'Image',
            'discount_code': 'Discount Code',
        }

        labels = {
            'category': 'Shop Category',
            'image': 'Images',
            'add_attributes': 'Add Attributes',
            'discount_code': 'Available Discount Codes',
        }

        for field in self.fields:
            if field != 'price_incl_vat' and field != 'fitting_cost':
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'
            elif field == 'price_incl_vat' or field == 'fitting_cost':
                self.fields[field].widget.attrs['class'] = 'form-control mb-1 mw-200'
            if field != 'category' and field != 'image' and field != \
                    'discount_code':
                self.fields[field].label = False
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'category' or field == 'image' or field == \
                    'discount_code':
                label = labels[field]
                self.fields[field].label = label
