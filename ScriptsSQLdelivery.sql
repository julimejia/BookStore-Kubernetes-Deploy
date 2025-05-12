CREATE TABLE delivery_providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    coverage_area VARCHAR(150) NOT NULL,
    cost DOUBLE PRECISION NOT NULL
);


CREATE TABLE delivery_assignments (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL REFERENCES purchases(id),
    provider_id INTEGER NOT NULL REFERENCES delivery_providers(id)
);

SELECT * FROM delivery_assignments;
SELECT * FROM delivery_providers;
SELECT * FROM purchases;

INSERT INTO delivery_providers (name, coverage_area, cost) VALUES
('Rápido Bogotá', 'Bogotá D.C. y alrededores', 12000.00),
('Antioquia Express', 'Medellín, Envigado, Bello', 13500.50),
('Costeña Delivery', 'Barranquilla, Cartagena, Santa Marta', 11000.75);
