# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import select
from database import database, engine
from models import books

app = FastAPI()

# Modèle Pydantic
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: Optional[str] = None
    year: int

# Démarrer/arrêter la base de données
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    query = books.insert().values(title=book.title, author=book.author, description=book.description, year=book.year)
    last_record_id = await database.execute(query)
    return {**book.dict(), "id": last_record_id}

@app.get("/books/", response_model=List[Book])
async def get_books():
    query = books.select()
    return await database.fetch_all(query)

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    query = books.select().where(books.c.id == book_id)
    book = await database.fetch_one(query)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    query = books.update().where(books.c.id == book_id).values(
        title=updated_book.title,
        author=updated_book.author,
        description=updated_book.description,
        year=updated_book.year,
    )
    await database.execute(query)
    return {**updated_book.dict(), "id": book_id}

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    query = books.select().where(books.c.id == book_id)
    book = await database.fetch_one(query)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    query = books.delete().where(books.c.id == book_id)
    await database.execute(query)
    return book
