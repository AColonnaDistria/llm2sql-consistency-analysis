## Natural language to SQL - LLM analysis
This project is an LLM-to-SQL analysis tool designed to quantify non-determinism behavior of LLMs.
Hallucinations and unreliability of LLMs are a huge problem especially when dealing with sensible data.

Features:
- Generate N version of SQL queries for the same prompt
- Scoring: gives syntaxic and structural scores to show how much the candidates are far from each other.
- Clusters: can group same candidates; AST levenhstein similarity scoring is used
- Ambiguity: computes an ambiguity score

This project was inspired by an article about the non-determinism of LLMs when writing code.
I have chosen to focus on SQL queries. The project uses `sqlglot` to parse the SQL code.

## Requirements
```bash
openai
dotenv
diskcache
sqlglot
pandas
PyMySQL
pyyaml
cryptography
textdistance
fastapi[standard]
numpy
```

## Configure
Inside the `app/config.yaml` file, you can access settings to modify the behavior of the program 

```yaml
openai:
  model: gpt-4o
  max_tokens: 600
  seed: 53
  temperature: 1.0
```

## Build & Run
Start at the root of the project.

Copy the .env.example file into .env :
```bash
cp .env.example .env
```

and then edit the .env file :

```bash
OPENAI_API_KEY=YOUR_API_KEY

MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_ROOT_PASSWORD=YOUR_ROOT_PASSWORD

MYSQL_DATABASE=llm_benchmark
MYSQL_USERNAME=llm_tester
MYSQL_PORT=3306

SERVER_PORT=8000
```

You should provide your own OPENAI API KEY. The root password is only used when running through Docker.

## Build & Run (Docker)
In order to run with docker, `docker compose v2` is required. 

On Ubuntu, it can be access through your package manager:
```bash
sudo apt install docker-compose-v2
```

Then, you should run the following commands to create and run your Docker container:
```bash
docker compose up --build
```

## Build & Run (natively)
Firstly install all of the required dependencies using `pip`. You can use a virtual environment in `.venv`.

```bash
python3 -m venv .venv

source .venv/bin/activate
pip install -r requirements.txt
```

You should then first run the setup file which will create the LLM user and the database and then you can run the `run.sh` file:

```bash
sudo ./setup.sh
./run.sh
```

## Using the API

```bash
source .env

# See similarity scores
curl -X POST "http://127.0.0.1:$SERVER_PORT/score/" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE monthly_revenue (month_id INT, revenue DECIMAL(10,2));",
           "number_of_candidates": 20,
           "prompt": "What is the average monthly growth?",
           "expected_query": "SELECT AVG(diff) FROM (SELECT revenue - LAG(revenue) OVER (ORDER BY month_id) as diff FROM monthly_revenue)",
           "datasets": []
        }'

# See heatmaps of similarity
curl -X POST "http://127.0.0.1:$SERVER_PORT/heatmap/" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE monthly_revenue (month_id INT, revenue DECIMAL(10,2));",
           "number_of_candidates": 20,
           "prompt": "What is the average monthly growth?",
           "expected_query": "SELECT AVG(diff) FROM (SELECT revenue - LAG(revenue) OVER (ORDER BY month_id) as diff FROM monthly_revenue)",
           "datasets": []
        }'

# Extract clusters
curl -X POST "http://127.0.0.1:$SERVER_PORT/clusters/" \
     -H "Content-Type: application/json" \
     -d '{
           "schema_db": "CREATE TABLE monthly_revenue (month_id INT, revenue DECIMAL(10,2));",
           "number_of_candidates": 20,
           "prompt": "What is the average monthly growth?",
           "expected_query": "SELECT AVG(diff) FROM (SELECT revenue - LAG(revenue) OVER (ORDER BY month_id) as diff FROM monthly_revenue)",
           "datasets": []
        }'
```

## TODO
- Execution analysis (semantic analysis)
- Verifying correctness & completedness
- Generate or use a dataset and analyze the data

## Ideas
- Implementing a better similarity scoring that accounts for free variables (example `AS total_spending` vs `AS total_spent`)
- Disambiguation by rewriting user prompt
- Trying to use smaller models
- Possibly, looking at performance
- Comparing to NoSQL solutions (MongoDB)

## References
Inspired by this article: https://deepai.org/publication/llm-is-like-a-box-of-chocolates-the-non-determinism-of-chatgpt-in-code-generation