from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlglot

import pandas as pd
import numpy as np

from sql_schema_init import MySQLSchemaInitializer
from sql_generator import MySQLGenerator
from sql_evaluator import SQLSyntaxicEvaluator, SQLStructuralEvaluator
from config_manager import ConfigManager

import os

app = FastAPI()
config = ConfigManager('config.yaml')

if os.getenv('DOCKER_CONTAINER') == '1':
    host = 'mysql'
else:
    host = 'localhost'
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

class EvaluateRequestBody(BaseModel):
    schema_db: str
    number_of_candidates: int
    expected_query: str
    prompt: str
    datasets: list

@app.post("/heatmap")
async def evaluate(body: EvaluateRequestBody):
    try:
        parsed = sqlglot.parse(body.schema_db)

        # Compute candidates
        print("--- Generating Queries ---")

        sqlGenerator = MySQLGenerator(
            seed=config.get('openai.seed'), 
            temperature=config.get('openai.temperature')
        )

        df = sqlGenerator.generate_queries(
            user_prompt=body.prompt,
            schema=body.schema_db,
            size=body.number_of_candidates
        )

        candidates = df['query']
        for query in candidates:
            print(query + "\n")
            
        print("--- Syntaxic ---")

        sqlSyntaxicEvaluator = SQLSyntaxicEvaluator(candidates)
        exact_matches = sqlSyntaxicEvaluator.exact_matches()
        levenhstein_heatmap = sqlSyntaxicEvaluator.levenhstein_normalized()

        sqlStructuralEvaluator = SQLStructuralEvaluator(candidates)
        exact_matches_ast = sqlStructuralEvaluator.exact_matches()
        levenhstein_heatmap_ast = sqlStructuralEvaluator.levenhstein_normalized()

        def flatten_matrix(data):
            if isinstance(data, pd.DataFrame):
                return data.values.tolist()
            if isinstance(data, np.ndarray):
                return data.tolist()
            return [list(row.values()) for row in data.values()]
        
        return {
            "candidates": candidates,
            "exact_matches": flatten_matrix(exact_matches),
            "levenhstein_heatmap": flatten_matrix(levenhstein_heatmap),
            "exact_matches_ast": flatten_matrix(exact_matches_ast),
            "levenhstein_heatmap_ast": flatten_matrix(levenhstein_heatmap_ast)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid SQL Syntax: {str(e)}")


@app.post("/score/")
async def evaluateSummary(body: EvaluateRequestBody):
    try:
        parsed = sqlglot.parse(body.schema_db)

        # Compute candidates
        print("--- Generating Queries ---")

        sqlGenerator = MySQLGenerator(
            seed=config.get('openai.seed'), 
            temperature=config.get('openai.temperature')
        )

        df = sqlGenerator.generate_queries(
            user_prompt=body.prompt,
            schema=body.schema_db,
            size=body.number_of_candidates
        )

        candidates = df['query']
        for query in candidates:
            print(query + "\n")
            
        print("--- Syntaxic ---")

        sqlSyntaxicEvaluator = SQLSyntaxicEvaluator(candidates)
        exact_matches_score = sqlSyntaxicEvaluator.exact_matches_score()
        levenhstein_score = sqlSyntaxicEvaluator.levenhstein_normalized_score()

        sqlStructuralEvaluator = SQLStructuralEvaluator(candidates)
        exact_matches_score_ast = sqlStructuralEvaluator.exact_matches_score()
        levenhstein_score_ast = sqlStructuralEvaluator.levenhstein_normalized_score()

        ambiguity_score = sqlStructuralEvaluator.get_ambiguity_score()

        return {
            "candidates": candidates,
            "exact_matches_score": exact_matches_score,
            "levenhstein_score": levenhstein_score,
            "exact_matches_ast": exact_matches_score_ast,
            "levenhstein_score_ast": levenhstein_score_ast,
            "ambiguity_score": ambiguity_score
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid SQL Syntax: {str(e)}")

@app.post("/clusters/")
async def findClusters(body: EvaluateRequestBody):
    try:
        parsed = sqlglot.parse(body.schema_db)

        # Compute candidates
        print("--- Generating Queries ---")

        sqlGenerator = MySQLGenerator(
            seed=config.get('openai.seed'), 
            temperature=config.get('openai.temperature')
        )

        df = sqlGenerator.generate_queries(
            user_prompt=body.prompt,
            schema=body.schema_db,
            size=body.number_of_candidates
        )

        candidates = df['query']
        for query in candidates:
            print(query + "\n")
            
        sqlStructuralEvaluator = SQLStructuralEvaluator(candidates)
        levenhstein_clusters = sqlStructuralEvaluator.extract_levenhstein_clusters()
    
        return {
            "candidates": candidates,
            "levenhstein_clusters": levenhstein_clusters
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid SQL Syntax: {str(e)}")

@app.post("/clusters/repr/")
async def findClustersRepresentants(body: EvaluateRequestBody):
    try:
        parsed = sqlglot.parse(body.schema_db)

        # Compute candidates
        print("--- Generating Queries ---")

        sqlGenerator = MySQLGenerator(
            seed=config.get('openai.seed'), 
            temperature=config.get('openai.temperature')
        )

        df = sqlGenerator.generate_queries(
            user_prompt=body.prompt,
            schema=body.schema_db,
            size=body.number_of_candidates
        )

        candidates = df['query']
        for query in candidates:
            print(query + "\n")
            
        sqlStructuralEvaluator = SQLStructuralEvaluator(candidates)
        levenhstein_clusters = sqlStructuralEvaluator.extract_levenhstein_clusters()

        levenhstein_clusters_repr = [levenhstein_cluster[0] for levenhstein_cluster in levenhstein_clusters]

        return {
            "candidates": candidates,
            "levenhstein_clusters_repr": levenhstein_clusters_repr
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid SQL Syntax: {str(e)}")
