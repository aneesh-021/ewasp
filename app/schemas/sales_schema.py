from pydantic import BaseModel, field_validator
from datetime import datetime

class SalesData(BaseModel):
    date: str
    product_id: str
    quantity_sold: int
    revenue: float
    region: str

    @field_validator("date")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except:
            raise ValueError("Invalid date format (YYYY-MM-DD required)")
        return value

    @field_validator("quantity_sold")
    def quantity_positive(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be > 0")
        return value

    @field_validator("revenue")
    def revenue_non_negative(cls, value):
        if value < 0:
            raise ValueError("Revenue cannot be negative")
        return value

    @field_validator("product_id", "region")
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value