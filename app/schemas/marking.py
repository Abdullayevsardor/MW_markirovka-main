from pydantic import BaseModel

class MarkingCreate(BaseModel):
    product_id: int
