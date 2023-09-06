from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, BookDB, Base
import pytest

client = TestClient(app)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
    )


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.query(BookDB).delete()
    db.commit()
    db.close()


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello World"}


def test_create_book_endpoint(db):
    book_data = {
        "title": "Sample Book",
        "author": "John Doe",
        "year": 2023,
        "pages": 300,
        "isbn": "1234567890",
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    created_book = response.json()
    assert created_book["title"] == "Sample Book"


def test_get_book_endpoint(db):
    # Add a test book to the database
    test_book = BookDB(
        title="Test Book", author="Author", year=2021, pages=250, isbn="987654"
    )
    db.add(test_book)
    db.commit()

    response = client.get("/books/1")
    assert response.status_code == 200
    retrieved_book = response.json()
    assert retrieved_book["title"] == "Test Book"


def test_get_all_books(db):
    # Clear the database and add test books
    db.query(BookDB).delete()
    db.commit()

    test_books = [
        BookDB(
            title="Book 1", author="Author 1",
            year=2022, pages=200, isbn="123456"
        ),
        BookDB(
            title="Book 2", author="Author 2",
            year=2023, pages=250, isbn="789012"
        ),
    ]
    db.add_all(test_books)
    db.commit()

    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2
    assert books[0]["title"] == "Book 1"
    assert books[1]["title"] == "Book 2"


def test_delete_book(db):
    # Clear the database and add a test book
    db.query(BookDB).delete()
    db.commit()

    test_book = BookDB(
        title="Book 1",
        author="Author 1",
        year=2022,
        pages=200,
        isbn="123456"
    )
    db.add(test_book)
    db.commit()

    response = client.delete("/books/1")
    assert response.status_code == 200
    deleted_book = response.json()
    assert deleted_book["title"] == "Book 1"

    # Check if the book is no longer in the database
    deleted_book = db.query(BookDB).filter(BookDB.id == 1).first()
    assert deleted_book is None
