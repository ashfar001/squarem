# Squarem Invoice - Django Invoice Management System

A clean, production-ready Django web application for creating and managing professional invoices and bills.

## 🌟 Features

### Core Functionality
- **Company Management** - Create and manage company profiles with logo, bank details, and UPI integration
- **Client Management** - Comprehensive client database with billing and shipping addresses
- **Invoice Creation** - Professional invoice generation with line items, taxes, and discounts
- **PDF Export** - Generate print-ready PDF invoices using WeasyPrint
- **QR Code Generation** - Automatic UPI payment QR codes for Indian payments
- **Dashboard** - Overview of total revenue, paid/unpaid invoices, and recent activity
- **Authentication** - Secure login system for authorized users only

### Invoice Features
- Auto-generated invoice numbers (format: INV-YYYYMM-0001)
- Multiple currency support (₹ INR, $ USD, € EUR, £ GBP)
- Line items with quantity, rate, discount, and GST
- Automatic calculation of subtotal, taxes, and grand total
- Amount in words (Indian numbering system)
- Invoice status tracking (Draft, Sent, Paid, Overdue, Cancelled)
- Payment tracking with balance due
- Custom notes and terms & conditions

### Design
- Clean, beige/off-white background inspired by professional invoices
- Responsive Bootstrap 5 interface
- Print-friendly invoice layout
- Mobile responsive design
- Modern, minimalist UI

## 📋 Requirements

- Python 3.10+
- Django 5.1+
- SQLite (default, can be changed to PostgreSQL/MySQL)
- See `requirements.txt` for full dependencies

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd d:\Django\invoice
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Create Static Files Directory

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 📂 Project Structure

```
invoice/
├── invoice/                    # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── invoices/                   # Main app
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── forms.py               # Django forms
│   ├── urls.py                # URL patterns
│   ├── admin.py               # Admin configuration
│   └── templates/             # HTML templates
│       └── invoices/
│           ├── base.html
│           ├── login.html
│           ├── dashboard.html
│           ├── invoice_detail.html
│           ├── invoice_pdf.html
│           ├── invoice_list.html
│           ├── invoice_form.html
│           ├── client_list.html
│           ├── client_form.html
│           ├── company_list.html
│           └── company_form.html
├── static/                     # Static files
│   └── css/
│       └── style.css
├── media/                      # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## 🎯 Usage Guide

### First Time Setup

1. **Login** - Navigate to http://127.0.0.1:8000/login/ and sign in with your superuser credentials

2. **Create a Company**
   - Go to Companies → Add Company
   - Fill in company details including:
     - Name, address, contact info
     - Bank details (for payment instructions)
     - UPI ID (for QR code generation)
     - GSTIN and PAN (for tax compliance)

3. **Add Clients**
   - Go to Clients → Add Client
   - Fill in client information and addresses

4. **Create Invoice**
   - Go to Invoices → Create Invoice
   - Select company and client
   - Set invoice and due dates
   - Add line items with descriptions, quantities, rates, discounts, and GST
   - Add notes or terms if needed
   - Save invoice

5. **View & Export**
   - View invoice in clean, printable format
   - Print directly from browser
   - Download as PDF

### Admin Panel

Access the Django admin panel at: http://127.0.0.1:8000/admin/

Features:
- Full CRUD operations on all models
- Inline editing of invoice items
- Advanced filtering and search
- Bulk actions

## 🔧 Configuration

### Settings (`invoice/settings.py`)

**Database:**
Default is SQLite. To use PostgreSQL or MySQL, update the `DATABASES` setting.

**Media Files:**
Uploaded files (logos, signatures, QR codes) are stored in the `media/` directory.

**Static Files:**
CSS and other static assets are in the `static/` directory.

### Environment Variables (Production)

For production deployment, set these environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False
- `ALLOWED_HOSTS` - Your domain name
- `DATABASE_URL` - Database connection string

## 📱 Features in Detail

### Invoice Numbering
Format: `INV-YYYYMM-XXXX`
- Example: INV-202601-0001
- Auto-increments monthly

### UPI QR Code
- Automatically generated when company has UPI ID
- Contains payment amount and invoice details
- Scannable by any UPI app

### Amount in Words
- Uses num2words library
- Supports Indian numbering (Lakhs, Crores)
- Displays "Rupees Only" for INR

### Status Tracking
- **Draft** - Invoice is being created
- **Sent** - Invoice sent to client
- **Paid** - Payment received
- **Overdue** - Past due date
- **Cancelled** - Invoice cancelled

## 🎨 Customization

### Colors & Design
Edit `static/css/style.css` to customize:
- Color scheme
- Typography
- Layout spacing

### Invoice Template
Edit `invoices/templates/invoices/invoice_detail.html` to customize:
- Invoice layout
- Sections displayed
- Content formatting

### PDF Template
Edit `invoices/templates/invoices/invoice_pdf.html` for PDF-specific styling.

## 🔒 Security

- Authentication required for all pages except login
- CSRF protection enabled
- Password validation
- SQL injection protection (Django ORM)

**For Production:**
- Set `DEBUG = False`
- Use strong `SECRET_KEY`
- Enable HTTPS
- Use secure database credentials
- Configure allowed hosts

## 📊 Database Models

- **Company** - Invoice issuer details
- **Client** - Customer information
- **Invoice** - Invoice header
- **InvoiceItem** - Line items
- **PaymentInfo** - Payment and signature details

## 🐛 Troubleshooting

### WeasyPrint Installation Issues

**Windows:**
WeasyPrint requires GTK3. Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

**Linux:**
```bash
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0
```

**Mac:**
```bash
brew install pango
```

### QR Code Not Generating
- Ensure company has UPI ID set
- Check that Pillow is installed
- Verify media directory has write permissions

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## 📝 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. Check model/view code comments

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL recommended)
- [ ] Set up static file serving (WhiteNoise or CDN)
- [ ] Configure media file storage (S3 recommended)
- [ ] Enable HTTPS
- [ ] Set secure cookies
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure backup strategy

### Recommended Stack
- **Server:** Gunicorn + Nginx
- **Database:** PostgreSQL
- **Storage:** AWS S3 for media files
- **Hosting:** AWS, DigitalOcean, Heroku, or PythonAnywhere

## 📈 Future Enhancements

Potential features for future versions:
- Email invoice sending
- Recurring invoices
- Multi-currency conversion
- Invoice templates
- Payment gateway integration
- Reports and analytics
- Client portal
- Invoice reminders
- Expense tracking
- Multi-language support

## 🙏 Acknowledgments

Built with:
- Django Web Framework
- Bootstrap 5
- WeasyPrint
- QRCode
- num2words

---

**Squarem Invoice** - Professional Invoice Management Made Simple
