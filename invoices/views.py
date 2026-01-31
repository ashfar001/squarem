from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import date, timedelta
from decimal import Decimal

from .models import Company, Client, Invoice, InvoiceItem, PaymentInfo, Payment
from .forms import (
    CompanyForm, ClientForm, InvoiceForm, 
    InvoiceItemFormSet, InvoiceItemFormSetEdit, PaymentInfoForm, PaymentForm
)


# Authentication Views
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'invoices/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# Dashboard
def dashboard(request):
    """Main dashboard with statistics"""
    invoices = Invoice.objects.all()
    
    # Statistics
    total_invoices = invoices.count()
    total_revenue = invoices.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
    paid_invoices = invoices.filter(status='paid').count()
    unpaid_invoices = invoices.exclude(status='paid').count()
    
    # Recent invoices
    recent_invoices = invoices.order_by('-created_at')[:10]
    
    # Overdue invoices
    overdue_invoices = invoices.filter(
        due_date__lt=date.today(),
        status__in=['draft', 'sent']
    ).count()
    
    context = {
        'total_invoices': total_invoices,
        'total_revenue': total_revenue,
        'paid_invoices': paid_invoices,
        'unpaid_invoices': unpaid_invoices,
        'overdue_invoices': overdue_invoices,
        'recent_invoices': recent_invoices,
    }
    
    return render(request, 'invoices/dashboard.html', context)


# Company Views
def company_list(request):
    """List all companies"""
    companies = Company.objects.all()
    return render(request, 'invoices/company_list.html', {'companies': companies})


def company_create(request):
    """Create new company"""
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Company "{company.name}" created successfully.')
            return redirect('company_list')
    else:
        form = CompanyForm()
    
    return render(request, 'invoices/company_form.html', {'form': form, 'action': 'Create'})


def company_edit(request, pk):
    """Edit existing company"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Company "{company.name}" updated successfully.')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'invoices/company_form.html', {'form': form, 'action': 'Edit', 'company': company})


def company_delete(request, pk):
    """Delete company"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Company "{company_name}" deleted successfully.')
        return redirect('company_list')
    
    return render(request, 'invoices/company_confirm_delete.html', {'company': company})


# Client Views
def client_list(request):
    """List all clients"""
    clients = Client.objects.all()
    return render(request, 'invoices/client_list.html', {'clients': clients})


def client_create(request):
    """Create new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            if request.user.is_authenticated:
                client.created_by = request.user
            client.save()
            messages.success(request, f'Client "{client.name}" created successfully.')
            return redirect('client_list')
    else:
        form = ClientForm()
    
    return render(request, 'invoices/client_form.html', {'form': form, 'action': 'Create'})


def client_edit(request, pk):
    """Edit existing client"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client "{client.name}" updated successfully.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'invoices/client_form.html', {'form': form, 'action': 'Edit', 'client': client})


def client_delete(request, pk):
    """Delete client"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        client_name = client.name
        client.delete()
        messages.success(request, f'Client "{client_name}" deleted successfully.')
        return redirect('client_list')
    
    return render(request, 'invoices/client_confirm_delete.html', {'client': client})


# Invoice Views
def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.select_related('client', 'company').all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search_query) |
            Q(client__name__icontains=search_query)
        )
    
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})


def invoice_create(request):
    """Create new invoice with line items"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST, instance=Invoice(), prefix='items')
        
        if form.is_valid() and formset.is_valid():
            # First save the invoice to get a primary key
            invoice = form.save(commit=False)
            if request.user.is_authenticated:
                invoice.created_by = request.user
            invoice.save()  # Now invoice has a pk
            
            # Save the line items
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    if item_form.cleaned_data.get('description'):  # Only save if has description
                        item = item_form.save(commit=False)
                        item.invoice = invoice
                        item.save()
            
            # Recalculate totals after items are saved
            invoice.calculate_totals()
            invoice.save()
            
            messages.success(request, f'Invoice "{invoice.invoice_number}" created successfully.')
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet(instance=Invoice(), prefix='items')
    
    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Create'
    })


