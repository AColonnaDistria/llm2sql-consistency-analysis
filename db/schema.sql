CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    signup_date DATE,
    country VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);