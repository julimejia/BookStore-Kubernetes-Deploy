from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.book import BookOut, BookBase
from services.book_service import BookService
from utils.jwt import get_current_user_id

router = APIRouter()

@router.get("/", response_model=list[BookOut])
def get_all_books(db: Session = Depends(get_db)):
    service = BookService(db)
    return service.list_books()

@router.get("/mine", response_model=list[BookOut])
def get_my_books(
    seller_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.list_books_by_seller(seller_id)

@router.post("/", response_model=BookOut)
def create_book(
    book: BookBase,
    seller_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.create_book(book, seller_id)

@router.put("/{book_id}", response_model=BookOut)
def edit_book(
    book_id: int,
    book_data: BookBase,
    seller_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    result, error = service.update_book(book_id, book_data, seller_id)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Book not found")
    if error == "unauthorized":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return result

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    seller_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    book, error = service.delete_book(book_id, seller_id)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Book not found")
    if error == "unauthorized":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"message": "Book deleted successfully"}

@router.get("/{book_id}", response_model=BookOut)
def get_book_by_id(
    book_id: int,
    db: Session = Depends(get_db)
):
    service = BookService(db)
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/update/{book_id}", response_model=BookOut)
def update_stock(
    book_id: int,
    new_stock: int,
    db: Session = Depends(get_db)
):
    service = BookService(db)
    book, error = service.update_stock(book_id, new_stock)
    if error == "not_found":
        raise HTTPException(status_code=404, detail="Book not found")
    return book