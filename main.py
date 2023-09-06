import uvicorn

from fastapi import FastAPI, HTTPException





from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Book









app = FastAPI()

books_db = []

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    year = Column(Integer)
    pages = Column(Integer)
    isbn = Column(String)


Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
async def home():


    
    return {"message": "Hello Friends..."}


# Create a new book
@app.post("/books/")
async def create_book(book: Book) -> Book:
    db_book = BookDB(**book.dict())
    db = SessionLocal()
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    db.close()
    return book


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    db = SessionLocal()
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    db.close()
    if db_book:
        return db_book
    raise HTTPException(status_code=404, detail="Book not found")


# Get all books
@app.get("/books/")
async def get_all_books():
    db = SessionLocal()
    books = db.query(BookDB).all()
    db.close()
    return books


# Delete a book by ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    db = SessionLocal()
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        db.close()
        return db_book
    db.close()
    raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)



