FROM python:3.8.6

WORKDIR /app

COPY pyproject.toml pyproject.toml

# Install and set up poetry.
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY server server
COPY bin bin

ENTRYPOINT ["./bin/start.sh"]
