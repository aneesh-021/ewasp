from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io
from app.schemas.sales_schema import SalesData
from app.db.snowflake_conn import get_connection

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # Clean column names
    df.columns = df.columns.str.strip()

    # Clean string values
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    valid_data = []
    invalid_data = []

    # Validation
    for _, row in df.iterrows():
        row_dict = row.to_dict()

        try:
            validated = SalesData(**row_dict)
            valid_data.append(validated.model_dump())
        except Exception as e:
            invalid_data.append({
                "row": row_dict,
                "error": str(e)
            })

    # ================= ETL =================
    valid_df = pd.DataFrame(valid_data)

    if not valid_df.empty:
        revenue_by_region = (
            valid_df.groupby("region")["revenue"]
            .sum()
            .reset_index()
            .to_dict(orient="records")
        )

        quantity_by_product = (
            valid_df.groupby("product_id")["quantity_sold"]
            .sum()
            .reset_index()
            .to_dict(orient="records")
        )

        daily_sales = (
            valid_df.groupby("date")["revenue"]
            .sum()
            .reset_index()
            .to_dict(orient="records")
        )
    else:
        revenue_by_region = []
        quantity_by_product = []
        daily_sales = []

    # ================= SNOWFLAKE INSERT =================
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("Connected to Snowflake")

        data_to_insert = [
            (
                row["date"],
                row["product_id"],
                row["quantity_sold"],
                row["revenue"],
                row["region"],
                row["cost"],
                row["vendor_id"],
                row["vendor_delay_days"],
                row["inventory_level"],
                row["price"],
                row["discount"],
                row["customer_segment"],
                row["order_priority"],
                row["lead_time_days"],
                row["return_rate"]
            )
            for row in valid_data
        ]

        cursor.executemany(
            """
            INSERT INTO SALES_DB.SALES_SCHEMA.SALES_DATA
            (date, product_id, quantity_sold, revenue, region,
             cost, vendor_id, vendor_delay_days,
             inventory_level, price, discount,
             customer_segment, order_priority,
             lead_time_days, return_rate)
            VALUES (%s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s)
            """,
            data_to_insert
        )

        conn.commit()

        print("Inserted rows:", len(valid_data))

        cursor.close()
        conn.close()

    except Exception as e:
        print("Snowflake Error:", e)

    # ================= RESPONSE =================
    return {
        "valid_count": len(valid_data),
        "invalid_count": len(invalid_data),
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "analytics": {
            "revenue_by_region": revenue_by_region,
            "quantity_by_product": quantity_by_product,
            "daily_sales": daily_sales
        }
    }