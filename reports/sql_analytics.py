import pandas as pd
from django.db import connection

class SQLAnalyticsExecutor:
    """
    Executes raw analytical SQL queries against the active MySQL database (royalcare_db)
    for Royal Care Clinic & Lab.
    """

    @staticmethod
    def execute_raw_sql(sql_query, params=None):
        """Executes a raw SQL statement and returns a Pandas DataFrame."""
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params or [])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=columns)

    @classmethod
    def get_daily_appointments_sql(cls):
        sql = """
        SELECT 
            appointment_date,
            COUNT(*) AS total_appointments,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
            SUM(CASE WHEN status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count
        FROM appointments_appointment
        GROUP BY appointment_date
        ORDER BY appointment_date DESC
        LIMIT 30;
        """
        return cls.execute_raw_sql(sql)

    @classmethod
    def get_doctor_performance_sql(cls):
        sql = """
        SELECT 
            d.id AS doctor_id,
            CONCAT(u.first_name, ' ', u.last_name) AS doctor_name,
            d.specialization,
            COUNT(a.id) AS total_consultations,
            SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS completed_consultations,
            SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_consultations,
            COALESCE(SUM(CASE WHEN a.status = 'completed' THEN a.fee ELSE 0 END), 0) AS total_doctor_revenue
        FROM doctors_doctor d
        JOIN accounts_user u ON d.user_id = u.id
        LEFT JOIN appointments_appointment a ON d.id = a.doctor_id
        GROUP BY d.id, u.first_name, u.last_name, d.specialization
        ORDER BY total_consultations DESC;
        """
        return cls.execute_raw_sql(sql)

    @classmethod
    def get_revenue_summary_sql(cls):
        sql = """
        SELECT 
            payment_method,
            COUNT(id) AS total_invoices,
            SUM(total_amount) AS total_billed,
            SUM(paid_amount) AS total_collected
        FROM billing_invoice
        GROUP BY payment_method
        ORDER BY total_collected DESC;
        """
        return cls.execute_raw_sql(sql)

    @classmethod
    def get_lab_demand_sql(cls):
        sql = """
        SELECT 
            lt.code AS test_code,
            lt.name AS test_name,
            lc.name AS category_name,
            lt.price AS unit_price,
            COUNT(loi.id) AS orders_count,
            COUNT(loi.id) * lt.price AS gross_revenue
        FROM lab_labtest lt
        JOIN lab_labcategory lc ON lt.category_id = lc.id
        LEFT JOIN lab_laborderitem loi ON lt.id = loi.test_id
        GROUP BY lt.id, lt.code, lt.name, lc.name, lt.price
        ORDER BY orders_count DESC;
        """
        return cls.execute_raw_sql(sql)
