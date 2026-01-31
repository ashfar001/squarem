# 🎓 Tutorial: Creating Your First Invoice

This guide will walk you through creating a complete invoice from scratch.

---

## Prerequisites

✅ Server is running: `python manage.py runserver`
✅ You're logged in as admin

---

## Step-by-Step Tutorial

### 1️⃣ Create a Company (Your Business)

**Navigate:** Companies → Add Company

Fill in the form:
```
Basic Information:
- Name: Squarem Technologies Pvt Ltd
- Email: billing@squarem.com
- Phone: +91 9876543210
- Website: https://squarem.com

Address:
- Address: Suite 301, Tech Tower
           Innovation Park
- City: Bangalore
- State: Karnataka
- Postal Code: 560001
- Country: India

Bank Details:
- Bank Name: HDFC Bank
- Branch: Koramangala Branch
- Account Number: 50200012345678
- IFSC Code: HDFC0001234
- UPI ID: squarem@paytm

Tax Details:
- GSTIN: 29ABCDE1234F1Z5
- PAN: ABCDE1234F
```

**Click:** Save Company

---

### 2️⃣ Create a Client

**Navigate:** Clients → Add Client

Fill in the form:
```
Basic Information:
- Name: Rajesh Kumar
- Company Name: TechStart Solutions
- Email: rajesh@techstart.com
- Phone: +91 9988776655
- GSTIN: 29XYZAB5678G1H9

Billing Address:
- Address: #45, 2nd Floor, MG Road
- City: Bangalore
- State: Karnataka
- Postal Code: 560002
- Country: India

Shipping Address: (same as billing)
[Leave blank or copy billing address]
```

**Click:** Save Client

---

### 3️⃣ Create an Invoice

**Navigate:** Invoices → Create Invoice

**Invoice Information:**
```
- Company: Select "Squarem Technologies Pvt Ltd"
- Client: Select "Rajesh Kumar"
- Invoice Date: Today's date (auto-filled)
- Due Date: 30 days from today (auto-filled)
- Currency: ₹ INR
- Status: Draft
- Amount Paid: 0.00
```

**Line Items:**

**Item 1:**
```
Description: Website Development - Frontend
Quantity: 40
Rate: 1500
Discount %: 0
GST %: 18
```

**Item 2:**
```
Description: Website Development - Backend
Quantity: 60
Rate: 1800
Discount %: 5
GST %: 18
```

**Item 3:**
```
Description: UI/UX Design Services
Quantity: 25
Rate: 1200
Discount %: 0
GST %: 18
```

**Item 4:**
```
Description: Domain & Hosting Setup (1 Year)
Quantity: 1
Rate: 5000
Discount %: 10
GST %: 18
```

**Click "Add Item"** if you need more rows.

**Additional Information:**
```
Notes:
Thank you for your business. Please make the payment 
within the due date to avoid any inconvenience.

Terms:
1. Payment is due within 30 days
2. Late payments will incur 2% monthly interest
3. Bank transfer or UPI payment accepted
4. All disputes subject to Bangalore jurisdiction
```

**Click:** Save Invoice

---

### 4️⃣ View Your Invoice

After saving, you'll be redirected to the invoice detail page where you'll see:

✅ Professional invoice layout
✅ Company logo area (if uploaded)
✅ Invoice number (auto-generated: INV-202601-0001)
✅ All line items with calculations
✅ Subtotal, GST, and Grand Total
✅ Amount in words
✅ Bank details for payment
✅ UPI QR code (if UPI ID provided)
✅ Terms and conditions

---

### 5️⃣ Expected Calculations

**Breakdown:**

**Item 1:** Website Frontend
- Subtotal: 40 × 1500 = ₹60,000
- Discount: 0% = ₹0
- Taxable: ₹60,000
- GST (18%): ₹10,800
- **Total: ₹70,800**

**Item 2:** Website Backend  
- Subtotal: 60 × 1800 = ₹108,000
- Discount: 5% = ₹5,400
- Taxable: ₹102,600
- GST (18%): ₹18,468
- **Total: ₹121,068**

