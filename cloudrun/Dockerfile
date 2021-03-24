FROM python:3.8-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml

# Install and set up poetry.
RUN pip install poetry==1.0.10
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY server server
COPY bin bin

ENTRYPOINT ["./bin/start.sh"]
