from sqlalchemy.orm import Session
from models.book import Book
from schemas.book import BookBase

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Book).all()

    def get_by_seller(self, seller_id: int):
        return self.db.query(Book).filter(Book.seller_id == seller_id).all()

    def get_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def create(self, book_data: BookBase):
        db_book = Book(**book_data.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update(self, book: Book, update_data: BookBase):
        for key, value in update_data.dict().items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book):
        self.db.delete(book)
        self.db.commit()
    
    def update_good(self, book: Book, update_data: dict):  # Cambié el tipo de update_data a dict
        for key, value in update_data.items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book