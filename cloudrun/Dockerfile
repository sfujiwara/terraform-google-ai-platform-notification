FROM python:3.8.6

COPY pyproject.toml pyproject.toml

# Install and set up poetry.
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY server server

ENTRYPOINT ["gunicorn", "server.main:app", "--threads", "8", "--workers", "1", "--timeout", "0"]
