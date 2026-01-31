from django import forms
from django.forms import inlineformset_factory
from .models import Company, Client, Invoice, InvoiceItem, PaymentInfo, Payment


class CompanyForm(forms.ModelForm):
    """Form for Company model"""
    class Meta:
        model = Company
        exclude = ['created_at', 'updated_at']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control'}),
            'pan': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ClientForm(forms.ModelForm):
    """Form for Client model"""
    class Meta:
        model = Client
        exclude = ['created_at', 'updated_at', 'created_by']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_state': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_country': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InvoiceForm(forms.ModelForm):
    """Form for Invoice model"""
    class Meta:
        model = Invoice
        fields = [
            'company', 'client', 'invoice_date', 'due_date', 
            'status', 'currency', 'notes', 'terms'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'client': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'terms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial date to today if creating new invoice
        if not self.instance.pk:
            from datetime import date, timedelta
            self.fields['invoice_date'].initial = date.today()
            self.fields['due_date'].initial = date.today() + timedelta(days=30)


class InvoiceItemForm(forms.ModelForm):
    """Form for InvoiceItem model"""
    class Meta:
        model = InvoiceItem
        fields = ['description', 'unit_type', 'quantity', 'rate', 'discount', 'tax_rate']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work/Material description'}),
            'unit_type': forms.Select(attrs={'class': 'form-control form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'value': '1'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'value': '0'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'value': '18'}),
        }


# Formset for managing multiple invoice items
# NOTE: extra=1 for new invoices, extra=0 for editing existing invoices
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)

# Formset with no extra rows for editing
InvoiceItemFormSetEdit = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class PaymentInfoForm(forms.ModelForm):
    """Form for PaymentInfo model"""
    class Meta:
        model = PaymentInfo
        exclude = ['invoice', 'created_at', 'updated_at']
        widgets = {
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_terms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'bank_instructions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'signatory_name': forms.TextInput(attrs={'class': 'form-control'}),
            'signatory_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'authorized_signature': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    """Form to capture advance/partial payments"""

    class Meta:
        model = Payment
        fields = ['amount', 'is_advance', 'method', 'reference', 'note', 'paid_on']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'required': True}),
            'is_advance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'method': forms.Select(attrs={'class': 'form-control form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Txn/Ref number (optional)'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes (optional)'}),
            'paid_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
