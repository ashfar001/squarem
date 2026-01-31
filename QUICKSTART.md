# 🚀 Quick Start Guide - Squarem Invoice

## ✅ Installation Complete!

Your Django invoice application is now set up and running.

---

## 🔐 Login Credentials

**Admin Account:**
- **URL:** http://127.0.0.1:8000/login/
- **Username:** `admin`
- **Password:** `admin123`

**Django Admin Panel:**
- **URL:** http://127.0.0.1:8000/admin/
- **Username:** `admin`
- **Password:** `admin123`

---

## 🎯 Getting Started

### Step 1: Login
1. Open your browser and go to: http://127.0.0.1:8000/
2. You'll be redirected to the login page
3. Enter username: `admin` and password: `admin123`

### Step 2: Create Your Company
1. Go to **Companies** from the navigation menu
2. Click **"Add Company"**
3. Fill in your company details:
   - **Name:** Squarem (or your company name)
   - **Address:** Your business address
   - **Contact info:** Email, phone, website
   - **Bank Details:** Account number, IFSC, bank name
   - **UPI ID:** For QR code generation (e.g., yourname@paytm)
   - **GSTIN & PAN:** For tax compliance

### Step 3: Add Clients
1. Go to **Clients** from the navigation menu
2. Click **"Add Client"**
3. Fill in client information:
   - Name and company
   - Contact details
   - Billing address
   - Shipping address (if different)

### Step 4: Create Your First Invoice
1. Go to **Invoices** from the navigation menu
2. Click **"Create Invoice"**
3. Select company and client
4. Set invoice date and due date
5. Add line items:
   - Description (e.g., "Web Development Services")
   - Quantity (e.g., 40 hours)
   - Rate (e.g., 1500 per hour)
   - Discount % (optional)
   - GST % (e.g., 18%)
6. Click **"Add Item"** to add more items
7. Add notes or terms if needed
8. Click **"Save Invoice"**

### Step 5: View & Export Invoice
1. After saving, you'll see the invoice in clean format
2. Click **"Print"** to print directly
3. Click **"Download PDF"** to save as PDF
4. The QR code will appear automatically if you added UPI ID

---

## 📱 Features Overview

### Dashboard
- Total invoices count
- Total revenue
- Paid vs unpaid invoices
- Recent invoices list
- Quick access to create new invoice

### Invoice Management
- Auto-generated invoice numbers (INV-202601-0001)
- Multiple line items with calculations
- GST and discount support
- Amount in words
- Status tracking (Draft, Sent, Paid, Overdue)
- Payment tracking

### PDF Generation
- Professional printable format
- Clean beige/off-white design
- Company logo and details
- QR code for UPI payments
- Bank transfer details
- Authorized signature section

---

## 🛠️ Customization

### Change Company Logo
1. Go to Companies → Edit your company
2. Upload logo image (PNG, JPG recommended)
3. Logo will appear on all invoices

### Add Payment Signature
Currently handled through admin panel or can be added later through payment info model

### Customize Invoice Design
Edit template: `invoices/templates/invoices/invoice_detail.html`

### Change Colors/Styling
Edit CSS: `static/css/style.css`

---

## 📊 Admin Panel Features

Access: http://127.0.0.1:8000/admin/

**Advanced Features:**
- Bulk edit operations
- Advanced filtering and search
- Inline invoice item editing
- Direct database access
- User management

---

## 🔧 Common Tasks

### Add New User
```bash
python manage.py createsuperuser
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Backup Database
Simply copy the `db.sqlite3` file to a safe location

### View Logs
Check terminal where server is running

---

## 🐛 Troubleshooting

### QR Code Not Showing
- Make sure company has UPI ID filled
- Format: `yourname@paytm` or `phonenumber@upi`

### PDF Download Not Working
WeasyPrint requires GTK3 on Windows. If PDF fails:
1. Download GTK3: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. Install and restart server

### Images Not Loading
```bash
python manage.py collectstatic
```

### Server Not Starting
Check if port 8000 is free:
```bash
python manage.py runserver 8080
```

---

## 📞 Next Steps

1. ✅ Create your company profile
2. ✅ Add your first client
3. ✅ Generate a test invoice
4. ✅ Test PDF export
5. ✅ Customize design if needed
6. ✅ Add more clients and invoices

---

## 🎨 Sample Data

For testing, you can create:

**Sample Company:**
- Name: Squarem Technologies
- Address: 123 Business Park, Tech City
- Phone: +91 98765 43210
- Email: info@squarem.com
- UPI: squarem@paytm

**Sample Client:**
- Name: John Doe
- Company: ABC Corporation
- Email: john@abc.com
- Address: 456 Client Street, Business District

**Sample Invoice Items:**
- Web Development - 40 hrs @ ₹1500/hr - GST 18%
- UI/UX Design - 20 hrs @ ₹1200/hr - GST 18%
- Server Setup - 1 @ ₹5000 - GST 18%

---

## 🔒 Security Notes

**For Production:**
- Change SECRET_KEY in settings.py
- Set DEBUG = False
- Configure ALLOWED_HOSTS
- Use strong passwords
- Enable HTTPS
- Use production database (PostgreSQL)

**Current Setup:**
- Development mode (DEBUG = True)
- SQLite database
- Default secret key (change this!)

---

## 📚 Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **Bootstrap 5 Docs:** https://getbootstrap.com/docs/5.3/
- **WeasyPrint Docs:** https://doc.courtbouillon.org/weasyprint/

---

## ✨ Enjoy Your Invoice System!

Your Squarem Invoice application is now ready to use. Start by creating your company profile and generating your first professional invoice.

**Questions?** Check the README.md file for detailed documentation.

---

**Current Status:**
✅ Database migrated
✅ Superuser created (admin/admin123)
✅ Server running on http://127.0.0.1:8000/
✅ All features functional

**Happy Invoicing! 🎉**
