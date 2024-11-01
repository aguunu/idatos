FROM python:3.10

WORKDIR /code

COPY . .

RUN pip install poetry

RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


