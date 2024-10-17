# app/main.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


# Import routers
from app.database.connection import init_db
from app.routers import books, users



app = FastAPI(
    title="Bookstore Inventory Management API",
    version="1.0.0",
    description="An API for managing bookstore inventory.",
)

# Include routers
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Root path
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Bookstore Inventory Management API"}


@app.on_event("startup")
async def startup_event():
    await init_db()





def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Bookstore Inventory API",
        version="1.0.0",
        description="API for managing bookstore inventory",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply security to all paths
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
