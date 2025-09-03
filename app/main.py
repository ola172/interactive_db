from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import Database
from app.exceptions.custom_exception import CustomException, CustomHTTPException
from app.routers.Instructor_routes import instructor_router
from app.routers.book_route import book_router
from app.routers.course_routes import course_router
from app.routers.pathway_routes import pathway_router
from app.routers.product_routes import product_router
from app.routers.user_routes import router as user_router

app = FastAPI(title="Zedny API")


# ✅ Global Exception Handlers
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.exception_type or "CustomException",
            "detail": exc.detail,
            "additional_info": exc.additional_info,
        },
    )


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.exception_type or "CustomHTTPException",
            "detail": exc.detail,
            "additional_info": exc.additional_info,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Catch-all for unexpected errors
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": str(exc),
        },
    )


# ✅ Routers
app.include_router(product_router)
app.include_router(course_router)
app.include_router(instructor_router)
app.include_router(book_router)
app.include_router(user_router)
app.include_router(pathway_router)

# ✅ Initialize DB
db = Database()


@app.on_event("startup")
async def on_startup():
    """Create tables if they don't exist"""
    await db.create_tables()
