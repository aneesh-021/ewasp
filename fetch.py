import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_data():
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )

        query = f"SELECT * FROM {os.getenv('SNOWFLAKE_TABLE')}"

        # Load into Pandas
        df = pd.read_sql(query, conn)

        conn.close()

        print("✅ Data fetched successfully")
        return df

    except Exception as e:
        print("❌ Error:", e)
        return None


if __name__ == "__main__":
    df = fetch_data()
    print(df.head())