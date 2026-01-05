#!/bin/bash

if [ "$DOCKER_CONTAINER" = "1" ]; then
    export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
    MYSQL_CMD="mysql -u root -h localhost"
else
    MYSQL_CMD="sudo MYSQL_DATABASE=\"$MYSQL_DATABASE\" MYSQL_USERNAME=\"$MYSQL_USERNAME\" MYSQL_PASSWORD=\"$MYSQL_PASSWORD\" mysql -u root"
fi

$MYSQL_CMD <<-EOSQL
    DROP USER IF EXISTS '$MYSQL_USERNAME'@'%';
    DROP USER IF EXISTS '$MYSQL_USERNAME'@'localhost';
    DROP DATABASE IF EXISTS $MYSQL_DATABASE;

    CREATE DATABASE $MYSQL_DATABASE;

    CREATE USER IF NOT EXISTS '$MYSQL_USERNAME'@'%' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PASSWORD';
    GRANT SELECT ON $MYSQL_DATABASE.* TO '$MYSQL_USERNAME'@'%';
    FLUSH PRIVILEGES;

    USE $MYSQL_DATABASE;

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

    INSERT INTO users (name, signup_date, country) VALUES
    ('Alice Smith', '2023-01-15', 'USA'),
    ('Bob Johnson', '2022-12-03', 'Canada'),
    ('Charlie Brown', '2023-03-22', 'UK'),
    ('Diana Miller', '2023-05-10', 'Australia'),
    ('Ethan Davis', '2022-11-28', 'Germany'),
    ('Fiona Wilson', '2023-04-19', 'France'),
    ('George Moore', '2023-02-14', 'Italy'),
    ('Hannah Taylor', '2022-10-07', 'Spain'),
    ('Ian Anderson', '2023-03-05', 'Netherlands'),
    ('Julia Thomas', '2023-01-30', 'Sweden'),
    ('Kevin White', '2023-05-21', 'Norway'),
    ('Laura Harris', '2023-02-27', 'Denmark'),
    ('Michael Martin', '2022-12-18', 'Belgium'),
    ('Nina Thompson', '2023-04-03', 'Switzerland'),
    ('Oliver Garcia', '2023-01-12', 'Portugal'),
    ('Paula Martinez', '2023-03-28', 'Ireland'),
    ('Quentin Robinson', '2023-05-06', 'Austria'),
    ('Rachel Clark', '2023-02-09', 'Finland'),
    ('Sam Lewis', '2022-11-14', 'Poland'),
    ('Tina Lee', '2023-01-23', 'Czech Republic'),
    ('Umar Walker', '2023-03-11', 'Hungary'),
    ('Victoria Hall', '2023-04-25', 'Greece'),
    ('William Allen', '2023-02-02', 'Luxembourg'),
    ('Xenia Young', '2023-01-08', 'Slovakia'),
    ('Yusuf King', '2022-12-29', 'Slovenia'),
    ('Zara Wright', '2023-03-18', 'Croatia'),
    ('Aaron Scott', '2023-05-12', 'Lithuania'),
    ('Bethany Adams', '2023-02-20', 'Latvia'),
    ('Carl Baker', '2023-01-16', 'Estonia'),
    ('Denise Gonzalez', '2023-04-08', 'Malta'),
    ('Eli Perez', '2023-03-01', 'Iceland'),
    ('Faith Murphy', '2023-05-18', 'Norway'),
    ('Gavin Rogers', '2023-02-11', 'Sweden'),
    ('Hailey Reed', '2023-01-25', 'Finland'),
    ('Isaac Cook', '2022-12-09', 'Denmark'),
    ('Jasmine Bailey', '2023-03-14', 'Belgium'),
    ('Kyle Richardson', '2023-04-01', 'Switzerland'),
    ('Lily Cox', '2023-01-19', 'Portugal'),
    ('Mason Howard', '2023-02-24', 'Ireland'),
    ('Natalie Ward', '2023-03-30', 'Austria'),
    ('Owen Peterson', '2023-05-02', 'Finland'),
    ('Penelope Simmons', '2023-02-06', 'Poland'),
    ('Quincy Foster', '2023-01-10', 'Czech Republic'),
    ('Ruby Bennett', '2023-04-15', 'Hungary'),
    ('Sean Hayes', '2023-03-09', 'Greece'),
    ('Tara Hughes', '2023-05-22', 'Luxembourg'),
    ('Victor Sanders', '2023-02-16', 'Slovakia'),
    ('Wendy Butler', '2023-01-28', 'Slovenia'),
    ('Xander Perry', '2023-03-24', 'Croatia'),
    ('Yvonne Russell', '2023-04-12', 'Lithuania'),
    ('Zachary Patterson', '2023-02-04', 'Latvia');

    INSERT INTO orders (user_id, amount, created_at) VALUES
    (1, 49.99, '2023-05-01 10:15:00'),
    (2, 120.50, '2023-05-02 14:20:00'),
    (3, 15.75, '2023-05-03 09:10:00'),
    (4, 200.00, '2023-05-03 12:30:00'),
    (5, 89.90, '2023-05-04 16:45:00'),
    (6, 34.50, '2023-05-05 11:05:00'),
    (7, 78.99, '2023-05-06 08:50:00'),
    (8, 150.00, '2023-05-06 15:15:00'),
    (9, 22.25, '2023-05-07 13:40:00'),
    (10, 60.00, '2023-05-08 09:25:00'),
    (11, 45.75, '2023-05-08 17:00:00'),
    (12, 88.80, '2023-05-09 10:50:00'),
    (13, 99.99, '2023-05-10 12:10:00'),
    (14, 33.33, '2023-05-11 14:30:00'),
    (15, 110.00, '2023-05-11 16:55:00'),
    (16, 25.25, '2023-05-12 09:15:00'),
    (17, 49.49, '2023-05-12 11:35:00'),
    (18, 75.00, '2023-05-13 13:00:00'),
    (19, 60.60, '2023-05-14 15:20:00'),
    (20, 80.80, '2023-05-14 17:45:00'),
    (21, 40.40, '2023-05-15 10:10:00'),
    (22, 150.50, '2023-05-15 12:25:00'),
    (23, 35.35, '2023-05-16 14:40:00'),
    (24, 90.90, '2023-05-17 16:55:00'),
    (25, 55.55, '2023-05-17 18:30:00'),
    (26, 120.20, '2023-05-18 09:05:00'),
    (27, 65.65, '2023-05-18 11:15:00'),
    (28, 70.70, '2023-05-19 13:25:00'),
    (29, 85.85, '2023-05-20 15:35:00'),
    (30, 95.95, '2023-05-20 17:45:00'),
    (31, 100.00, '2023-05-21 10:10:00'),
    (32, 45.00, '2023-05-21 12:20:00'),
    (33, 75.00, '2023-05-22 14:30:00'),
    (34, 60.00, '2023-05-22 16:40:00'),
    (35, 30.00, '2023-05-23 10:50:00'),
    (36, 90.00, '2023-05-23 13:00:00'),
    (37, 110.00, '2023-05-24 15:10:00'),
    (38, 50.00, '2023-05-24 17:20:00'),
    (39, 80.00, '2023-05-25 10:30:00'),
    (40, 20.00, '2023-05-25 12:40:00'),
    (41, 55.00, '2023-05-26 14:50:00'),
    (42, 75.50, '2023-05-26 16:00:00'),
    (43, 65.25, '2023-05-27 10:15:00'),
    (44, 95.75, '2023-05-27 12:25:00'),
    (45, 35.40, '2023-05-28 14:35:00'),
    (46, 45.90, '2023-05-28 16:45:00'),
    (47, 85.10, '2023-05-29 10:05:00'),
    (48, 120.00, '2023-05-29 12:15:00'),
    (49, 60.60, '2023-05-30 14:25:00'),
    (50, 75.75, '2023-05-30 16:35:00');
EOSQL