**Item 3:** UI/UX Design
- Subtotal: 25 × 1200 = ₹30,000
- Discount: 0% = ₹0
- Taxable: ₹30,000
- GST (18%): ₹5,400
- **Total: ₹35,400**

**Item 4:** Domain & Hosting
- Subtotal: 1 × 5000 = ₹5,000
- Discount: 10% = ₹500
- Taxable: ₹4,500
- GST (18%): ₹810
- **Total: ₹5,310**

**Grand Total:**
```
Subtotal:    ₹203,000.00
Discount:    -₹5,900.00
GST (18%):   +₹35,478.00
─────────────────────────
Total:       ₹232,578.00
```

**Amount in Words:**
"Two Lakh Thirty Two Thousand Five Hundred Seventy Eight Rupees Only"

---

### 6️⃣ Export Options

**Print Invoice:**
1. Click the **"Print"** button
2. Your browser's print dialog will open
3. Select printer or "Save as PDF"
4. Action buttons and navigation will be hidden automatically

**Download PDF:**
1. Click the **"Download PDF"** button
2. PDF will be generated using WeasyPrint
3. File name: `invoice_INV-202601-0001.pdf`
4. Ready to email or share

---

### 7️⃣ Update Invoice Status

**After sending to client:**
1. Go to Invoices → Find your invoice
2. Click **"Edit"**
3. Change Status to **"Sent"**
4. Save

**After receiving payment:**
1. Edit the invoice again
2. Update **"Amount Paid"** to ₹232,578.00
3. Change Status to **"Paid"**
4. Save

The balance due will automatically update to ₹0.00

---

## 🎯 Testing Checklist

✅ Company details appear correctly
✅ Client information is accurate
✅ All 4 line items are listed
✅ Calculations are correct
✅ GST is calculated properly
✅ Discount is applied correctly
✅ Grand total matches expected: ₹232,578.00
✅ Amount in words is displayed
✅ QR code appears (if UPI ID provided)
✅ Bank details are shown
✅ Print preview works
✅ PDF downloads successfully

---

## 💡 Pro Tips

1. **Reuse Clients:** Once created, clients appear in dropdown for future invoices

2. **Invoice Numbering:** Format is INV-YYYYMM-XXXX
   - Automatically increments
   - Resets monthly
   - Always unique

3. **Quick Entry:** Use Tab key to move between fields quickly

4. **Delete Items:** Check the DELETE checkbox to remove line items

5. **Draft Status:** Keep as Draft while working, change to Sent when ready

6. **Payment Tracking:** Update Amount Paid to track partial payments

7. **Search:** Use the search bar in invoice list to find invoices quickly

8. **Filter by Status:** Filter invoices by Draft, Sent, Paid, etc.

---

## 📱 Mobile View

The invoice is responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- All modern browsers

---

## 🎨 Customization Ideas

**Logo:**
- Upload 200x80px PNG with transparent background
- Will appear on all invoices

**Colors:**
- Edit `static/css/style.css` to change color scheme
- Current: Professional blue with beige invoice background

**Layout:**
- Edit `invoices/templates/invoices/invoice_detail.html`
- Rearrange sections as needed

---

## 🔄 Creating More Invoices

Now that you have:
- ✅ 1 Company
- ✅ 1 Client
- ✅ 1 Invoice

**Next steps:**
1. Add more clients (5-10 for testing)
2. Create multiple invoices
3. Track payments
4. Generate reports from dashboard

---

## 📊 Dashboard Overview

After creating a few invoices, your dashboard will show:
- Total invoices count
- Total revenue
- Paid invoices (green)
- Unpaid/Overdue (orange/red)
- Recent invoices table with quick actions

---

## ✨ Congratulations!

You've successfully created your first professional invoice!

**What you learned:**
✅ Setting up company profile
✅ Adding clients
✅ Creating detailed invoices
✅ Understanding calculations
✅ Exporting PDFs
✅ Tracking payments

**Ready for production?**
- Review the README.md for deployment guide
- Change admin password
- Update SECRET_KEY
- Configure production settings

---

**Need help?** Check README.md or settings documentation.

**Happy Invoicing! 🎉**
