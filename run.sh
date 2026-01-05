source .env
source .venv/bin/activate

cd app
fastapi run server.py --port $SERVER_PORT
