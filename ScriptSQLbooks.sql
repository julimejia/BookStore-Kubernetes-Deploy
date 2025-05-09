CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC NOT NULL,
    stock INTEGER DEFAULT 0,
    seller_id INTEGER NOT NULL
);

SELECT * FROM books;