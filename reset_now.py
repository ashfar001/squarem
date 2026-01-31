#!/usr/bin/env python
"""
Script to reset the database and create 2 admin accounts.
Run with: python reset_now.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice.settings')
django.setup()

from django.contrib.auth.models import User
from invoices.models import Company, Client, Invoice, InvoiceItem, PaymentInfo, Payment

def clear_media_files():
    """Clear uploaded media files"""
    media_dirs = ['media/company_logos', 'media/qr_codes']
    for dir_path in media_dirs:
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

print("=== Clearing all data ===")

# Delete in correct order due to foreign keys
Payment.objects.all().delete()
print("Deleted all payments")

PaymentInfo.objects.all().delete()
print("Deleted all payment info")

InvoiceItem.objects.all().delete()
print("Deleted all invoice items")

Invoice.objects.all().delete()
print("Deleted all invoices")

Client.objects.all().delete()
print("Deleted all clients")

Company.objects.all().delete()
print("Deleted all companies")

User.objects.all().delete()
print("Deleted all users")

# Clear media files
clear_media_files()
print("Cleared media files")

print("\n=== Creating admin accounts ===")

# Admin account 1
admin1 = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
print("Created admin: username='admin', password='admin123'")

# Admin account 2
admin2 = User.objects.create_superuser(
    username='admin2',
    email='admin2@example.com',
    password='admin456'
)
print("Created admin: username='admin2', password='admin456'")

print("\n=== SETUP COMPLETE ===")
print("Admin Accounts:")
print("  1. admin / admin123")
print("  2. admin2 / admin456")
