from pydantic import BaseModel, Field
from typing import Dict, Union

class MenuItem(BaseModel):
    name: str
    description: str = Field(default="")  # Description can be empty string
    price: float
    attributes: Dict[str, Union[str, int]]
    restaurant_id: str  # Foreign key reference to the restaurant