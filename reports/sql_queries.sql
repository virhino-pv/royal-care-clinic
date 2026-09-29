-- ==============================================================================
-- ROYAL CARE CLINIC & LAB — PRODUCTION SQL ANALYTICS LAYER
-- Technology Partner: Powered by Virhino.com
-- Database Engine: MySQL 8.x / 8.0.44 Compatible
-- ==============================================================================

-- 1. Daily Appointments Summary
-- Calculates total, completed, cancelled, and no-show appointments grouped by date
SELECT 
    appointment_date,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
    SUM(CASE WHEN status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count,
    ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS completion_rate_pct
FROM appointments_appointment
GROUP BY appointment_date
ORDER BY appointment_date DESC;

-- 2. Weekly Appointments Trend
SELECT 
    DATE_FORMAT(appointment_date, '%Y-%u') AS year_week,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM appointments_appointment
GROUP BY year_week
ORDER BY year_week DESC;

-- 3. Monthly Appointments Trend
SELECT 
    DATE_FORMAT(appointment_date, '%Y-%m') AS month_period,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
    SUM(CASE WHEN status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count
FROM appointments_appointment
GROUP BY month_period
ORDER BY month_period DESC;

-- 4. Doctor-wise Appointment Volume & Performance
SELECT 
    d.id AS doctor_id,
    CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
    d.specialization,
    COUNT(a.id) AS total_consultations,
    SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS completed_consultations,
    SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_consultations,
    ROUND(SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(a.id), 0), 1) AS completion_pct,
    COALESCE(SUM(CASE WHEN a.status = 'completed' THEN a.fee ELSE 0 END), 0) AS total_doctor_revenue
FROM doctors_doctor d
JOIN accounts_user u ON d.user_id = u.id
LEFT JOIN appointments_appointment a ON d.id = a.doctor_id
GROUP BY d.id, u.first_name, u.last_name, d.specialization
ORDER BY total_consultations DESC;

-- 5. Service-wise / Consultation Type Breakdown
SELECT 
    appointment_type,
    COUNT(*) AS booking_count,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    ROUND(SUM(CASE WHEN status = 'completed' THEN fee ELSE 0 END), 2) AS total_fee_collected
FROM appointments_appointment
GROUP BY appointment_type
ORDER BY booking_count DESC;

-- 6. Completed Appointments Detail Analysis
SELECT 
    a.id AS appointment_id,
    a.appointment_date,
    a.appointment_time,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.phone AS patient_phone,
    CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
    a.appointment_type,
    a.fee
FROM appointments_appointment a
JOIN patients_patient p ON a.patient_id = p.id
JOIN doctors_doctor d ON a.doctor_id = d.id
JOIN accounts_user u ON d.user_id = u.id
WHERE a.status = 'completed'
ORDER BY a.appointment_date DESC, a.appointment_time DESC;

-- 7. Cancelled Appointments Root Cause Log
SELECT 
    a.id AS appointment_id,
    a.appointment_date,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
    a.reason,
    a.doctor_notes
FROM appointments_appointment a
JOIN patients_patient p ON a.patient_id = p.id
JOIN doctors_doctor d ON a.doctor_id = d.id
JOIN accounts_user u ON d.user_id = u.id
WHERE a.status = 'cancelled'
ORDER BY a.appointment_date DESC;

-- 8. No-Show Appointments Analysis
SELECT 
    a.id AS appointment_id,
    a.appointment_date,
    a.appointment_time,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.phone AS patient_phone,
    d.specialization
FROM appointments_appointment a
JOIN patients_patient p ON a.patient_id = p.id
JOIN doctors_doctor d ON a.doctor_id = d.id
WHERE a.status = 'no_show'
ORDER BY a.appointment_date DESC;

-- 9. New Patient Registrations per Month
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') AS registration_month,
    COUNT(*) AS new_patients_registered,
    SUM(CASE WHEN gender = 'male' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN gender = 'female' THEN 1 ELSE 0 END) AS female_count
FROM patients_patient
GROUP BY registration_month
ORDER BY registration_month DESC;

-- 10. Returning Patients vs Single-Visit Patients (CTE Cohort Analysis)
WITH PatientVisitCounts AS (
    SELECT 
        patient_id,
        COUNT(*) AS visit_count
    FROM appointments_appointment
    GROUP BY patient_id
)
SELECT 
    CASE 
        WHEN pvc.visit_count = 1 THEN '1 Visit (Single)'
        WHEN pvc.visit_count BETWEEN 2 AND 4 THEN '2-4 Visits (Returning)'
        ELSE '5+ Visits (Frequent)'
    END AS cohort,
    COUNT(p.id) AS patient_count,
    ROUND(COUNT(p.id) * 100.0 / (SELECT COUNT(*) FROM patients_patient), 1) AS pct_of_total_patients
FROM patients_patient p
LEFT JOIN PatientVisitCounts pvc ON p.id = pvc.patient_id
GROUP BY cohort
ORDER BY patient_count DESC;

-- 11. Daily Revenue Breakdown (Consultation vs Lab vs Total Paid)
SELECT 
    DATE(created_at) AS transaction_date,
    COUNT(id) AS invoices_issued,
    SUM(consultation_charges) AS total_consultation_revenue,
    SUM(lab_charges) AS total_lab_revenue,
    SUM(medicine_charges) AS total_pharmacy_revenue,
    SUM(discount_amount) AS total_discounts,
    SUM(paid_amount) AS net_cash_collected
FROM billing_invoice
GROUP BY transaction_date
ORDER BY transaction_date DESC;

-- 12. Weekly Revenue Summary
SELECT 
    DATE_FORMAT(created_at, '%Y-%u') AS year_week,
    COUNT(id) AS invoices_count,
    SUM(total_amount) AS total_billed,
    SUM(paid_amount) AS total_collected
FROM billing_invoice
GROUP BY year_week
ORDER BY year_week DESC;

-- 13. Monthly Revenue Trend & Realization Rate
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') AS month_period,
    COUNT(id) AS total_bills,
    SUM(total_amount) AS gross_billed,
    SUM(paid_amount) AS net_revenue_collected,
    ROUND(SUM(paid_amount) * 100.0 / NULLIF(SUM(total_amount), 0), 1) AS collection_efficiency_pct
FROM billing_invoice
GROUP BY month_period
ORDER BY month_period DESC;

-- 14. Doctor-wise Revenue Generation
SELECT 
    d.id AS doctor_id,
    CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
    d.specialization,
    COUNT(a.id) AS completed_consultations,
    SUM(a.fee) AS total_consultation_billed
FROM appointments_appointment a
JOIN doctors_doctor d ON a.doctor_id = d.id
JOIN accounts_user u ON d.user_id = u.id
WHERE a.status = 'completed'
GROUP BY d.id, u.first_name, u.last_name, d.specialization
ORDER BY total_consultation_billed DESC;

-- 15. Service / Diagnostic Category Revenue Breakdown
SELECT 
    lc.name AS lab_category,
    COUNT(loi.id) AS total_tests_performed,
    SUM(lt.price) AS total_category_revenue
FROM lab_laborderitem loi
JOIN lab_labtest lt ON loi.test_id = lt.id
JOIN lab_labcategory lc ON lt.category_id = lc.id
GROUP BY lc.id, lc.name
ORDER BY total_category_revenue DESC;

-- 16. Peak Appointment Hours Distribution (Hourly Heatmap)
SELECT 
    HOUR(appointment_time) AS hour_of_day,
    COUNT(*) AS total_appointments_booked,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count
FROM appointments_appointment
GROUP BY hour_of_day
ORDER BY hour_of_day ASC;

-- 17. Patient Visit Frequency & Top Patient Ranking
SELECT 
    p.id AS patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.phone,
    COUNT(a.id) AS total_appointments,
    MAX(a.appointment_date) AS last_visit_date,
    COALESCE(SUM(inv.paid_amount), 0) AS lifetime_spend
FROM patients_patient p
LEFT JOIN appointments_appointment a ON p.id = a.patient_id
LEFT JOIN billing_invoice inv ON p.id = inv.patient_id
GROUP BY p.id, p.first_name, p.last_name, p.phone
ORDER BY total_appointments DESC
LIMIT 20;

-- 18. Diagnostic Laboratory Test Demand & Revenue Velocity
SELECT 
    lt.code AS test_code,
    lt.name AS test_name,
    lc.name AS category_name,
    lt.sample_type,
    lt.price AS unit_price,
    COUNT(loi.id) AS orders_count,
    COUNT(loi.id) * lt.price AS gross_revenue,
    SUM(CASE WHEN loi.is_abnormal = 1 THEN 1 ELSE 0 END) AS abnormal_result_count
FROM lab_labtest lt
JOIN lab_labcategory lc ON lt.category_id = lc.id
LEFT JOIN lab_laborderitem loi ON lt.id = loi.test_id
GROUP BY lt.id, lt.code, lt.name, lc.name, lt.sample_type, lt.price
ORDER BY orders_count DESC;
