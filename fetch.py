import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_data():
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )

        cursor = conn.cursor()

        query = f"""
        SELECT *
        FROM {os.getenv("SNOWFLAKE_TABLE")}
        LIMIT 100
        """

        cursor.execute(query)

        # Fetch data
        data = cursor.fetchall()

        # Get column names
        columns = [col[0] for col in cursor.description]

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=columns)

        print(" Data fetched successfully")
        return df

    except Exception as e:
        print(" Error:", e)
        return None

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


if __name__ == "__main__":
    df = fetch_data()

    if df is not None:
        print(df.head())
    else:
        print(" No data fetched")