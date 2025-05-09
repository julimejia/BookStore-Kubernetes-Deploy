from fastapi import FastAPI
from routes import books

app = FastAPI(title="Books Service")

app.include_router(books.router, prefix="/books", tags=["Books"])