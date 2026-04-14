from pydantic import BaseModel
from datetime import date

class SalesData(BaseModel):
    date: date
    product_id: str
    quantity_sold: int
    revenue: float
    region: str

    cost: float
    vendor_id: str
    vendor_delay_days: int

    inventory_level: int
    price: float
    discount: float
    customer_segment: str
    order_priority: str
    lead_time_days: int
    return_rate: float