from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class Company(models.Model):
    """Company profile model for invoice issuer"""
    name = models.CharField(max_length=200, default='Squarem')
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    # Bank details
    bank_name = models.CharField(max_length=200, blank=True)
    bank_branch = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    
    # UPI details
    upi_id = models.CharField(max_length=100, blank=True)
    
    # Tax details
    gstin = models.CharField(max_length=15, blank=True, verbose_name='GSTIN')
    pan = models.CharField(max_length=10, blank=True, verbose_name='PAN')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Client(models.Model):
    """Client/Customer model"""
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Billing address
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_country = models.CharField(max_length=100, default='India')
    billing_postal_code = models.CharField(max_length=20, blank=True)
    
    # Shipping address (optional)
    shipping_address = models.TextField(blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    
    # Tax details
    gstin = models.CharField(max_length=15, blank=True, verbose_name='GSTIN')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_full_billing_address(self):
        """Returns formatted billing address"""
        parts = [self.billing_address]
        if self.billing_city:
            parts.append(self.billing_city)
        if self.billing_state:
            parts.append(self.billing_state)
        if self.billing_postal_code:
            parts.append(self.billing_postal_code)
        if self.billing_country:
            parts.append(self.billing_country)
        return ', '.join(parts)

    def get_full_shipping_address(self):
        """Returns formatted shipping address"""
        if not self.shipping_address:
            return self.get_full_billing_address()
        parts = [self.shipping_address]
        if self.shipping_city:
            parts.append(self.shipping_city)
        if self.shipping_state:
            parts.append(self.shipping_state)
        if self.shipping_postal_code:
            parts.append(self.shipping_postal_code)
        if self.shipping_country:
            parts.append(self.shipping_country)
        return ', '.join(parts)


class Invoice(models.Model):
    """Invoice model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    CURRENCY_CHOICES = [
        ('INR', '₹ INR'),
        ('USD', '$ USD'),
        ('EUR', '€ EUR'),
        ('GBP', '£ GBP'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    
    invoice_date = models.DateField()
    due_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    
    # Calculated fields
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Payment tracking
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Notes
    notes = models.TextField(blank=True, help_text='Internal notes')
    terms = models.TextField(blank=True, help_text='Terms and conditions')
    
    # QR Code for UPI payment
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='invoices')

    class Meta:
        ordering = ['-invoice_date', '-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.name}"

    def save(self, *args, **kwargs):
        """Override save to generate invoice number and QR code"""
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        # Only calculate totals if this invoice already has a primary key
        # (i.e., it's being updated, not created for the first time)
        if self.pk:
            self.calculate_totals()
        
        super().save(*args, **kwargs)
        
        # Generate QR code after saving
        if self.company and self.company.upi_id and not self.qr_code:
            self.generate_qr_code()

    def generate_invoice_number(self):
        """Generate unique invoice number"""
        from datetime import datetime
        year = datetime.now().year
        month = datetime.now().month
        
        last_invoice = Invoice.objects.filter(
            invoice_number__startswith=f'INV-{year}{month:02d}'
        ).order_by('-invoice_number').first()
        
        if last_invoice:
            last_num = int(last_invoice.invoice_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f'INV-{year}{month:02d}-{new_num:04d}'

    def calculate_totals(self):
        """Calculate invoice totals from line items"""
        items = self.items.all()
        
        subtotal = Decimal('0.00')
        tax_amount = Decimal('0.00')
        discount_amount = Decimal('0.00')
        
        for item in items:
            line_subtotal = item.quantity * item.rate
            line_discount = line_subtotal * (item.discount / Decimal('100'))
            line_taxable = line_subtotal - line_discount
            line_tax = line_taxable * (item.tax_rate / Decimal('100'))
            
            subtotal += line_subtotal
            discount_amount += line_discount
            tax_amount += line_tax
        
        self.subtotal = subtotal
        self.discount_amount = discount_amount
        self.tax_amount = tax_amount
        self.total = subtotal - discount_amount + tax_amount

    def get_balance_due(self):
        """Get remaining balance"""
        return self.total - self.amount_paid

    def is_paid(self):
        """Check if invoice is fully paid"""
        return self.amount_paid >= self.total

    def get_display_status(self):
        """Get the actual status considering overdue logic"""
        from datetime import date
        # If already marked as paid, return paid
        if self.status == 'paid':
            return 'paid'
        # If cancelled, return cancelled
        if self.status == 'cancelled':
            return 'cancelled'
        # If past due date and not paid, it's overdue
        if self.due_date < date.today() and self.status != 'paid':
            return 'overdue'
        # If not paid yet
        if self.amount_paid < self.total:
            return 'unpaid'
        return self.status

    def get_status_badge_class(self):
        """Get Bootstrap badge class for status"""
        status = self.get_display_status()
        status_classes = {
            'paid': 'bg-success',
            'unpaid': 'bg-warning text-dark',
            'overdue': 'bg-danger',
            'draft': 'bg-secondary',
            'sent': 'bg-info',
            'cancelled': 'bg-dark',
        }
        return status_classes.get(status, 'bg-secondary')

    def get_status_label(self):
        """Get human-readable status label"""
        status = self.get_display_status()
        labels = {
            'paid': 'Paid',
            'unpaid': 'Unpaid',
            'overdue': 'Overdue',
            'draft': 'Draft',
            'sent': 'Sent',
            'cancelled': 'Cancelled',
        }
        return labels.get(status, status.title())

    def generate_qr_code(self):
        """Generate UPI QR code for payment"""
        if not self.company.upi_id:
            return
        
        # UPI payment string format
        upi_string = f"upi://pay?pa={self.company.upi_id}&pn={self.company.name}&am={self.total}&cu={self.currency}&tn=Invoice {self.invoice_number}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to Django file
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f'qr_{self.invoice_number}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        
        Invoice.objects.filter(pk=self.pk).update(qr_code=self.qr_code)

    def get_amount_in_words(self):
        """Convert amount to words (Indian numbering system)"""
        from num2words import num2words
        try:
            # Split into rupees and paise
            rupees = int(self.total)
            paise = int((self.total - rupees) * 100)
            
            words = num2words(rupees, lang='en_IN').title()
            if paise > 0:
                words += f" and {num2words(paise, lang='en_IN').title()} Paise"
            
            if self.currency == 'INR':
                words += " Rupees Only"
            else:
                words += " Only"
            
            return words
        except:
            return f"{self.currency} {self.total} Only"


class InvoiceItem(models.Model):
    """Line items for invoices"""
    
    # Unit type choices for construction company
    UNIT_TYPE_CHOICES = [
        ('sqft', 'Square Feet (Sq.Ft)'),
        ('sqm', 'Square Meter (Sq.M)'),
        ('nos', 'Numbers (Nos)'),
        ('ls', 'Lump Sum (L.S)'),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, default='nos', verbose_name='Unit')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    rate = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text='GST %')
    
    # Calculated fields
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.rate}"

    def save(self, *args, **kwargs):
        """Calculate line item amount"""
        subtotal = self.quantity * self.rate
        discount_amount = subtotal * (self.discount / Decimal('100'))
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * (self.tax_rate / Decimal('100'))
        self.amount = taxable_amount + tax_amount
        
        super().save(*args, **kwargs)
        
        # Update invoice totals
        if self.invoice_id:
            self.invoice.calculate_totals()
            Invoice.objects.filter(pk=self.invoice.pk).update(
                subtotal=self.invoice.subtotal,
                tax_amount=self.invoice.tax_amount,
                discount_amount=self.invoice.discount_amount,
                total=self.invoice.total
            )

    def get_line_total(self):
        """Get line item total"""
        return self.amount


class PaymentInfo(models.Model):
    """Payment information and terms"""
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='payment_info')
    
    payment_method = models.CharField(max_length=100, blank=True)
    payment_terms = models.TextField(blank=True)
    
    # Bank transfer details
    bank_instructions = models.TextField(blank=True)
    
    # Signature
    authorized_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    signatory_name = models.CharField(max_length=200, blank=True)
    signatory_designation = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment Info for {self.invoice.invoice_number}"


class Payment(models.Model):
    """Individual payments/advances recorded against an invoice"""

    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_advance = models.BooleanField(default=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    reference = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=255, blank=True)
    paid_on = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-paid_on', '-created_at']

    def __str__(self):
        return f"Payment {self.amount} for {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_invoice_totals()

    def update_invoice_totals(self):
        total_paid = self.invoice.payments.aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
        self.invoice.amount_paid = total_paid
        # Auto-mark paid if fully settled
        if self.invoice.total and total_paid >= self.invoice.total:
            self.invoice.status = 'paid'
        self.invoice.save(update_fields=['amount_paid', 'status', 'updated_at'])
