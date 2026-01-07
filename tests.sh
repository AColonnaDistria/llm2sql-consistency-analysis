
curl -X POST "http://127.0.0.1:8001/semantic" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE IF NOT EXISTS sales (id INT, customer_name VARCHAR(50), amount DECIMAL(10,2));",
           "tables": ["sales"],
           "number_of_candidates": 20,
           "prompt": "Find the best customer",
           "expected_query": "SELECT customer_name FROM sales GROUP BY customer_name ORDER BY SUM(amount) DESC LIMIT 1",
           "tests": [
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Alice'\'', 120.00), (2, '\''Bob'\'', 300.00), (3, '\''Alice'\'', 150.00), (4, '\''Charlie'\'', 200.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Dave'\'', 500.00), (2, '\''Eve'\'', 700.00), (3, '\''Dave'\'', 300.00), (4, '\''Eve'\'', 200.00), (5, '\''Frank'\'', 400.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Gina'\'', 1000.00), (2, '\''Hank'\'', 800.00), (3, '\''Gina'\'', 200.00), (4, '\''Hank'\'', 300.00), (5, '\''Ivy'\'', 1200.00);"
           ]
        }' | jq

curl -X POST "http://127.0.0.1:8001/score" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE IF NOT EXISTS sales (id INT, customer_name VARCHAR(50), amount DECIMAL(10,2));",
           "tables": ["sales"],
           "number_of_candidates": 20,
           "prompt": "Find the best customer",
           "expected_query": "SELECT customer_name FROM sales GROUP BY customer_name ORDER BY SUM(amount) DESC LIMIT 1",
           "tests": [
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Alice'\'', 120.00), (2, '\''Bob'\'', 300.00), (3, '\''Alice'\'', 150.00), (4, '\''Charlie'\'', 200.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Dave'\'', 500.00), (2, '\''Eve'\'', 700.00), (3, '\''Dave'\'', 300.00), (4, '\''Eve'\'', 200.00), (5, '\''Frank'\'', 400.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Gina'\'', 1000.00), (2, '\''Hank'\'', 800.00), (3, '\''Gina'\'', 200.00), (4, '\''Hank'\'', 300.00), (5, '\''Ivy'\'', 1200.00);"
           ]
        }' | jq

curl -X POST "http://127.0.0.1:8001/clusters" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE IF NOT EXISTS sales (id INT, customer_name VARCHAR(50), amount DECIMAL(10,2));",
           "tables": ["sales"],
           "number_of_candidates": 20,
           "prompt": "Find the best customer",
           "expected_query": "SELECT customer_name FROM sales GROUP BY customer_name ORDER BY SUM(amount) DESC LIMIT 1",
           "tests": [
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Alice'\'', 120.00), (2, '\''Bob'\'', 300.00), (3, '\''Alice'\'', 150.00), (4, '\''Charlie'\'', 200.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Dave'\'', 500.00), (2, '\''Eve'\'', 700.00), (3, '\''Dave'\'', 300.00), (4, '\''Eve'\'', 200.00), (5, '\''Frank'\'', 400.00);",
               "INSERT INTO sales (id, customer_name, amount) VALUES (1, '\''Gina'\'', 1000.00), (2, '\''Hank'\'', 800.00), (3, '\''Gina'\'', 200.00), (4, '\''Hank'\'', 300.00), (5, '\''Ivy'\'', 1200.00);"
           ]
        }' | jq
