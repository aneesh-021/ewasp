import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user="ANEESH021",
        password="Aneeshdesai@21",
        account="wlljihu-zc77775",
        warehouse="COMPUTE_WH",
        database="SALES_DB",
        schema="SALES_SCHEMA"
    )