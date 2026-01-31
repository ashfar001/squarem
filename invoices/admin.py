from django.contrib import admin
from .models import Company, Client, Invoice, InvoiceItem, PaymentInfo


class InvoiceItemInline(admin.TabularInline):
    """Inline for invoice items"""
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'rate', 'discount', 'tax_rate', 'amount']
    readonly_fields = ['amount']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model"""
    list_display = ['name', 'email', 'phone', 'city', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'email', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'bank_branch', 'account_number', 'ifsc_code', 'upi_id')
        }),
        ('Tax Details', {
            'fields': ('gstin', 'pan')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin interface for Client model"""
    list_display = ['name', 'company_name', 'email', 'phone', 'billing_city', 'billing_country', 'created_at']
    list_filter = ['billing_country', 'created_at']
    search_fields = ['name', 'company_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company_name', 'email', 'phone', 'gstin', 'created_by')
        }),
        ('Billing Address', {
            'fields': ('billing_address', 'billing_city', 'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin interface for Invoice model"""
    list_display = ['invoice_number', 'client', 'company', 'invoice_date', 'due_date', 'total', 'status', 'created_at']
    list_filter = ['status', 'currency', 'invoice_date', 'created_at']
    search_fields = ['invoice_number', 'client__name', 'company__name']
    readonly_fields = ['invoice_number', 'subtotal', 'tax_amount', 'discount_amount', 'total', 'qr_code', 'created_at', 'updated_at']
    date_hierarchy = 'invoice_date'
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'company', 'client', 'invoice_date', 'due_date', 'status', 'currency')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'discount_amount', 'tax_amount', 'total', 'amount_paid')
        }),
        ('Additional Info', {
            'fields': ('notes', 'terms', 'qr_code'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by to current user if not set"""
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """Admin interface for InvoiceItem model"""
    list_display = ['invoice', 'description', 'quantity', 'rate', 'discount', 'tax_rate', 'amount']
    list_filter = ['invoice__status', 'tax_rate']
    search_fields = ['description', 'invoice__invoice_number']
    readonly_fields = ['amount']


@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    """Admin interface for PaymentInfo model"""
    list_display = ['invoice', 'payment_method', 'signatory_name', 'created_at']
    search_fields = ['invoice__invoice_number', 'signatory_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('invoice', 'payment_method', 'payment_terms', 'bank_instructions')
        }),
        ('Signature', {
            'fields': ('authorized_signature', 'signatory_name', 'signatory_designation')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site header
admin.site.site_header = "Squarem Invoice Administration"
admin.site.site_title = "Squarem Invoice Admin"
admin.site.index_title = "Welcome to Squarem Invoice Management"
