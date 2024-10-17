# app/routers/books.py

from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List
from app.schemas import BookCreate, BookUpdate, BookInDB, UserInDB
from app.database.connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import Query  # Add this import
from datetime import date  # Add this import
from fastapi import Body  # Add this import
from app.routers.users import get_current_user




router = APIRouter()

@router.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: UserInDB = Security(get_current_user),
):
    # Optional: Check if the user has the 'admin' role
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    book_dict = book.model_dump()
    result = await db["books"].insert_one(book_dict)
    created_book = await db["books"].find_one({"_id": result.inserted_id})
    return BookInDB(**created_book)


@router.get("/{book_id}", response_model=BookInDB)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    book = await db["books"].find_one({"_id": ObjectId(book_id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookInDB(**book)

@router.put("/{book_id}", response_model=BookInDB)
async def update_book(book_id: str, book_update: BookUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    update_data = {k: v for k, v in book_update.model_dump().items() if v is not None}
    if update_data:
        result = await db["books"].update_one({"_id": ObjectId(book_id)}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
    updated_book = await db["books"].find_one({"_id": ObjectId(book_id)})
    return BookInDB(**updated_book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    result = await db["books"].delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

@router.get("/", response_model=List[BookInDB])
async def list_books(db: AsyncIOMotorDatabase = Depends(get_database), author: str = None, genre: str = None):
    query = {}
    if author:
        query["author"] = author
    if genre:
        query["genre"] = genre
    books_cursor = db["books"].find(query)
    books = await books_cursor.to_list(length=100)
    return [BookInDB(**book) for book in books]


@router.get("/search", response_model=List[BookInDB])
async def search_books(
    db: AsyncIOMotorDatabase = Depends(get_database),
    q: str = Query(None, description="Search query"),
    author: str = Query(None),
    genre: str = Query(None),
    price_min: float = Query(None, ge=0),
    price_max: float = Query(None, ge=0),
    publication_date_start: date = Query(None),
    publication_date_end: date = Query(None),
):
    query = {}
    if q:
        query["$text"] = {"$search": q}
    if author:
        query["author"] = author
    if genre:
        query["genre"] = genre
    if price_min is not None or price_max is not None:
        query["price"] = {}
        if price_min is not None:
            query["price"]["$gte"] = price_min
        if price_max is not None:
            query["price"]["$lte"] = price_max
    if publication_date_start or publication_date_end:
        query["publication_date"] = {}
        if publication_date_start:
            query["publication_date"]["$gte"] = publication_date_start
        if publication_date_end:
            query["publication_date"]["$lte"] = publication_date_end

    books_cursor = db["books"].find(query)
    books = await books_cursor.to_list(length=100)
    return [BookInDB(**book) for book in books]


@router.get("/inventory/low-stock", response_model=List[BookInDB])
async def get_low_stock_books(
    db: AsyncIOMotorDatabase = Depends(get_database),
    threshold: int = Query(10, ge=0, description="Stock threshold"),
):
    books_cursor = db["books"].find({"stock_quantity": {"$lte": threshold}})
    books = await books_cursor.to_list(length=100)
    return [BookInDB(**book) for book in books]



@router.patch("/{book_id}/update-stock", response_model=BookInDB)
async def update_stock(
    book_id: str,
    stock_quantity: int = Body(..., embed=True, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    result = await db["books"].update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"stock_quantity": stock_quantity}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = await db["books"].find_one({"_id": ObjectId(book_id)})
    return BookInDB(**updated_book)
