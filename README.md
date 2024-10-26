docker-compose down
docker volume rm idatos_pg_data

docker-compose up
docker run -it --rm --network idatos_default postgis/postgis:latest psql -h db -U idatos -d db_name

poetry install
poetry run uvicorn app.main:app --reload
