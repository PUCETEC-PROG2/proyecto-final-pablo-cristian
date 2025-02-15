from django import forms
from .models import Client, Product, Purchase, PurchaseDetail
from django.forms import BaseInlineFormSet

class RequiredInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_featured', 'category']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['client', 'date']  # Ahora date es editable
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'client': forms.Select(attrs={'class': 'form-select'})
        }