def invoice_edit(request, pk):
    """Edit existing invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSetEdit(request.POST, instance=invoice, prefix='items')
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.save()
            
            # Recalculate totals
            invoice.calculate_totals()
            invoice.save()
            
            messages.success(request, f'Invoice "{invoice.invoice_number}" updated successfully.')
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSetEdit(instance=invoice, prefix='items')
    
    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Edit',
        'invoice': invoice
    })


def invoice_detail(request, pk):
    """View invoice details in printable format"""
    invoice = get_object_or_404(
        Invoice.objects.select_related('company', 'client').prefetch_related('items'),
        pk=pk
    )
    
    # Get or create payment info
    payment_info, created = PaymentInfo.objects.get_or_create(invoice=invoice)
    payments = invoice.payments.all()
    
    # Build PDF URL for sharing
    pdf_url = request.build_absolute_uri(f'/invoices/{pk}/pdf/')
    
    context = {
        'invoice': invoice,
        'payment_info': payment_info,
        'payments': payments,
        'pdf_url': pdf_url,
    }
    
    return render(request, 'invoices/invoice_detail.html', context)


def invoice_mark_paid(request, pk):
    """Mark invoice as paid"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        invoice.status = 'paid'
        invoice.amount_paid = invoice.total
        invoice.save()
        messages.success(request, f'Invoice "{invoice.invoice_number}" marked as paid.')
    
    return redirect('invoice_detail', pk=pk)


def invoice_delete(request, pk):
    """Delete invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Invoice "{invoice_number}" deleted successfully.')
        return redirect('invoice_list')
    
    return render(request, 'invoices/invoice_confirm_delete.html', {'invoice': invoice})


def invoice_pdf(request, pk):
    """Generate PDF from invoice"""
    invoice = get_object_or_404(
        Invoice.objects.select_related('company', 'client').prefetch_related('items'),
        pk=pk
    )
    
    # Get or create payment info
    payment_info, created = PaymentInfo.objects.get_or_create(invoice=invoice)
    
    try:
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Render HTML template
        template = get_template('invoices/invoice_pdf.html')
        context = {
            'invoice': invoice,
            'payment_info': payment_info,
        }
        html_string = template.render(context)
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        
        if not pdf.err:
            # Return PDF response
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            # Use inline for viewing in browser (works better on mobile)
            # Add download param for forcing download
            if request.GET.get('download'):
                response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
            else:
                response['Content-Disposition'] = f'inline; filename="invoice_{invoice.invoice_number}.pdf"'
            return response
        else:
            messages.error(request, 'Error generating PDF.')
            return redirect('invoice_detail', pk=pk)
        
    except ImportError:
        messages.error(request, 'xhtml2pdf is not installed. Please install it to generate PDFs.')
        return redirect('invoice_detail', pk=pk)


def payment_create(request, invoice_pk):
    """Record an advance/partial payment for an invoice"""
    invoice = get_object_or_404(Invoice, pk=invoice_pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            messages.error(request, 'Please correct the payment details below.')
    else:
        form = PaymentForm()

    return render(request, 'invoices/payment_form.html', {
        'invoice': invoice,
        'form': form,
    })


def payment_receipt_pdf(request, pk):
    """Generate PDF receipt for a specific payment"""
    payment = get_object_or_404(Payment.objects.select_related('invoice__client', 'invoice__company'), pk=pk)
    invoice = payment.invoice

    try:
        from xhtml2pdf import pisa
        from io import BytesIO

        template = get_template('invoices/payment_receipt_pdf.html')
        context = {
            'payment': payment,
            'invoice': invoice,
        }
        html_string = template.render(context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = f"receipt_{invoice.invoice_number}_{payment.pk}.pdf"
            if request.GET.get('download'):
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
        messages.error(request, 'Error generating receipt PDF.')
    except ImportError:
        messages.error(request, 'xhtml2pdf is not installed. Please install it to generate PDFs.')

    return redirect('invoice_detail', pk=invoice.pk)
