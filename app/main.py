from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import Database
from app.repositories.product import ProductRepository, ProductTypeRepository
from app.schemas.product import ProductCreate, ProductTypeCreate

db = Database()
db.create_tables()

app = FastAPI()

def get_db_session():
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

# ---------- Product Types ----------
@app.get("/types")
def read_types(session: Session = Depends(get_db_session)):
    repo = ProductTypeRepository(session)
    return [t.__dict__ for t in repo.get_all()]

@app.post("/types")
def create_type(type_data: ProductTypeCreate, session: Session = Depends(get_db_session)):
    repo = ProductTypeRepository(session)
    new_type = repo.create(type_data.model_dump())
    return {"message": "Type created", "type": new_type.__dict__}

# ---------- Products ----------
@app.get("/products")
def read_products(session: Session = Depends(get_db_session)):
    repo = ProductRepository(session)
    return [p.__dict__ for p in repo.get_all()]

@app.post("/products")
def create_product(product: ProductCreate, session: Session = Depends(get_db_session)):
    repo = ProductRepository(session)
    new_product = repo.create(product.model_dump())
    return {"message": "Product created", "product": new_product.__dict__}
