from sqlalchemy.orm import Session
from schemas.book import BookBase, BookCreate
from repository.book_repository import BookRepository

class BookService:
    def __init__(self, db: Session):
        self.repo = BookRepository(db)

    def list_books(self):
        return self.repo.get_all()

    def list_books_by_seller(self, seller_id: int):
        return self.repo.get_by_seller(seller_id)

    def create_book(self, book_data: BookBase, seller_id: int):
        book_with_seller = BookCreate(**book_data.dict(), seller_id=seller_id)
        return self.repo.create(book_with_seller)

    def update_book(self, book_id: int, book_data: BookBase, seller_id: int):
        book = self.repo.get_by_id(book_id)
        if not book:
            return None, "not_found"
        if book.seller_id != seller_id:
            return None, "unauthorized"
        updated_book = self.repo.update(book, book_data)
        return updated_book, None

    def delete_book(self, book_id: int, seller_id: int):
        book = self.repo.get_by_id(book_id)
        if not book:
            return None, "not_found"
        if book.seller_id != seller_id:
            return None, "unauthorized"
        self.repo.delete(book)
        return book, None

    def get_book(self, book_id: int):
        return self.repo.get_by_id(book_id)


    def update_stock(self, book_id: int, new_stock: int):
        book = self.repo.get_by_id(book_id)
        if not book:
            return None, "not_found"
        update_data = {"stock": new_stock}
        updated_book = self.repo.update_good(book, update_data)  
        return updated_book, None