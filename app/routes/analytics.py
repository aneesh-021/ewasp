from fastapi import APIRouter
from app.db.snowflake_conn import get_connection

router = APIRouter()   # ✅ THIS IS REQUIRED

# 1️⃣ Sales Summary
@router.get("/sales/summary")
def get_sales_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(revenue) AS total_revenue,
            SUM(quantity_sold) AS total_quantity
        FROM SALES_DB.SALES_SCHEMA.SALES_DATA
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "total_revenue": result[0],
        "total_quantity": result[1]
    }


# 2️⃣ Sales by Region
@router.get("/sales/by-region")
def sales_by_region():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT region, SUM(revenue) 
        FROM SALES_DB.SALES_SCHEMA.SALES_DATA
        GROUP BY region
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {"region": row[0], "revenue": row[1]}
        for row in rows
    ]