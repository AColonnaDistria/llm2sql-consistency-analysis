from sql_generator import MySQLGenerator
import pandas as pd

if __name__ == "__main__":
    test_schema = """
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
    """

    sqlGenerator = MySQLGenerator(seed=53, temperature=1.2)

    print("--- Generating Queries ---")
    df = sqlGenerator.generate_queries(
        user_prompt="Show me the top 5 users from France by total spending",
        schema=test_schema,
        size=10  # Generate 10 variations
    )

    # 6. Display Results
    if df is not None and not df.empty:
        print("\n--- Results ---")
        for query in df['query']:
            print(query + "\n")
        
        df.to_csv("test_results.csv", index=False)
    else:
        print("❌ No data generated.")