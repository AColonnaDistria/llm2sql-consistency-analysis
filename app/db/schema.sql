DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    signup_date DATE,
    country VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount DECIMAL(10, 2),
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);