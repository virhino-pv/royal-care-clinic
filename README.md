# 🏥 Royal Care Clinic & Lab
### Digital Clinic Management & Healthcare Analytics System
> **Brand:** Powered by [Virhino.com](https://virhino.com)  
> **Client Address:** 8, Vijayeswari Street, Razaak Garden, Ayyavoo Colony, Aminjikarai, Chennai, Tamil Nadu 600029.  
> **Contact:** +91 98400 12345 / 044-2365 7890 | **WhatsApp:** +91 98400 12345  
> **Operating Hours:** Mon - Sat: 07:30 AM - 09:30 PM | Sun: 08:00 AM - 01:00 PM

---

## 📌 Executive Overview

**Royal Care Clinic & Lab** is an independent, enterprise-grade digital clinic management and healthcare intelligence platform built specifically for medical practitioners, diagnostic pathologists, reception staff, and patients in Chennai.

---

## 🚀 Key System Features

### 1. 🌐 Public Clinic Website & Patient Portal
- **Modern Healthcare Aesthetics:** Designed with deep clinical royal blue, emerald green accents, and glassmorphism.
- **Hero Section & Quick Booking:** Instant OPD slot and home sample collection booking.
- **Doctor Directory & Timings:** Full specialties, qualifications, experience, fees, and consult schedules.
- **Diagnostic Lab Catalog:** 100+ tests categorized under Hematology, Biochemistry, Thyroid, Clinical Pathology, and Serology with sample requirements and turnaround times.
- **Location & CTAs:** Embedded Google Map of 8 Vijayeswari St Aminjikarai, with direct Call and WhatsApp quick action buttons.

### 2. 🔐 Role-Based Staff Management (RBAC)
- **Administrator:** Full administrative dashboard, doctor roster management, user management, and executive analytics.
- **Doctor / Specialist:** Consultation queue, digital prescription generator (with vitals and dosage schedules), and patient medical history review.
- **Receptionist / Front Desk:** Patient registration, appointment scheduling, and cashier billing.
- **Lab Technician / Pathologist:** Diagnostic worklists, specimen tracking, and abnormal flag verifications.

### 3. 🧪 Comprehensive Diagnostic Laboratory Management
- **Test Categories & Profiles:** Manage test parameters, reference intervals, specimen types, and turnaround hours.
- **Diagnostic Order Workflow:** `Pending Sample` ➔ `Sample Collected` ➔ `Under Testing` ➔ `Completed & Verified`.
- **Automated Pathologist Reports:** Single-click printable A4 diagnostic laboratory report.

### 4. 🧾 Unified Invoicing & Cashier Billing
- **Consolidated Charges:** Seamlessly aggregates doctor consultation fees, diagnostic lab charges, medicines, and procedures.
- **Multi-Mode Payment Tracking:** Cash, UPI / QR Code (GPay / PhonePe), and Card (POS).
- **Printable Receipts:** Computer-generated official tax/fee receipts.

### 5. 📊 Python + Pandas Healthcare Analytics & Power BI Data Engine
- **KPI Dashboards:** Real-time patient volume, new vs. returning patient retention, completion rates, and no-show metrics.
- **Peak Hour Analytics:** Visual breakdown of patient footfall by hour (08:00 AM to 08:00 PM).
- **Financial Trends:** Monthly revenue comparison between OPD consultations and diagnostic investigations.
- **Multi-Format Data Exports:**
  - Full Multi-Sheet Excel Workbook (`.xlsx`) generated dynamically via Pandas and openpyxl.
  - Power BI Star-Schema Zip Bundle (`DimDate.csv`, `DimPatient.csv`, `DimDoctor.csv`, `DimLabTest.csv`, `FactAppointments.csv`, `FactBilling.csv`, `FactLabOrders.csv`).

### 6. 🌐 Decoupled RESTful API (DRF + SimpleJWT)
- Stateless JWT authentication (`/api/auth/token/`)
- Endpoints for patients, doctors, appointments, lab tests, and billing.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13 / 3.14 + Django 6.x
- **API:** Django REST Framework + SimpleJWT
- **Analytics Engine:** Pandas 3.x + NumPy
- **Excel Engine:** OpenPyXL + XlsxWriter
- **Database:** SQLite (default portable) / MySQL 8.0 / PostgreSQL
- **Frontend:** Django Templates + Bootstrap 5 + Bootstrap Icons + Chart.js

---

## 👥 Demo Staff Credentials

| Role | Username | Password |
|------|----------|----------|
| **Administrator** | `admin` | `admin123` |
| **Doctor** | `dr_sharma` | `Doctor@1234` |
| **Receptionist** | `receptionist` | `Staff@1234` |
| **Lab Technician** | `lab_tech` | `Lab@1234` |

---

## ⚙️ Quick Start & Setup

```bash
# 1. Navigate to project folder
cd "D:\Virhino\Virhino Care\Royal Care Clinic & Lab"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Seed database with realistic clinical & analytics records
python manage.py seed_data

# 5. Run test suite
python test_system.py

# 6. Start development server
python manage.py runserver 8000
```

Open your browser at: `http://127.0.0.1:8000/`

---

## 🏢 Client Details & Technology Partner

- **Clinic:** Royal Care Clinic & Lab
- **Location:** 8, Vijayeswari Street, Razaak Garden, Ayyavoo Colony, Aminjikarai, Chennai, Tamil Nadu 600029.
- **Technology Partner:** [Virhino.com](https://virhino.com) — *Empowering healthcare with modern software.*
