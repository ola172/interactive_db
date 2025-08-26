from typing import Any, AsyncGenerator

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Database
from app.repositories.product import ProductRepository, ProductTypeRepository
from app.schemas.product import ProductCreate, ProductTypeCreate

db = Database()

app = FastAPI()


# ---------- Startup event to create tables ----------
@app.on_event("startup")
async def on_startup():
    await db.create_tables()


# ---------- Dependency ----------
async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async for session in db.get_session():
        yield session


# ---------- Product Types ----------
@app.get("/types")
async def read_types(session: AsyncSession = Depends(get_db_session)):
    repo = ProductTypeRepository(session)
    types = await repo.get_all()
    return [t.__dict__ for t in types]


@app.post("/types")
async def create_type(type_data: ProductTypeCreate, session: AsyncSession = Depends(get_db_session)):
    repo = ProductTypeRepository(session)
    new_type = await repo.create(type_data.model_dump())
    return {"message": "Type created", "type": new_type.__dict__}


# ---------- Products ----------
@app.get("/products")
async def read_products(session: AsyncSession = Depends(get_db_session)):
    repo = ProductRepository(session)
    products = await repo.get_all()
    return [p.__dict__ for p in products]


@app.post("/products")
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_db_session)):
    repo = ProductRepository(session)
    new_product = await repo.create(product.model_dump())
    return {"message": "Product created", "product": new_product.__dict__}
