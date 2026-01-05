## Configure
Inside the `app/config.yaml` file, you can access settings to modify the behavior of the program 

```yaml
openai:
  model: gpt-4o
  max_tokens: 600
  seed: 53
  prompt: "Show me the top 5 users from France by total spending"
  size: 5   # Number of different queries generated
  output-file: "test_results.csv"
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

If you edit the app/db/setup.sh file, you should run the following commands (otherwise the script won't run):
```bash
docker compose down -v
docker compose up --build
```

## Build & Run (natively)
Firstly install all of the required dependencies using `pip`. You can use a virtual environment in `.venv`.

```bash
pip install -r requirements.txt
```

You should then first run the setup file which will create the LLM user and the database and then you can run the `run.sh` file:

```bash
sudo ./setup.sh
./run.sh
```