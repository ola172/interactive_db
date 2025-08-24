from pydantic import BaseModel

class ProductTypeCreate(BaseModel):
    name: str

class ProductCreate(BaseModel):
    type_id: int
    title: str
    description: str | None = None
    language: str | None = None
    level: str | None = None
    duration: int | None = None

class ProductTypeRead(ProductTypeCreate):
    id: int
    class Config:
        orm_mode = True

class ProductRead(ProductCreate):
    id: int
    type: ProductTypeRead
    class Config:
        orm_mode = True
