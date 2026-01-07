from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    url: str

class ProductRead(BaseModel):
    id: int 
    name: str
    url: str

    class Config:
        from_attributes = True