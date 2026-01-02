from sql_generator import MySQLGenerator
import pandas as pd
import os

from config_manager import ConfigManager

def run():
    config = ConfigManager('config.yaml')

    with open('schema.sql') as schema_file:
        schema = schema_file.read()

    print(schema)
    
    sqlGenerator = MySQLGenerator(
        seed=config.get('openai.seed'), 
        temperature=config.get('openai.temperature')
    )

    print("--- Generating Queries ---")
    df = sqlGenerator.generate_queries(
        user_prompt=config.get('openai.prompt'),
        schema=schema,
        size=config.get('openai.size', 1)
    )

    if df is not None and not df.empty:
        print("\n--- Results ---")
        for query in df['query']:
            print(query + "\n")
        
        df.to_csv(f"out/{config.get('openai.output-file')}", index=False)


if __name__ == "__main__":
    run()