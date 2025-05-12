CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id) ON DELETE SET NULL,
    amount DOUBLE PRECISION,
    payment_method VARCHAR,
    payment_status VARCHAR
);


