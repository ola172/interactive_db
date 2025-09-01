from fastapi import FastAPI

from app.core.database import Database
from app.routers.Instructor_routes import instructor_router
from app.routers.book_route import book_router
from app.routers.course_routes import course_router
from app.routers.pathway_routes import pathway_router
from app.routers.product_routes import product_router
from app.routers.user_routes import router as user_router

app = FastAPI(title="Zedny API")

# Include routers
app.include_router(product_router)
app.include_router(course_router)
app.include_router(instructor_router)
app.include_router(book_router)
app.include_router(user_router)
app.include_router(pathway_router)

# Initialize DB
db = Database()


@app.on_event("startup")
async def on_startup():
    """Create tables if they don't exist"""
    await db.create_tables()
