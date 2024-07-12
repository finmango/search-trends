FROM python:3.12.4

WORKDIR /app
COPY . .

RUN python3.12 -m pip install poetry

RUN poetry install
