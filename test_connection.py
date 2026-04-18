import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT")
    )

    print(" Connection Successful!")

    conn.close()

except Exception as e:
    print(" Connection Failed:", e)