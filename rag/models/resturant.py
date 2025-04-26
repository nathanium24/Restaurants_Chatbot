from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Restaurant(BaseModel):
    name: str
    location: str
    phone: str
    menu_items: List[str]  # list of MenuItem IDs (as strings for simplicity)
    rating: Optional[float] = None
    opening_hour: str
    dietary_options: Optional[List[str]] = []
    price_range: str
    cuisine: Optional[List[str]] = []
    is_open: Optional[bool] = Field(default=True)