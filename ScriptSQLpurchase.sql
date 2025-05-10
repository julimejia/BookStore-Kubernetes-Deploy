CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price FLOAT NOT NULL,
    status VARCHAR(255) DEFAULT 'Pending Payment'
);

SELECT * FROM purchases;


SELECT * FROM books;