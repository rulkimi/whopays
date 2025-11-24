# whopays

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
docker compose up -d (first setup)
alembic upgrade init (if no alembic folder generated)
alembic upgrade head
alembic/sripts/arev.sh "explanation" (to generate migrations)