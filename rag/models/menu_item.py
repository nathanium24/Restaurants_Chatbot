from pydantic import BaseModel, Field
from typing import Optional

class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    is_veg: Optional[bool] = Field(default=None) 
    category: str
    resturant_id: str = Field(..., description="The ID of the restaurant this menu item belongs to")