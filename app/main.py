from sql_generator import MySQLGenerator
import pandas as pd
import os

from config_manager import ConfigManager

from sql_executor import MySQLExecutor

from sql_evaluator import SQLSyntaxicEvaluator, SQLStructuralEvaluator, SQLValidityEvaluator

def run():
    config = ConfigManager('config.yaml')

    with open('db/schema.sql') as schema_file:
        schema = schema_file.read()
    
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

    print("--- Execute queries ---")

    if os.getenv('DOCKER_CONTAINER') == '1':
        host = 'mysql'
    else:
        host = 'localhost'

    sqlExecutor = MySQLExecutor(
        host=host,
        user=config.get('mysql.username'),
        database=config.get('mysql.database'),
        password=config.get('mysql.password')
    )

    for query in df['query']:
        print(sqlExecutor.run_query(query))

    print("--- Evaluate queries ---")
    print("--- Validity ---")

    sqlValidityEvaluator = SQLValidityEvaluator(df['query'])
    print(sqlValidityEvaluator.parsable_scores())

    print("--- Syntaxic ---")

    sqlSyntaxicEvaluator = SQLSyntaxicEvaluator(df['query'])

    print("--- Exact matches ---")
    print(sqlSyntaxicEvaluator.exact_matches())

    print("--- Levenhstein ---")
    levenhstein_heatmap = sqlSyntaxicEvaluator.levenhstein_normalized()
    print(levenhstein_heatmap)

    sqlStructuralEvaluator = SQLStructuralEvaluator(df['query'])
    print("--- Exact matches ---")
    print(sqlStructuralEvaluator.exact_matches())

    print("--- Levenshtein ---")
    print(sqlStructuralEvaluator.levenhstein_normalized())

if __name__ == "__main__":
    run()